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
class MtimeWebAccTouristHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('GET','POST','PUT')

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
    touristBook = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][19]['name']
                ]

    fu = FileUtil()

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''

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
                        if self.apiId == 402021:
                            try:
                                pNum = int(self.request.arguments['pNum'][0])
                            except:
                                code = 4040
                                message = 'Invalid Phone Number'
                                raise Exception

                            accFind = yield self.account.find(
                                        {
                                            'contact.0.value':pNum
                                        },
                                        {
                                            '_id': 1,
                                            'firstName': 1,
                                            'lastName': 1,
                                            'contact': 1
                                        },
                                        limit=1
                                )
                            if not len(accFind):
                                status = False
                                code = 4550
                                message = "No Account found"
                                raise Exception
                            proFind = yield self.profile.find(
                                        {
                                            'accountId': accFind[0]['_id'],
                                            'entityId': self.entityId,
                                            'applicationId': ObjectId('5e5611bcb0c34f3bb9c2cd36')
                                        }
                                    )
                            if not len(proFind):
                                status = False
                                code = 4560
                                message = "No Account found"
                                raise Exception
                            touMem = yield self.subTourist.find(
                                        {
                                            'profileId':proFind[0]['_id'],
                                            '$where': 'this.subTouristDetails != null'
                                        },
                                        {
                                            '_id': 1,
                                            'verified':1,
                                            'disabled':1,
                                            'primary':1,
                                            'subTouristDetails':1,
                                            'documents':1,
                                            'faceProof':1,
                                            'location':1,
                                            'submitRequest':1
                                        }
                                    )
                            if not len(touMem):
                                status = False
                                code = 4570
                                message = "No tourist member found"
                                raise Exception
                            for res in touMem:
                                for docx in res['documents']:
                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                            + str(self.entityId) + '/tourist_kyc/' \
                                            + 'subtourist/' + str(res['_id']) \
                                            + '/' + str(docx['time']) + docx['mimeType']
                                for docx in res['faceProof']:
                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                            + str(self.entityId) + '/tourist_kyc/' \
                                            + 'subtourist/' + str(res['_id']) \
                                            + '/' + str(docx['time']) + docx['mimeType']
                                res['id'] = str(res['_id'])
                                res['touristProfile'] = str(proFind[0]['_id'])
                                del res['_id']
                                result.append(res)

                            accFind[0]['_id'] = str(accFind[0]['_id'])
                            accFind[0]['profileId'] = str(proFind[0]['_id'])
                            result = [
                                        {
                                            'account': accFind[0],
                                            'members': result
                                        }
                                    ]
                            status = True
                            code = 2000
                            message = "List of tourist members"
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
                        if self.apiId == 402021:
                            touMem = self.request.arguments.get('touristMembers')
                            if not len(touMem):
                                code = 4760
                                status = False
                                message = "No Tourist Added"
                                raise Exception
                            try:
                                touristId = ObjectId(self.request.arguments.get('touristId'))
                            except:
                                code = 4770
                                status = False
                                message = "Invalid Tourist Id"
                                raise Exception
                            touCount = len(touMem)
                            touPro = yield self.profile.find(
                                            {
                                                '_id':touristId
                                            }
                                        )
                            if not len(touPro):
                                code = 4780
                                status = False
                                message = "Invalid Account"
                                raise Exception
                            touristDetails = []
                            for resId in touMem:
                                touAcc = yield self.subTourist.find(
                                        {
                                            '_id':ObjectId(resId)
                                        },
                                        {
                                            '_id':1,
                                            'subTouristDetails':1,
                                            'faceProof':1,
                                            'documents':1,
                                            'primary':1
                                        }
                                    )
                                v = {
                                        'id':str(touAcc[0]['_id']),
                                        'firstName':touAcc[0]['subTouristDetails'][0]['firstName'],
                                        'lastName':touAcc[0]['subTouristDetails'][0]['lastName'],
                                        'address':touAcc[0]['subTouristDetails'][0]['address'],
                                        'documents':touAcc[0]['documents'],
                                        'faceProof':touAcc[0]['faceProof'],
                                        'liveProof':[],
                                        'note':[],
                                        'primary':touAcc[0]['primary']
                                    }
                                touristDetails.append(v)

                            bookingId = yield self.touristBook.insert(
                                    {
                                        'touristCount':touCount,
                                        'touristDetails':touristDetails,
                                        'disabled':False,
                                        'providerDetails':[
                                                            {
                                                                'id':self.profileId,
                                                                'accountId':self.accountId
                                                            }
                                                        ],
                                        "entityId" : self.entityId,
                                        "sendSmsCounter":0,
                                        "activity" : [
                                                        {
                                                            "id" : 0,
                                                            "time": timeNow()
                                                        }
                                                    ],
                                        "location":[],
                                        'touristId':touristId
                                    }
                                )
                            result.append(str(bookingId))
                            code = 2000
                            status = True
                            message = "Booking Initiated"
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
                liveProof = self.request.files['liveProof'][0]
            except Exception as e:
                code = 4100
                message = 'Need a live video proof.'
                raise Exception
            try:
                bookingId = ObjectId(self.request.arguments['bookingId'][0])
            except:
                code == 4310
                message = 'Invalid Argument - [ Booking Id ].'
                raise Exception
            try:
                subId = ObjectId(self.request.arguments['subId'][0])
            except:
                code == 4320
                message = 'Invalid Argument - [ Subtourist Id ].'
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
                        if self.apiId == 402021:
                            priTou = yield self.touristBook.find(
                                        {
                                            '_id':bookingId

                                        }
                                    )
                            if not len(priTou):
                                code = 4620
                                status = False
                                message = "Invalid Booking"
                                raise Exception

                            filepath = []
                            liveProofType = liveProof['content_type']
                            liveProofType = yield mimetypes.guess_extension(
                                                liveProofType,
                                                strict=True
                                            )
                            liveTime = timeNow()
                            if str(liveProofType) in ['.mp4']:
                                fName = liveTime
                                fRaw = liveProof['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + liveProofType
                                filepath.append(fpm)
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                            else:
                                message = 'Invalid File Type for Video Proof.'
                                code = 4040
                                raise Exception

                            subUpdate = yield self.touristBook.update(
                                        {
                                            '_id':bookingId,
                                            'touristDetails.id': str(subId)
                                        },
                                        {
                                        '$set':{
                                                'touristDetails.$.liveProof': [
                                                                                {
                                                                                    'time':liveTime,
                                                                                    'mimeType':liveProofType
                                                                                }
                                                                            ]
                                                },
                                        '$inc': {
                                                    'touristCount' : -1,
                                                }
                                        }

                                    )
                            if subUpdate['n']:
                                result.append(str(bookingId))
                                code = 2000
                                status = True
                                message = "Live Proof has been added"

                                uPath = self.fu.uploads + '/' + str(self.entityId)
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)
                                uPath = uPath + '/tourist_kyc'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)
                                uPath = uPath + '/subtourist/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)
                                uPath = uPath + str(subId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)
                                for i in filepath:
                                    os.system('mv ' + i + ' ' + uPath)

                                Log.d(uPath)
                                os.system('chmod 755 -R ' + uPath + '*')

                            else:
                                code = 2002
                                status = False
                                message = "Invalid Booking"
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
