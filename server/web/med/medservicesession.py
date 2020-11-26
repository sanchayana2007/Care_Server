#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    1.  VtsVehicleHandler
        Type: Class
        Methods:
            A.GET:
                Get all vehicle  details under that entity
                Line: 39
            B.POST:
                Will create new row vehicles
                Line: 162
            C.PUT:
                Update Vehicle details on vehicles.
                Line: 335
            D:DELETE:
                Delete the Vehicle from Vehicles.
                Line: 523
'''

from __future__ import division
from lib import *
from PIL import Image
import requests
import http.client
import datetime

@xenSecureV1
class MedServiceSessionHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('GET','POST','PUT','DELETE')

    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]

    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]

    bookingCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][1]['name']
                ]

    vehicle = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][4]['name']
                ]

    vehicleType = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][2]['name']
                ]

    booking = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][10]['name']
                ]

    coupon = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][11]['name']
                ]
    testBooking = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][12]['name']
                ]
    touristKyc = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][16]['name']
                ]
    subTourist = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][17]['name']
                ]
    imgWrite = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][18]['name']
                ]
    serviceBook = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][0]['name']
                ]
    serviceList = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][1]['name']
                ]
    cancelFee = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][2]['name']
                ]

    fu = FileUtil()


    @defer.inlineCallbacks
    def put(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                bookingId = ObjectId(self.request.arguments['id'][0])
            except:
                code = 4855
                status = False
                message = "Invalid booking ID"
                raise Exception
            # TODO: this need to be moved in a global class, from here
	    profile = yield self.profile.find(
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
            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                app = yield self.applications.find(
                            {
                                '_id': self.applicationId
                            },
                            {
                                '_id': 1,
                                'apiId': 1
                            },
                            limit=1
                        )
                if len(app):
                    self.apiId = app[0]['apiId']
                    Log.i(self.apiId)
                    if self.apiId in [ 502020, 502022, 502021]:
                        if self.apiId == 502022 or self.apiId == 502021:

                            serBook = yield self.serviceBook.find(
                                        {
                                            '_id':bookingId
                                        }
                                    )
                            if not len(serBook):
                                code = 4060
                                message = "Invalid Booking"
                                raise Exception
                            phoneNumber = serBook[0]['accountDetails'][0]['contact'][0]['value']
                            # TODO: Country code hard coded
                            phoneNumber = str(phoneNumber - 910000000000)
                            Log.i('Customer Phone Number', phoneNumber)

                            serList = yield self.serviceList.find(
                                        {
                                            '_id':serBook[0]['serviceId']
                                        }
                                    )
                            if not len(serList):
                                code = 4060
                                message = "Invalid Service"
                                raise Exception
                            if serBook[0]['stage'] == 'accepted':
                                if serBook[0]['session_remaining'] <= 0:
                                    code = 4565
                                    status = False
                                    message = "Invalid Session Update"
                                    raise Exception
                                if serBook[0]['session_remaining'] == 1:
                                    serBookUpdate = yield self.serviceBook.update(
                                                    {
                                                        '_id':bookingId
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
                                    else:
                                        code = 4555
                                        status = False
                                        message = "Session could not be updated."
                                        raise Exception
                                else:
                                    serBookUpdate = yield self.serviceBook.update(
                                                    {
                                                        '_id':bookingId
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
                                code = 4070
                                status = False
                                message = "Invalid Session Update"
                                raise Exception
                        elif self.apiId == 502020:
                            try:
                                bookingId = ObjectId(self.request.arguments.get('bookingId'))
                            except:
                                code = 4050
                                message = "Invalid Booking Id"
                                raise Exception
                            serBook = yield self.serviceBook.find(
                                        {
                                            '_id':bookingId
                                        }
                                    )
                            if not len(serBook):
                                code = 4060
                                message = "Invalid Booking"
                                raise Exception
                            phoneNumber = serBook[0]['accountDetails'][0]['contact'][0]['value']
                            # TODO: Country code hard coded
                            phoneNumber = str(phoneNumber - 910000000000)
                            Log.i('Customer Phone Number', phoneNumber)

                            serList = yield self.serviceList.find(
                                        {
                                            '_id':serBook[0]['serviceId']
                                        }
                                    )
                            if not len(serList):
                                code = 4060
                                message = "Invalid Service"
                                raise Exception

                            serName = serList[0]['serNameEnglish']

                            serUpdate = yield self.serviceBook.update(
                                        {
                                            '_id':bookingId
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

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''
        try:
            bookingId = self.request.arguments['id'][0]
        except:
            bookingId = None
        try:
            # TODO: this need to be moved in a global class
            profile = yield self.profile.find(
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
            if len(profile):
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                app = yield self.applications.find(
                            {
                                '_id': self.applicationId
                            },
                            {
                                '_id': 0,
                                'apiId': 1
                            },
                            limit=1
                        )
                if len(app):
                    self.apiId = app[0]['apiId']
                    if app[0]['apiId'] in [ 502020, 502022]: # TODO: till here
                        if self.apiId == 502022:
                            if bookingId == None:
                                res = yield self.serviceBook.find(
                                        {
                                            'entityId':self.entityId,
                                            'disabled':False
                                        }
                                    )
                            else:
                                try:
                                    bookingId = ObjectId(bookingId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid Booking Id"
                                res = yield self.serviceBook.find(
                                        {
                                            'entityId':self.entityId,
                                            '_id':bookingId,
                                            'disabled':False
                                        }
                                    )
                            if len(res):
                                for bookInfo in res:
                                    v = {
                                            '_id':str(bookInfo['_id']),
                                            'accountDetails':bookInfo['accountDetails'],
                                            'booktime':bookInfo['booktime'],
                                            'stage':bookInfo['stage'],
                                            'session':bookInfo['session'],
                                            'disabled':bookInfo['disabled'],
                                            'requestedTime':bookInfo['requestedTime'],
                                            'comment':bookInfo['comment'],
                                            'logo':"https://medix.xlayer.in/uploads/default/logo.jpg",
                                            'address':'Ohzas,Banaras.'
                                        }
                                    try:
                                        if len(str(bookInfo['session_remaining'])) and bookInfo['stage'] in ['new','accepted']:
                                            v['session_remaining'] = bookInfo['session']
                                        else:
                                            v['session_remaining'] = bookInfo['session_remaining']
                                    except:
                                        v['session_remaining'] = 'N/A'
                                    serInfo = yield self.serviceList.find(
                                                {
                                                    '_id':bookInfo['serviceId']
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
                                    if bookInfo['session'] in [5,6,7,8,9,10]:
                                        discount = 0.1
                                    elif bookInfo['session'] in [11,12,13,14,15]:
                                        discount = 0.15
                                    elif bookInfo['session'] in [16,17,18,19,20]:
                                        discount = 0.2
                                    else:
                                        discount = 0
                                    try:
                                        if len(str(bookInfo['cancelFee'])):
                                            cancelFeeAmt = bookInfo['cancelFee']
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
                        elif self.apiId == 502020:
                            if bookingId == None:
                                print self.entityId
                                print self.profileId
                                res = yield self.serviceBook.find(
                                        {
                                            'entityId':self.entityId,
                                            'profileId':self.profileId
                                        }
                                    )
                            else:
                                try:
                                    bookingId = ObjectId(bookingId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid Booking Id"
                                res = yield self.serviceBook.find(
                                        {
                                            'entityId':self.entityId,
                                            'profileId':self.profileId,
                                            '_id':bookingId
                                        }
                                    )
                            if len(res):
                                for bookInfo in res:
                                    v = {
                                            '_id':str(bookInfo['_id']),
                                            'booktime':bookInfo['booktime'],
                                            'stage':bookInfo['stage'],
                                            'requestedTime':bookInfo['requestedTime'],
                                            'comment':bookInfo['comment']
                                        }
                                    serInfo = yield self.serviceList.find(
                                                {
                                                    '_id':bookInfo['serviceId']
                                                },
                                                {
                                                    '_id':0,
                                                    'serNameHindi':1,
                                                    'serNameEnglish':1,
                                                    'serCharges':1,
                                                    'serTADA':1,
                                                    'serTotal':1
                                                }
                                            )
                                    v['serviceDetails'] = serInfo
                                    result.append(v)
                                result.reverse()
                                code = 2000
                                status = True
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



    @defer.inlineCallbacks
    def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                bookingId = ObjectId(self.request.arguments['id'][0])
            except Exception as e:
                code = 4100
                message = 'Invalid ID'
                raise Exception
            # TODO: this need to be moved in a global class, from here
            profile = yield self.profile.find(
                            {
                                'closed': False,
                                'accountId': self.accountId,
                                'entityId': self.entityId,
                                'applicationId': self.applicationId
                            },
                            limit=1
                        )
            if len(profile):
                app = yield self.applications.find(
                            {
                                '_id': profile[0]['applicationId']
                            },
                            limit=1
                        )
                if len(app):
                    if app[0]['apiId'] == 502022:# TODO: till here
                        bookDel = yield self.serviceBook.update(
                                    {
                                        '_id':bookingId
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

