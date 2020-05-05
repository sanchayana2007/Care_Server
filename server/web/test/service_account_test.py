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

@xenSecureV1
class MtimeWebServiceAccountHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('GET', 'POST', 'DELETE','PUT')

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

    fu = FileUtil()

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            profileId = ObjectId(self.request.arguments['id'][0])
        except:
            profileId = None

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
                    if app[0]['apiId'] in [ 402021, 402022]: # TODO: till here

                        # For Service Provider GET
                        if self.apiId == 402021:
                            serviceAcc  = yield self.serviceAccount.find(
                                            {
                                                'profileId':self.profileId,
                                            },
                                            {
                                                '_id': 1,
                                                'hotelName':1,
                                                'hotelAddress':1,
                                                'submitRequest':1,
                                                'GSTin':1,
                                                'verified':1,
                                                'location':1,
                                                'media':1
                                            }
                                        )
                            for docx in serviceAcc[0]['media']:
                                docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                + 'service_media/' + str(serviceAcc[0]['_id'])\
                                                + '/' + str(docx['time']) + docx['mimeType']
                            if len(serviceAcc):
                                    serviceAcc[0]['id'] = str(serviceAcc[0]['_id'])
                                    del serviceAcc[0]['_id']
                                    result.append(serviceAcc[0])
                            if len(result):
                                status = True
                                code = 2000
                            else:
                                code = 4015
                                status = False
                                message = "Account Not Found"
                        elif self.apiId == 402022:
                            # For Admin GET
                            accProvApp = yield self.applications.find(
                                        {
                                            'apiId': 402021
                                        },
                                        {
                                            '_id': 1
                                        },
                                        limit=1
                                    )
                            if not len(accProvApp):
                                code = 5210
                                message = 'Application Not Found.'
                                raise Exception

                            if profileId:
                                accProv = yield self.profile.find(
                                        {
                                            '_id': profileId
                                        },
                                        {
                                            '_id': 1,
                                            'accountId': 1
                                        }
                                    )
                            else:
                                accProv = yield self.profile.find(
                                        {
                                            'entityId': self.entityId,
                                            'applicationId': accProvApp[0]['_id']
                                        },
                                        {
                                            '_id': 1,
                                            'accountId': 1
                                        }
                                    )

                            if not len(accProv):
                                code = 4110
                                message = 'Provider List is Empty.'
                                raise Exception

                            for val in accProv:
                                serProf = []
                                if profileId:
                                    orgAcc = yield self.account.find(
                                                {
                                                    '_id': val['accountId']
                                                },
                                                {
                                                    '_id': 0,
                                                    'firstName': 1,
                                                    'lastName': 1,
                                                    'contact': 1
                                                }
                                            )
                                    if len(orgAcc):
                                        print(orgAcc)
                                        serProf = yield self.serviceAccount.find(
                                            {
                                                'profileId': val['_id']
                                            },
                                            {
                                                '_id': 1,
                                                'hotelName':1,
                                                'hotelAddress':1,
                                                'GSTin':1,
                                                'submitRequest':1,
                                                'verified': 1,
                                                'disabled': 1,
                                                'location':1
                                            },
                                            limit=1
                                        )
                                        serProf[0]['accountDetails'] = orgAcc
                                else:
                                    serProf = yield self.serviceAccount.find(
                                            {
                                                'profileId': val['_id']
                                            },
                                            {
                                                '_id': 1,
                                                'hotelName':1,
                                                'hotelAddress':1,
                                                'GSTin':1,
                                                'submitRequest':1,
                                                'verified': 1,
                                                'disabled': 1,
                                                'location':1
                                            },
                                            limit=1
                                        )
                                if len(serProf):
                                    serProf[0]['serviceAccountId'] = str(serProf[0]['_id'])
                                    serProf[0]['id'] = str(val['_id'])
                                    del serProf[0]['_id']
                                    result.append(serProf[0])

			    if len(result):
                                code = 2000
			        status = True
                            else:
                                code = 4121
                                status = False
                                message = "No data Found"
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
                    if self.apiId in [ 402021, 402022]:
                        hotelName = self.request.arguments.get('hotelName')
                        code,message = Validate.i(
                                            hotelName,
                                            'Hotel Name',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 50
                                        )
                        if code != 4100:
                            raise Exception

                        hotelAddress = self.request.arguments.get('hotelAddress')
                        code,message = Validate.i(
                                            hotelAddress,
                                            'Hotel Address',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 300
                                        )
                        if code != 4100:
                            raise Exception

                        GSTin = self.request.arguments.get('GSTin')
                        code,message = Validate.i(
                                            GSTin,
                                            'GSTin',
                                            notEmpty = True,
                                            dataType = unicode,
                                            noSpecial = True,
                                            maxLength = 50
                                        )
                        if code != 4100:
                            raise Exception

                        try:
                            aLatitude = float(self.request.arguments.get('latitude'))
                            code, message = Validate.i(
                                            aLatitude,
                                            'latitude',
                                            maxNumber=90,
                                            minNumber=-90
                                        )

                            if code != 4100:
                                raise Exception

                        except Exception as e:
                            code = 4210
                            message = 'Invalid Argument - [ latitude ].'
                            raise Exception

                        try:
                            aLongitude = float(self.request.arguments.get('longitude'))
                            code, message = Validate.i(
                                            aLongitude,
                                            'longitude',
                                            maxNumber=180,
                                            minNumber=-180
                                        )

                            if code != 4100:
                                raise Exception

                        except Exception as e:
                            code = 4210
                            message = 'Invalid Argument - [ longitude ].'
                            raise Exception



                        #For requesting approval from Provider end
                        if self.apiId == 402021:
                            try:
                                accConfId = yield self.serviceAccount.insert(
                                        {
                                            'entityId':self.entityId,
                                            'profileId':self.profileId,
                                            'disabled': False,
                                            'verified': False,
                                            'location': [
                                                            {
                                                                'type': 'Point',
                                                                'coordinates': [aLongitude, aLatitude]
                                                            }
                                                        ],
                                            'submitRequest':[0,1],
                                            'hotelName': hotelName,
                                            'hotelAddress': hotelAddress,
                                            'GSTin': GSTin,
                                            'media':[]
                                        }
                                    )
                                result.append(str(accConfId))
                                code = 2000
                                status = True
                                message = "Service Account has been submitted."
                            except:
                                code = 4013
                                status = False
                                message = "Your Service Account is already submitted."
                        elif self.apiId == 402022:

                            applicationId = self.request.arguments.get('applicationId')
                            approvId = yield self.applications.find(
                                    {
                                            "applicationId" : applicationId
                                    }
                                )
                            if not len(approvId):
                                code = 5050
                                message = 'Invalid Application'
                                raise Exception
                            firstName = self.request.arguments.get('firstName')
                            code,message = Validate.i(
                                            firstName,
                                            'First Name',
                                            notEmpty = True,
                                            dataType = unicode,
                                            noSpecial = True,
                                            maxLength = 50
                                        )
                            if code != 4100:
                                raise Exception
                            lastName = self.request.arguments.get('lastName')
                            code,message = Validate.i(
                                            lastName,
                                            'Last Name',
                                            notEmpty = True,
                                            dataType = unicode,
                                            noSpecial = True,
                                            maxLength = 50
                                        )
                            if code != 4100:
                                raise Exception
                            phoneNumber = self.request.arguments.get('phoneNumber')
                            code,message = Validate.i(
                                            phoneNumber,
                                            'Phone Number',
                                            notEmpty = True,
                                            dataType = int,
                                            minNumber=911000000000,
                                            maxNumber=999999999999
                                        )

                            if code != 4100:
                                raise Exception
                            email = self.request.arguments.get('email')
                            code,message = Validate.i(
                                            email,
                                            'Email',
                                            inputType='email',
                                            dataType = unicode,
                                            maxLength = 50,
                                        )
                            if code != 4100:
                                raise Exception
                            pAccount = yield self.account.find(
                                        {
                                            'contact.0.value': phoneNumber
                                        }
                                    )
                            if len(pAccount):
                                profile = yield self.profile.find(
                                            {
                                                'accountId':pAccount[0]['_id']
                                            }
                                        )
                                if len(profile):
                                    pid = profile[0]['_id']
                                else:
                                    code = 5010
                                    status = False
                                    message = 'Internal Error Please Contact the Support Team.'
                            else:
                                accountData =   {
                                                    'firstName': firstName,
                                                    'lastName': lastName,
                                                    'contact':  [
                                                                    {
                                                                        'verified': False,
                                                                        'value': phoneNumber
                                                                    },
                                                                ]
                                                    }
                                if email != None:
                                    accountData['contact'].append(
                                            {
                                                'verified': False,
                                            }
                                        )
                                accountId = yield self.account.insert(accountData)
                                profileId = yield self.profile.insert(
                                                    {
                                                        'active': False,
                                                        'locked': False,
                                                        'closed': False,
                                                        'entityId': self.entityId,
                                                        'accountId': accountId,
                                                        'applicationId':approvId[0]['_id'],
                                                        'data':[]
                                                    }
                                                )
                                pid = profileId
                            try:
                                accConfId = yield self.serviceAccount.insert(
                                    {
                                        'entityId':self.entityId,
                                        'profileId':pid,
                                        'disabled': False,
                                        'verified': False,
                                        'submitRequest':[1,0],
                                        'hotelName': hotelName,
                                        'hotelAddress': hotelAddress,
                                        'GSTin': GSTin
                                    }
                                )
                                result.append(str(accConfId))
                                code = 2000
                                status = True
                                message = "Service Account has been submitted."
                            except:
                                code = 4013
                                status = False
                                message = "Your Service Account is already submitted."
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
    def put(self):

        status = False
        code = 4000
        result = []
        message = ''



        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body)
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
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
                                'disabled': False,
                                '_id': self.applicationId
                            },
                            {
                                'apiId': 1
                            },
                            limit=1
                        )
                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [402022,402021]:
                        if self.apiId in [ 402021 ]: # TODO: till here
                            accConfId = ObjectId(self.request.arguments.get('accConfId'))
                            hotelName = self.request.arguments.get('hotelName')
                            code,message = Validate.i(
                                            hotelName,
                                            'Hotel Name',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 50
                                        )
                            if code != 4100:
                                raise Exception

                            hotelAddress = self.request.arguments.get('hotelAddress')
                            code,message = Validate.i(
                                            hotelAddress,
                                            'Hotel Address',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 300
                                        )
                            if code != 4100:
                                raise Exception

                            GSTin = self.request.arguments.get('GSTin')
                            code,message = Validate.i(
                                            GSTin,
                                            'GSTin',
                                            notEmpty = True,
                                            dataType = unicode,
                                            noSpecial = True,
                                            maxLength = 50
                                        )

                            if code != 4100:
                                raise Exception
                            try:
                                aLatitude = self.request.arguments.get('latitude')
                                code, message = Validate.i(
                                            aLatitude,
                                            'latitude',
                                            maxNumber=90,
                                            minNumber=-90
                                        )

                                if code != 4100:
                                    raise Exception

                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ latitude ].'
                                raise Exception

                            try:
                                aLongitude = self.request.arguments.get('longitude')
                                code, message = Validate.i(
                                            aLongitude,
                                            'longitude',
                                            maxNumber=180,
                                            minNumber=-180
                                        )

                                if code != 4100:
                                    raise Exception

                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ longitude ].'
                                raise Exception
                            #TODO:: Need to verify max number of re-submissions
                            serUpdate = yield self.serviceAccount.update(
                                        {
                                            '_id':accConfId
                                            #'$where': 'this.submitRequest[1] < 5'
                                        },
                                        {
                                        '$set': {
                                                    'hotelName':hotelName,
                                                    'hotelAddress':hotelAddress,
                                                    'GSTin':GSTin,
                                                    'location': [
                                                                    {
                                                                        'type': 'Point',
                                                                    'coordinates': [aLongitude, aLatitude]
                                                                    }
                                                                ],
                                                },
                                        '$inc': {
                                                    'submitRequest.1':1
                                                },
                                        }
                                    )
                            if serUpdate['n']:
                                code = 2000
                                status = True
                                message = "Verification has been re-submitted"
                            else:
                                code = 4068
                                status = False
                                message = "You have exceeded the max number of retries for verification process"
                        elif self.apiId in [ 402022 ]: # TODO: till here
                            statusValue = self.request.arguments.get('statusValue')
                            code,message = Validate.i(
                                            statusValue,
                                            'Status Value',
                                            dataType = bool,
                                        )
                            if code != 4100:
                                raise Exception
                            #TODO::Need to send notication based on status
                            accConfId = self.request.arguments.get('accConfId')
                            accConfVerify = yield self.serviceAccount.update(
                                            {
                                                '_id':ObjectId(accConfId)
                                            },
                                            {
                                            '$set': {
                                                        'verified': statusValue,
                                                    },
                                            '$inc': {
                                                        'submitRequest.0':1
                                                    },
                                            }
                                        )
                            if accConfVerify['n']:
                                code = 2000
                                status = True
                                if statusValue:
                                    message = "Account details has been accepted."
                                else:
                                    message = "Account details has been declined."
                            else:
                                code = 2003
                                status = False
                                message = "Invalid verification request"

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

    @defer.inlineCallbacks
    def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body)
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
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
                    if app[0]['apiId'] == 402020: # TODO: till here
                        try:
                            vTypeId = ObjectId(self.request.arguments['id'])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception
                        updateResult = yield self.vehicle.find_and_modify(
                                    query = {
                                            '_id': vTypeId,
                                            'disabled': False,
                                            'entityId': self.entityId
                                        },
                                    update = {
                                        '$set': {
                                            'disabled': True
                                        }
                                    }
                            )
                        if updateResult:
                            status = True
                            code = 2000
                            message = 'Vehicle has been Disabled.'
                        else:
                            code = 4210
                            message = 'This vehicle does not exist.'
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

