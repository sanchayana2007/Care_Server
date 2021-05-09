#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    1.  clinic_updater
        Type: Class
        This is used by App admin to modify , delete and Update any clinic details

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
                Delete the Doctor from list.
                Line: 523
'''

from __future__ import division
from PIL import Image
from ..lib.lib import *
import requests
import http.client
import datetime

@xenSecureV1
class Clinic_updater(tornado.web.RequestHandler):

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
    clinic_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][1]['name']
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
                        #Doc Clinic App doc addition req handling
                        if self.apiId == 502020:
                            Log.i('Clinic Post req', self.request.arguments)
                            clinicName = self.request.arguments.get('clinicname')
                            clinicLocation = self.request.arguments.get('cliniclocation')
                            clinicAddress = self.request.arguments.get('clinicaddress')
                            clinicpocPh = self.request.arguments.get('clinicpocph')
                            paymentId = self.request.arguments.get('paymentId')
                            clinicpaymentAddress = self.request.arguments.get('clinicpaymentaddress')



                            #Check the clinic info table and update the object id of there

                            clinicId = self.clinic_list.insert_one(
                                        {
                                            'clinicname':clinicName,
                                            'cliniclocation': clinicLocation,
                                            'clinicaddress': clinicAddress,
                                            'clinicpocph': clinicpocPh,
                                            'clinicpayment': paymentId,
                                            'clinicpaymentaddress': clinicpaymentAddress,
                                            'requestedTime':timeNow(),
                                            'comment':"Entry test "
                                        }
                                    )
                            if clinicId:
                                Log.i("clinicId inserted",clinicId)
                                code = 2000
                                message = "Doc is has been added"
                                status = True

                            else:
                                Log.i("clinicId not inserted")
                                code = 2000
                                message = "Error in Doc addition"
                                status = True

                        elif self.apiId == 502022:

                            code = 4003
                            status = False
                            message = "The App id dosent support clinic Updates "
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
    #To insert the Doctor data nd
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
                        #TODO : Change ths code to 502022
                        if self.apiId == 502020:
                            Log.i('Clinic PUT req', self.request.arguments)

                            '''
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

                            '''
                        elif self.apiId == 502022:
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

        #self.request.arguments =  json.loads(self.request.body.decode('utf-8'))
        try:
            areaId = int(self.request.arguments["aid"][0])
        except:
            areaId = None

        #Set the Doctor id if found in the request
        try:
            docId = str(self.request.arguments["did"][0].decode('utf-8'))
        except:
            docId = None

        #Set the Clinic id if found in the request
        try:
            clinicId = str(self.request.arguments["cid"][0].decode('utf-8'))
        except:
            clinicId = None

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
                        #Handle the Clinic Doc list get request
                        #Show only the listed doctor for that clinic
                        if self.apiId == 502022:
                            Log.i('APIID', self.apiId)
                            if clinicId == None:
                                code = 4050
                                status = False
                                message = "Clinic ID Cannot be Empty"
                            else:
                                try:
                                    docId = ObjectId(docId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid doc Id"
                                resQ = self.clinic_list.find(
                                        {
                                            'clinicid':clinicId,
                                        }
                                    )
                                res = []
                                async for i in resQ:
                                    res.append(i)
                            #Res is from clinic_list collections whatevr matches
                            if len(res):
                                for i in res:
                                    i["_id"]= str(i["_id"])
                                    result.append(i)
                                result.reverse()
                                code = 2000
                                status = True
                                message = "Doctors Found in Clinic"
                            else:
                                code = 4080
                                status = False
                                message = "No data found"

                        #Patient App Handling
                        elif self.apiId == 502020:
                            #Set the Area id if found in the request
                            Log.i('docId',docId)
                            Log.i('clinicId',clinicId)
                            #TODO : to check need of ObjectID check
                            if docId != None:
                                try:
                                    docId = ObjectId(docId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid docId Id"
                                    Log.i("Invalid Doc ID")

                            if clinicId != None:
                                try:
                                    clinicId = ObjectId(clinicId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid Clinic Id"
                                    Log.i("Invalid Clinet ID")

                            #Doc and clinic both are None show all Docs in all clinics
                            if docId == None and clinicId ==None:

                                #resQ = self.doc_list.find()
                                resQ = await self.doc_list.count_documents({})
                                res = []
                                Log.i('Count of Docs ', resQ)
                                resQ = self.doc_list.find({})
                                async for i in resQ:
                                    i["_id"]=str(i["_id"])
                                    res.append(i)
                                Log.i('result ', res)

                                for doc in res:
                                    v= {"id": int(doc["docid"]), "doc": str(doc["docname"]) }
                                    result.append(v)

                            #Show thw list of all clinic  in that doc id
                            elif docId != None and clinicId == None:
                                resQ = self.doc_list.find(
                                        {
                                        }
                                    )
                                result = []
                                async for i in resQ:
                                    i["_id"]= str(i["_id"])
                                    i["clinicid"]= str(i["clinicid"])
                                    result.append(i)

                            #Show thw list of all doc  in that clinic id
                            elif docId == None and clinicId != None:
                                resQ = self.doc_list.find(
                                        {
                                            'clinicid':clinicId
                                        }
                                    )
                                result = []
                                async for i in resQ:
                                    i["_id"]= str(i["_id"])
                                    i["clinicid"]= str(i["clinicid"])
                                    result.append(i)
                            #Clinic and doc both provided Show the doc associated with the clinic
                            else:
                                Log.i("docid object",docId)
                                Log.i("clinicid object",clinicId)
                                resDoc = self.doc_list.find(
                                        {
                                            "_id": docId

                                        }
                                    )

                                result = []

                                async for i in resDoc:
                                    i["_id"]= str(i["_id"])
                                    i["clinicid"]= str(i["clinicid"])
                                    Log.i("Result",i)
                                    result.append(i)


                            #Create the response
                            if len(result):
                                result.reverse()
                                code = 2000
                                status = True
                                message = "Doc List Found "
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
