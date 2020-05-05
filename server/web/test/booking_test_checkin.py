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
import random

@xenSecureV1
class MtimeWebTestBookingCinHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('POST', 'PUT')

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
    def post(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # GET FILES FROM REQUEST BODY
            try:
                liveProof = self.request.files['liveProof'][0]
            except Exception as e:
                code = 4100
                message = 'Need a Live Video Proof.'
                raise Exception

            try:
                idProof = self.request.files['idProof'][0]
            except Exception as e:
                code = 4102
                message = 'Need a Id Proof.'
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
		    if self.apiId in [ 402021, 30216, 20216 ]:
			if self.apiId == 402021: # TODO: till here
                            aLatitude = 22.5825182
                            aLongitude = 88.4386982
                            aTime = timeNow()
                            '''
                            try:
                                aLatitude = float(self.get_arguments('latitude')[0])
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
                                aLongitude = float(self.get_arguments('longitude')[0])
                                code, message = Validate.i(
                                    aLongitude,
                                    'longitude',
                                    maxNumber=180,
                                    minNumber=-180
                                )
                                if code != 4100:
                                    raise Exception
                            except:
                                code = 4310
                                message = 'Invalid Argument - [ longitude ].'
                                raise Exception

                            try:
                                aTime = int(self.get_arguments('time')[0])
                                code, message = Validate.i(
                                    aTime,
                                    'time',
                                    maxNumber=(timeNow() + 3600000000),
                                    minNumber=(timeNow() - 3600000000)
                                )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                Log.e(e)
                                code = 4410
                                message = 'Invalid Argument - [ time ].'
                                raise Exception
                            '''
                            filepath = []
                            liveProofType = liveProof['content_type']
                            liveProofType = yield mimetypes.guess_extension(
                                            liveProofType,
                                            strict=True
                                )

                            idProofType = idProof['content_type']
                            idProofType = yield mimetypes.guess_extension(
                                            idProofType,
                                            strict=True
                                )

                            aTime = aTime + 1
                            liveTime = aTime
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
                                message = 'Invalid File Type for Live Video Proof.'
                                code = 4010
                                raise Exception

                            ocrData = {}
                            aTime = aTime + 1
                            idTime = aTime
                            if str(idProofType) in ['.jpeg', '.jpg', '.jpe']:
                                fName = idTime
                                fRaw = idProof['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + idProofType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                                # Converting to PNG
                                idProofType = '.png'
                                fpx = fp + '/' + str(fName) + idProofType
                                filepath.append(fpx)
                                im = Image.open(fpm)
                                im.save(fpx, 'PNG')
                                os.system('rm ' + fpm)
                                os.system('chmod 755 -R ' + fp + '*')

                                # OCR CONVERTION
                                try:
                                    import pytesseract
                                    a = pytesseract.image_to_string(Image.open(fpx))
                                    b = a.encode('utf-8')
                                    c = b.split()
                                    ocrData['firstName'] = c[0]
                                    ocrData['lastName'] = c[1]
                                except Exception as e:
                                    Log.i(e)

                            else:
                                message = 'Invalid File Type for Id Proof.'
                                code = 4011
                                raise Exception

                            touId = random.randint(100000000000,999999999999)

                            #TODO::Need to give expired time.
                            bookingId = yield self.touristBook.insert(
                                        {
                                            'disabled':False,
                                            'entityId':self.entityId,
                                            'touristId':None,
                                            'providerDetails':
                                            [
                                                {
                                                    'id':self.profileId,
                                                    'accountId':self.accountId
                                                }
                                            ],
                                            'touristDetails':[
                                                {
                                                    'id':str(touId),
                                                    'note' : [ ],
                                                    'faceProof':[ ],
                                                    'primary' : True,

                                                    'liveProof':[
                                                                    {
                                                                        'time':liveTime,
                                                                        'mimeType':liveProofType
                                                                    }
                                                                ],
                                                    'documents':[
                                                                    {
                                                                        'id':1,
                                                                        'time':idTime,
                                                                        'mimeType':idProofType
                                                                    }
                                                                ],
                                                }
                                            ],
                                            'location': [
                                                {
                                                    'type': 'Point',
                                                    'coordinates': [aLongitude, aLatitude]
                                                }
                                            ],
                                            'activity': [
                                                            {
                                                                'id':0,
                                                                'time': aTime,
                                                            }
                                                        ],
                                            'touristCount' : 1,
                                            'sendSmsCounter': 0
                                        }
                                    )
                                # Moving Temp dir to booking dir
                            uPath = self.fu.uploads + '/' + str(self.entityId)
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)

                            uPath = uPath + '/tourist_kyc/'
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)

                            uPath = uPath + '/subtourist/'
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)

                            uPath = uPath + str(touId) + '/'
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)

                            for i in filepath:
                                os.system('mv ' + i + ' ' + uPath)

                            Log.d(uPath)

                            os.system('chmod 755 -R ' + uPath + '*')
                            result.append(
                                    {'bookingId': str(bookingId),
                                     'touristId': str(touId),
                                     'ocrData':ocrData
                                    }
                                    )
                            code = 2000
                            status = True
                            message = "Tourist Entry has been uploaded."
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
                    if self.apiId in [ 402020, 402021, 402022 ]: # TODO: till here
                        if self.apiId == 402021:
                            try:
                                bookingId = ObjectId(self.request.arguments.get('bookingId'))
                            except:
                                code = 4560
                                status = False
                                message = "Invalid Booking Id"
                                raise Exception

                            subtouristId = str(self.request.arguments.get('subtouristId'))
                            if len(subtouristId) != 12:
                                code = 4570
                                status = False
                                message = "Invalid Tourist Id"
                                raise Exception

                            cFirstName = self.request.arguments.get('firstName')
                            code,message = Validate.i(
                                            cFirstName,
                                            'First Name',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 50,
                                            noSpecial = True,
                                            noNumber = True
                                        )

                            if code != 4100:
                                raise Exception



                            cLastName = self.request.arguments.get('lastName')
                            code,message = Validate.i(
                                            cLastName,
                                            'Last Name',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 50,
                                            noSpecial = True,
                                            noNumber = True
                                        )

                            if code != 4100:
                                raise Exception

                            cAddress = self.request.arguments.get('address')
                            code,message = Validate.i(
                                            cAddress,
                                            'Address',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 1000,
                                        )

                            if code != 4100:
                                raise Exception

                            touDetailsUpdate = yield self.touristBook.update(
                                                                {
                                                                    '_id':bookingId,
                                                                    'touristDetails.id': str(subtouristId)
                                                                },
                                                                {
                                                                '$set': {
                                                                            'touristDetails.$.firstName': cFirstName,
                                                                            'touristDetails.$.lastname': cLastName,
                                                                            'touristDetails.$.address': cAddress,
                                                                        }
                                                                }
                                                    )
                            if touDetailsUpdate['n']:
                                result.append(str(bookingId))
                                code = 2000
                                status = True
                                message = "Tourist contact information has been updated"
                            else:
                                code = 2002
                                status = False
                                message = "Invalid Booking."

                        else:
                            code = 4003
                            self.set_status(401)
                            message = 'You are not Authorized'
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

