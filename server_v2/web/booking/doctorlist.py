#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    1.  VtsDoctorHandler
        Type: Class
        Methods:
            A.GET:
                Get all doctor  details under that entity
                Line: 39
            B.POST:
                Will create new row doctors
                Line: 162
            C.PUT:
                Update Doctor details on doctors.
                Line: 335
            D:DELETE:
                Delete the Doctor from Vehicles.
                Line: 523
'''

from __future__ import division
from PIL import Image
from ..lib.lib import *
import requests
import http.client
import datetime

@xenSecureV1
class DocterListHandler(tornado.web.RequestHandler):

    SUPPORTED_METHODS = ('GET','POST','PUT','DELETE')

    #User profile to identify the App
    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]
    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]
    #Other Item lists
    doc_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][0]['name']
                ]




    fu = FileUtil()

    async def post(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            # TODO: this need to be moved in a global class, from here
            profileQ = self.profile.find(
                    {
                        'closed': False,
                        'entityId': self.entityId,
                        'accountId': self.accountId,
                        'applicationId': self.applicationId
                    },
                    {
                        '_id': 1
                    },
                    limit=1
                )
            profile = []
            async for i in profileQ:
                profile.append(i)

            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                appQ = self.applications.find(
                        {
                            '_id': self.applicationId
                        },
                        {
                            '_id': 1,
                            'apiId': 1
                        },
                        limit=1
                )
                app = []
                async for i in appQ:
                        app.append(i)

                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [ 502020, 502022]:
                        if self.apiId == 502020:
                            try:
                                serviceId = ObjectId(self.request.arguments.get('serviceId'))
                            except:
                                code = 4888
                                message = "Invalid Service Id"
                                raise Exception

                            try:
                                aTime = long(self.request.arguments.get('time'))
                                code, message = Validate.i(
                                         aTime,
                                         'Time',
                                        )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ time ].'
                                raise Exception


                            comment = self.request.arguments.get('comment')
                            code, message = Validate.i(
                                            comment,
                                            'Comment',
                                            dataType=unicode,
                                            maxLength=400
                                        )
                            if code != 4100:
                                raise Exception

                            session = self.request.arguments.get('session')
                            if session == None or session == 'One-time-session':
                                session = 1
                            else:
                                code, message = Validate.i(
                                                session,
                                                'session',
                                                datatype=int,
                                            )
                                if code != 4100:
                                    raise Exception

                            accDetailsQ = self.account.find(
                                            {
                                                '_id':self.accountId,
                                            },
                                            {
                                                '_id':0,
                                                'firstName':1,
                                                'lastName':1,
                                                'contact':1
                                            }
                                        )
                            accDetails = []
                            async for i in accDetailsQ:
                                accDetails.append(i)

                            if not len(accDetails):
                                code= 4055
                                status = False
                                message = "No Account Found"
                                raise Exception

                            fullName = str(accDetails[0]['firstName']) + ' ' + str(accDetails[0]['lastName'])
                            phoneNumber = accDetails[0]['contact'][0]['value']
                            # TODO: Country code hard coded
                            phoneNumber = str(phoneNumber - 910000000000)
                            Log.i('Customer Phone Number', phoneNumber)


                            serListQ = self.serviceList.find(
                                        {
                                            '_id':serviceId
                                        }
                                    )
                            serList = []
                            async for i in serListQ:
                                serList.append(i)
                            if not len(serList):
                                code = 4060
                                message = "Invalid Service"
                                raise Exception

                            serName = serList[0]['serNameEnglish']

                            cancelFeeQQ = self.cancelFee.find(
                                            {
                                                'profileId':self.profileId
                                            }
                                        )
                            cancelFeeQ = []
                            async for i in cancelFeeQQ:
                                cancelFeeQ.append(i)
                            if len(cancelFeeQ):
                                cancelFeeAmt = cancelFeeQ[0]['cancellationFee']
                            else:
                                cancelFeeAmt = 0

                            docId = self.doc_list.insert_one(
                                        {
                                            'disabled':False,
                                            'cancelFee':cancelFeeAmt,
                                            'accountDetails':accDetails,
                                            'stage':'new',
                                            'serviceId':serviceId,
                                            'booktime':aTime,
                                            'session':session,
                                            'session_remaining':session,
                                            'requestedTime':timeNow(),
                                            'profileId':self.profileId,
                                            'entityId':self.entityId,
                                            'comment':comment
                                        }
                                    )

                            date = int(aTime/1000000)
                            date = date + 19800
                            newDate = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %I:%M:%p')

                            if docId:
                                cancelFeeDel = self.cancelFee.delete_many(
                                                {
                                                    'profileId':self.profileId
                                                }
                                            )
                                conn = http.client.HTTPSConnection("api.msg91.com")
                                sms = 'Greetings from Ohzas. Your appointement for {} at {} has been \
                                        placed on request'.format(serName,newDate)
                                payloadJson = {
                                                "sender":"SOCKET",
                                                "route":4,
                                                "country":91,
                                                "sms":[
                                                        {
                                                            "message":sms,
                                                            "to":[phoneNumber]
                                                        }
                                                    ]
                                                }
                                payload = json.dumps(payloadJson)
                                headers = {
                                            'authkey': MSG91_GW_ID,
                                            'content-type': "application/json"
                                        }
                                conn.request("POST", "/api/v2/sendsms", payload, headers)
                                res = conn.getresponse()
                                data = res.read()
                                stat = json.loads(data.decode("utf-8"))
                                Log.i('Notification Status',stat['type'])
                                if stat['type'] == "success":
                                    code = 2000
                                    message = "Request has been submitted."
                                    Log.i('SMS notification is sent')
                                    status = True
                                else:
                                    code = 4055
                                    message = "Request has been submitted."
                                    Log.i('SMS notification could not be sent')
                                    status = True
                                sms = 'Hi! A Request to appointement for {} at {} has been \
                                        placed through the OHZAS app. The request is placed by \
                                        {} and the contact number is {}'\
                                        .format(serName,newDate,fullName,phoneNumber,)
                                adminNum = str(CONFIG['medAdmin_contact'][0]['num1'])
                                payloadJson = {
                                                "sender":"SOCKET",
                                                "route":4,
                                                "country":91,
                                                "sms":[
                                                        {
                                                            "message":sms,
                                                            "to":[adminNum]
                                                        }
                                                    ]
                                                }
                                payload = json.dumps(payloadJson)
                                headers = {
                                            'authkey': MSG91_GW_ID,
                                            'content-type': "application/json"
                                        }
                                conn.request("POST", "/api/v2/sendsms", payload, headers)
                                res = conn.getresponse()
                                data = res.read()
                                stat = json.loads(data.decode("utf-8"))
                                Log.i('Notification Status',stat['type'])
                                if stat['type'] == "success":
                                    code = 2000
                                    status = True
                                else:
                                    code = 4055
                                    Log.i('SMS notification could not be sent to admin to check the request')
                                    status = False
                            else:
                                code = 4040
                                message = "Invalid Appointment"
                                status = False
                                raise Exception
                        elif self.apiId == 502022:
                            try:
                                docId = ObjectId(self.request.arguments.get('docId'))
                            except:
                                code = 4888
                                message = "Invalid Booking Id"
                                raise Exception
                            serBookQ = self.doc_list.find(
                                    {
                                        '_id':docId
                                    }
                                )
                            serBook = []
                            async for i in serBookQ:
                                serBook.append(i)
                            if not len(serBook):
                                code = 4060
                                message = "Invalid Booking"
                                raise Exception
                            phoneNumber = serBook[0]['accountDetails'][0]['contact'][0]['value']
                            phoneNumber = str(phoneNumber - 910000000000)
                            Log.i('Customer Phone Number', phoneNumber)
                            serListQ = self.serviceList.find(
                                    {
                                        '_id':serBook[0]['serviceId']
                                    }
                                )
                            serList = []
                            async for i in serListQ:
                                serList.append(i)
                            if not len(serList):
                                code = 4060
                                message = "Invalid Service"
                                raise Exception
                            serName = serList[0]['serNameEnglish']
                            if serBook[0]['stage'] == 'accepted':
                                if serBook[0]['session_remaining'] <= 0:
                                    code = 4565
                                    status = False
                                    message = "Invalid Session Update"
                                    raise Exception
                                if serBook[0]['session_remaining'] == 1:
                                    serBookUpdate = self.doc_list.update_one(
                                                    {
                                                        '_id':docId
                                                    },
                                                    {
                                                    '$set':{
                                                            'stage':'completed'
                                                            },
                                                    '$inc':{
                                                            'session_remaining':-1
                                                            }
                                                    }
                                                )
                                    if serBookUpdate['n']:
                                        code = 2000
                                        status = True
                                        message = "Session is updated and booking is complete."
                                        sms = 'Greetings from Ohzas! Your session is complete\
                                                and your appointment for {} has been finished.\
                                            We look forward to provide service to you again. '.format(serName)
                                        conn = http.client.HTTPSConnection("api.msg91.com")
                                        payloadJson = {
                                                    "sender":"SOCKET",
                                                    "route":4,
                                                    "country":91,
                                                    "sms":[
                                                            {
                                                                "message":sms,
                                                                "to":[phoneNumber]
                                                            }
                                                        ]
                                                    }
                                        payload = json.dumps(payloadJson)
                                        headers = {
                                                'authkey': MSG91_GW_ID,
                                                'content-type': "application/json"
                                            }
                                        conn.request("POST", "/api/v2/sendsms", payload, headers)
                                        res = conn.getresponse()
                                        data = res.read()
                                        stat = json.loads(data.decode("utf-8"))
                                        Log.i('Notification Status',stat['type'])
                                        if stat['type'] == "success":
                                            code = 2000
                                            message = "Request has been submitted and SMS notification has been sent"
                                            status = True
                                        else:
                                            code = 4055
                                            message = "Request has been submitted but the SMS notification could not be sent"
                                            status = False
                                    else:
                                        code = 4555
                                        status = False
                                        message = "Session could not be updated."
                                        raise Exception
                                else:
                                    erBookUpdate = self.doc_list.update_one(
                                                    {
                                                        '_id':docId
                                                    },
                                                    {
                                                    '$inc':{
                                                            'session_remaining':-1
                                                            }
                                                    }
                                                )
                                    if serBookUpdate['n']:
                                        code = 2000
                                        status = True
                                        message = "Session is updated."
                                    else:
                                        code = 4555
                                        status = False
                                        message = "Session could not be updated."
                                        raise Exception
                            else:
                                code = 2000
                                status = False
                                message = "Invalid Session Update"
                        else:
                            code = 4003
                            self.set_status(401)
                            message = 'You are not Authorized.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not Authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not Authorized.'

            else:
                code = 4003
                self.set_status(401)
                message = 'You are not Authorized.'
        except Exception as e:
            status = False
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return

    async def put(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            # TODO: this need to be moved in a global class, from here
            profileQ = self.profile.find(
                    {
                        'closed': False,
                        'entityId': self.entityId,
                        'accountId': self.accountId,
                        'applicationId': self.applicationId
                    },
                    {
                        '_id': 1
                    },
                    limit=1
                )
            profile = []
            async for i in profileQ:
                profile.append(i)

            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                appQ = self.applications.find(
                        {
                            '_id': self.applicationId
                        },
                        {
                            '_id': 1,
                            'apiId': 1
                        },
                        limit=1
                )
                app = []
                async for i in appQ:
                        app.append(i)

                if len(app):
                    self.apiId = app[0]['apiId']
                    Log.i(self.apiId)
                    if self.apiId in [ 502020, 502022]:
                        if self.apiId == 502022:
                            try:
                                docId = ObjectId(self.request.arguments.get('docId'))
                            except:
                                code = 4050
                                message = "Invalid Booking Id"
                                raise Exception
                            try:
                                stage = self.request.arguments.get('stage').lower()
                            except:
                                stage = None

                            serBookQ = self.doc_list.find(
                                        {
                                            '_id':docId
                                        }
                                    )
                            serBook = []
                            async for i in serBookQ:
                                serBook.append(i)
                            if not len(serBook):
                                code = 4060
                                message = "Invalid Booking"
                                raise Exception
                            phoneNumber = serBook[0]['accountDetails'][0]['contact'][0]['value']
                            # TODO: Country code hard coded
                            phoneNumber = str(phoneNumber - 910000000000)
                            Log.i('Customer Phone Number', phoneNumber)

                            serListQ = self.serviceList.find(
                                        {
                                            '_id':serBook[0]['serviceId']
                                        }
                                    )
                            serList = []
                            async for i in serListQ:
                                serList.append(i)
                            if not len(serList):
                                code = 4060
                                message = "Invalid Service"
                                raise Exception

                            serName = serList[0]['serNameEnglish']

                            if stage in ['accepted','declined','completed','declined_fee']:
                                serUpdate = self.doc_list.update_one(
                                            {
                                                '_id':docId
                                            },
                                            {
                                            '$set':{
                                                        'stage':stage
                                                   }
                                            }
                                        )
                                if stage in ['declined','completed','declined_fee']:
                                    sessionUpdate = self.doc_list.update_one(
                                                {
                                                    '_id':docId
                                                },
                                                {
                                                '$set':{
                                                            'session_remaining':0
                                                       }
                                                }
                                            )
                                if stage == 'completed':
                                    sms = 'Greetings from Ohzas! Your appointment is complete. \
                                            We look forward to provide service to you again. '
                                elif stage == 'declined':
                                    sms = 'Greetings from Ohzas! We regret to inform you that your \
                                            appointment for {} has been cancelled. \
                                            We look forward to provide service to you again.'.format(serName)
                                elif stage == 'declined_fee':
                                    sms = 'Greetings from Ohzas! We regret to inform you that your \
                                            appointment for {} has been cancelled. \
                                            You will be charged \
                                            a cancellation fee in your next appointment.\
                                            We look forward to provide service to you again.'.format(serName)
                                    cancelUpdate = self.cancelFee.update_one(
                                                    {
                                                        'profileId':serBook[0]['profileId']
                                                    },
                                                    {
                                                    '$set':{
                                                                'profileId':serBook[0]['profileId'],
                                                                'cancellationFee':50,
                                                                'docId':docId,
                                                                'cancelTime':timeNow(),
                                                                'bookingTime':serBook[0]['booktime']
                                                            }
                                                    },
                                                    upsert=True
                                                )
                                else:
                                    sms = 'Hello! Greetings from Ohzas! Your appointement for {} has been {}'.format(serName,stage)
                                if serUpdate['n']:
                                    conn = http.client.HTTPSConnection("api.msg91.com")
                                    payloadJson = {
                                                    "sender":"SOCKET",
                                                    "route":4,
                                                    "country":91,
                                                    "sms":[
                                                            {
                                                                "message":sms,
                                                                "to":[phoneNumber]
                                                            }
                                                        ]
                                                    }
                                    payload = json.dumps(payloadJson)
                                    headers = {
                                                'authkey': MSG91_GW_ID,
                                                'content-type': "application/json"
                                            }
                                    conn.request("POST", "/api/v2/sendsms", payload, headers)
                                    res = conn.getresponse()
                                    data = res.read()
                                    stat = json.loads(data.decode("utf-8"))
                                    Log.i('Notification Status',stat['type'])
                                    if stat['type'] == "success":
                                        code = 2000
                                        message = "Request has been submitted and SMS notification has been sent"
                                        status = True
                                    else:
                                        code = 4055
                                        message = "Request has been submitted but the SMS notification could not be sent"
                                        status = False
                                else:
                                    code = 2000
                                    message = "Invalid booking"
                                    status = True
                            else:
                                code = 4070
                                status = False
                                message = "Invalid Option"
                        elif self.apiId == 502020:
                            try:
                                docId = ObjectId(self.request.arguments.get('docId'))
                            except:
                                code = 4050
                                message = "Invalid Booking Id"
                                raise Exception
                            serBookQ = self.doc_list.find(
                                        {
                                            '_id':docId
                                        }
                                    )
                            serBook = []
                            async for i in serBookQ:
                                serBook.append(i)
                            if not len(serBook):
                                code = 4060
                                message = "Invalid Booking"
                                raise Exception
                            phoneNumber = serBook[0]['accountDetails'][0]['contact'][0]['value']
                            # TODO: Country code hard coded
                            phoneNumber = str(phoneNumber - 910000000000)
                            Log.i('Customer Phone Number', phoneNumber)

                            serListQ = self.serviceList.find(
                                        {
                                            '_id':serBook[0]['serviceId']
                                        }
                                    )
                            serList = []
                            async for i in serListQ:
                                serList.append(i)
                            if not len(serList):
                                code = 4060
                                message = "Invalid Service"
                                raise Exception

                            serName = serList[0]['serNameEnglish']

                            serUpdate = self.doc_list.update_one(
                                        {
                                            '_id':docId
                                        },
                                        {
                                        '$set':{
                                                    'stage':'declined'
                                                }
                                        }
                                    )
                            sms = 'Greetings from Ohzas! We are sorry to know that you \
                                    have cancelled the appointment for {}. \
                                    We look forward to provide service to you again.'.format(serName)
                            if serUpdate['n']:
                                conn = http.client.HTTPSConnection("api.msg91.com")
                                payloadJson = {
                                                "sender":"SOCKET",
                                                "route":4,
                                                "country":91,
                                                "sms":[
                                                        {
                                                            "message":sms,
                                                            "to":[phoneNumber]
                                                        }
                                                    ]
                                                }
                                payload = json.dumps(payloadJson)
                                headers = {
                                            'authkey': MSG91_GW_ID,
                                            'content-type': "application/json"
                                        }
                                conn.request("POST", "/api/v2/sendsms", payload, headers)
                                res = conn.getresponse()
                                data = res.read()
                                stat = json.loads(data.decode("utf-8"))
                                Log.i('Notification Status',stat['type'])
                                if stat['type'] == "success":
                                    code = 2000
                                    message = "Request has been cancelled"
                                    status = True
                                else:
                                    code = 4055
                                    Log.i('SMS notification could not be sent')
                            else:
                                code = 2000
                                message = "Invalid booking"
                                status = True
                        else:
                            code = 4003
                            self.set_status(401)
                            message = 'You are not Authorized.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not Authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not Authorized.'

            else:
                code = 4003
                self.set_status(401)
                message = 'You are not Authorized.'
        except Exception as e:
            status = False
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return

    async def get(self):

        status = False
        code = 4000
        result = []
        message = ''
        try:
            docId = self.request.arguments['id'][0]
        except:
            docId = None
        try:
            # TODO: this need to be moved in a global class
            profileQ = self.profile.find(
                    {
                        'closed': False,
                        'entityId': self.entityId,
                        'accountId': self.accountId,
                        'applicationId': self.applicationId
                    },
                    {
                        '_id': 1
                    },
                    limit=1
                )
            profile = []
            async for i in profileQ:
                profile.append(i)

            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('ProfID', self.profileId)
                appQ = self.applications.find(
                        {
                            '_id': self.applicationId
                        },
                        {
                            '_id': 1,
                            'apiId': 1
                        },
                        limit=1
                )
                app = []
                async for i in appQ:
                        app.append(i)
                #Determine which app has sent it
                if len(app):
                    self.apiId = app[0]['apiId']
                    if app[0]['apiId'] in [ 502020, 502022]: # TODO: till here
                        if self.apiId == 502022:
                            Log.i('APIID', self.apiId)
                            if docId == None:
                                resQ = self.doc_list.find(
                                        {
                                            'entityId':self.entityId,
                                            'disabled':False
                                        }
                                    )
                                res = []
                                async for i in resQ:
                                    res.append(i)
                            else:
                                try:
                                    docId = ObjectId(docId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid Booking Id"
                                resQ = self.doc_list.find(
                                        {
                                            'entityId':self.entityId,
                                            '_id':docId,
                                            'disabled':False
                                        }
                                    )
                                res = []
                                async for i in resQ:
                                    res.append(i)

                            #Res is from doc_list collections whatevr matches
                            '''
                            if len(res):
                                for docinfo in res:
                                    #Collec the Data from doc_list collections row
                                    v = {
                                            '_id':str(docinfo['_id']),
                                            'accountDetails':docinfo['accountDetails'],
                                            'booktime':docinfo['booktime'],
                                            'stage':docinfo['stage'],
                                            'disabled':docinfo['disabled'],
                                            'requestedTime':docinfo['requestedTime'],
                                            'comment':docinfo['comment'],
                                            'logo':"https://medix.xlayer.in/uploads/default/logo.jpg",
                                            'address':'Ohzas,Banaras.'
                                        }
                                    try:
                                        if len(str(docinfo['session_remaining'])) and docinfo['stage'] in ['new','accepted']:
                                            v['session_remaining'] = docinfo['session_remaining']
                                        else:
                                            v['session_remaining'] = 0
                                    except:
                                        v['session_remaining'] = 'N/A'

                                    #Check the clinic ID  of the doctor

                                    serInfoQ = self.serviceList.find(
                                                {
                                                    '_id':docinfo['serviceId']
                                                },
                                                {
                                                    '_id':0,
                                                    'serNameHindi':1,
                                                    'serNameEnglish':1,
                                                    'serCharges':1,
                                                    'serTA':1,
                                                    'serTATotal':1,
                                                    'serDA':1,
                                                    'serDATotal':1
                                                }
                                            )
                                    serInfo = []
                                    async for i in serInfoQ:
                                        serInfo.append(i)
                                    if docinfo['session'] in [5,6,7,8,9,10]:
                                        discount = 0.1
                                    elif docinfo['session'] in [11,12,13,14,15]:
                                        discount = 0.15
                                    elif docinfo['session'] in [16,17,18,19,20]:
                                        discount = 0.2
                                    else:
                                        discount = 0
                                    try:
                                        if len(str(docinfo['cancelFee'])):
                                            cancelFeeAmt = docinfo['cancelFee']
                                        else:
                                            cancelFeeAmt = 0
                                    except:
                                        cancelFeeAmt = 0
                                    serInfo[0]['serTATotal'] = serInfo[0]['serTATotal'] - (discount * serInfo[0]['serTATotal'])\
                                            + cancelFeeAmt
                                    v['cancelFee'] = cancelFeeAmt
                                    v['serviceDetails'] = serInfo
                                    v['serviceTotal'] = serInfo[0]['serTATotal']
                                    result.append(v)
                                result.reverse()
                                code = 2000
                                status = True
                            else:
                                code = 4080
                                status = False
                                message = "No data found"
                            '''
                        elif self.apiId == 502020:
                            try:
                                docId = int(self.request.arguments["id"][0])

                            except:
                                docId = None

                            if docId == None:
                                '''
                                resQ = self.doc_list.find(
                                        {
                                            'entityId':self.entityId,
                                            'profileId':self.profileId
                                        }
                                    )
                                '''
                                #resQ = self.doc_list.find()
                                resQ = await self.doc_list.count_documents({})
                                res = []
                                Log.i('resQ ', resQ)
                                resQ = self.doc_list.find({})
                                async for i in resQ:
                                    i["_id"]=str(i["_id"])
                                    res.append(i)
                                Log.i('result ', res)

                                for doc in res:
                                    v= {"id": int(doc["docid"]), "doc": str(doc["docname"]) }
                                    result.append(v)
                            else:
                                try:
                                    docId = ObjectId(docId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid Booking Id"
                                resQ = self.doc_list.find(
                                        {

                                            'docid':docId
                                        }
                                    )
                                result = []
                                async for i in resQ:
                                    i["_id"]= str(i["_id"])
                                    result.append(i)

                            if len(result):


                                result.reverse()
                                code = 2000
                                status = True
                                message = "Doc List "
                            else:
                                code = 4080
                                status = False
                                message = "No data found"
                        else:
                            code = 4003
                            self.set_status(401)
                            message = 'You are not authorized.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not authorized.'
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not authorized.'
        except Exception as e:
            status = False
            result = []
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.w('EXC', iMessage)
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            result = []
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return


    async def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                docId = ObjectId(self.request.arguments['id'][0].decode())
            except Exception as e:
                code = 4100
                message = 'Invalid ID'
                raise Exception
            # TODO: this need to be moved in a global class, from here
            profileQ = self.profile.find(
                    {
                        'closed': False,
                        'entityId': self.entityId,
                        'accountId': self.accountId,
                        'applicationId': self.applicationId
                    },
                    {
                        '_id': 1
                    },
                    limit=1
                )
            profile = []
            async for i in profileQ:
                profile.append(i)

            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                appQ = self.applications.find(
                        {
                            '_id': self.applicationId
                        },
                        {
                            '_id': 1,
                            'apiId': 1
                        },
                        limit=1
                )
                app = []
                async for i in appQ:
                        app.append(i)

                if len(app):
                    self.apiId = app[0]['apiId']
                    if app[0]['apiId'] == 502022:# TODO: till here
                        bookDel = self.doc_list.update_one(
                                    {
                                        '_id':docId
                                    },
                                    {
                                    '$set':{
                                            'disabled':True
                                           }
                                    }
                                )
                        if bookDel['n']:
                            code = 2000
                            status = True
                            message = "Booking entry has been removed from active entries"
                        else:
                            code = 4210
                            status = False
                            message = 'This entry does not exist.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not authorized.'
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not authorized.'

        except Exception as e:
            status = False
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.w('EXC', iMessage)
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return
