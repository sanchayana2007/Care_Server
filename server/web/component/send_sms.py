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
import datetime
import requests
import http.client

@xenSecureV1
class MedServiceSendSMSHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('POST','GET')

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
    serviceBook = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][0]['name']
                ]
    serviceList = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][1]['name']
                ]

    fu = FileUtil()

    @defer.inlineCallbacks
    def post(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # GET JSON FROM REQUEST BODY
                self.request.arguments = json.loads(self.request.body)

            except Exception as e:
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                code = 4100
                message = 'Expected Request Type FormData.'
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
		    if self.apiId in [ 502022, 502020,502021 ]:
                        if self.apiId == 502022: #TODO: till here
                            contacts = []
                            manual = self.request.arguments.get('manual')
                            if manual == None:
                                manual = False
                            if type(manual) != bool:
                                code = 7483
                                status = False
                                message = "Invalid argument - ['manual']"
                                raise Exception
                            smsMessage = self.request.arguments.get('smsMessage')
                            if smsMessage == None or smsMessage == "":
                                code = 8943
                                status = False
                                message = "SMS Message cannot be empty"
                                raise Exception
                            if len(smsMessage) > 159:
                                code = 6728
                                status = False
                                message = "SMS exceeds 159 Characters"
                                raise Exception
                            if manual == True:
                                numbers = self.request.arguments.get('numbers')
                                if numbers == None or numbers == "":
                                    code = 8942
                                    status = False
                                    message = "There are no numbers added"
                                    raise Exception
                                numbers = (numbers.split (","))
                                for i in numbers:
                                    contacts.append(int(i))

                            else:
                                serviceType = self.request.arguments.get('serviceType')
                                if serviceType == None:
                                    code = 7842
                                    status = False
                                    message = "Please select the receiver type in the dropdown"
                                    raise Exception
                                if serviceType not in [0,1]:
                                    code = 5848
                                    status = False
                                    message = "Invalid Argument - ['serviceType']"
                                if serviceType == 0:
                                    applicationFind = yield self.applications.find(
                                                            {
                                                                'apiId':502020
                                                            }
                                                        )
                                elif serviceType == 1:
                                    applicationFind = yield self.applications.find(
                                                            {
                                                                'apiId':502021
                                                            }
                                                        )
                                if not len(applicationFind):
                                    code = 7873
                                    status = False
                                    message = "Application Not Found. Please contact Support"
                                    raise Exception
                                proFind = yield self.profile.find(
                                                            {
                                                                'entityId':self.entityId,
                                                                'applicationId':applicationFind[0]['_id']
                                                            }
                                                        )
                                if len(proFind):
                                    for res in proFind:
                                        accFind = yield self.account.find(
                                                                            {
                                                                                '_id':res['accountId']
                                                                            }
                                                                        )
                                        if len(accFind):
                                            pNum = int(accFind[0]['contact'][0]['value'] - 910000000000)
                                            contacts.append(pNum)
                                if not len(contacts):
                                    code = 5478
                                    status = False
                                    message = "No Contacts Found"
                                    raise Exception
                            #To bring to format of numbers accepted by bulksmsgateway
                            contacts = str(contacts).replace(' ','')
                            contacts = contacts.replace('[','')
                            contacts = contacts.replace(']','')

                            Log.i("Contacts:",contacts)
                            Log.i("smsMessage:",smsMessage)
                            if True:
                                URL = "https://login.bulksmsgateway.in/sendmessage.php"
                                PARAMS = {
                                            'user':'Xlayer technologies',
                                            'password':'Xlayer@920',
                                            'mobile':contacts,
                                            'message':smsMessage,
                                            'sender':'XLAYER',
                                            'type':'203'
                                        }
                                r = requests.get(url = URL, params = PARAMS)
                                data = r.json()
                                Log.i(data)
                                if data['status'] == 'success':
                                    code = 2000
                                    status = True
                                    message = "SMS has been successfully sent"
                                else:
                                    code = 8493
                                    status = False
                                    message = "SMS could not be sent. Please contact Support"
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
		    if self.apiId in [ 502022, 502020,502021 ]:
                        if self.apiId == 502022: #TODO: till here
                            URL = "https://login.bulksmsgateway.in/userbalance.php"
                            PARAMS = {
                                        'user':'Xlayer technologies',
                                        'password':'Xlayer@920',
                                        'type':'203'
                                    }
                            try:
                                r = requests.get(url = URL, params = PARAMS)
                                data = r.json()
                                Log.i(data)
                                if data.get('remainingcredits') != None:
                                    smsCredits = data['remainingcredits']
                                else:
                                    smsCredits = "Data not available"
                            except:
                                smsCredits = "Data not available"
                            v = {"smsCredits":smsCredits}
                            result.append(v)
                            code = 2000
                            status = True
                            message = "SMS CREDITS DATA"
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

