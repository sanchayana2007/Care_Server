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
class MtimeWebTouristVerifyHandler(cyclone.web.RequestHandler,
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
    touristKyc = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][16]['name']
                ]
    subTourist = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][17]['name']
                ]

    fu = FileUtil()

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            kycId = ObjectId(self.request.arguments['id'][0])
        except:
            kycId = None

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
                    if app[0]['apiId'] in [ 402020, 402022]: # TODO: till here

                        # For Service Provider GET
                        if self.apiId == 402020:
                            kycAcc  = yield self.touristKyc.find(
                                            {
                                                'profileId':self.profileId,
                                            },
                                            {
                                                '_id': 1,
                                                'disabled':1,
                                                'verified':1,
                                                'touristDetails':1,
                                                'documents':1,
                                                'faceProof':1,
                                                'submitRequest':1
                                            }
                                        )
                            if len(kycAcc):
                                for docx in kycAcc[0]['documents']:
                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                + str(self.entityId) + '/tourist_kyc/' \
                                                + str(kycAcc[0]['_id']) \
                                                + '/' + str(docx['time']) + docx['mimeType']
                                for docx in kycAcc[0]['faceProof']:
                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                + str(self.entityId) + '/tourist_kyc/' \
                                                + str(kycAcc[0]['_id']) \
                                                + '/' + str(docx['time']) + docx['mimeType']

                                kycAcc[0]['id'] = str(kycAcc[0]['_id'])
                                del kycAcc[0]['_id']
                                result.append(kycAcc[0])

                                status = True
                                code = 2000
                            else:
                                code = 4015
                                status = False
                                message = "Kyc Not Found"
                        elif self.apiId == 402022:
                            if kycId == None:
                                kycAcc  = yield self.touristKyc.find(
                                            {
                                                'entityId':self.entityId,
                                            },
                                            {
                                                '_id': 1,
                                                'profileId':1,
                                                'verified':1,
                                                'touristDetails':1,
                                                'submitRequest':1,
                                                'location':1
                                            }
                                        )
                                if len(kycAcc):
                                    for res in kycAcc:
                                        v = {
                                                'profileId':str(res['profileId']),
                                                'id':str(res['_id']),
                                                'verified':res['verified'],
                                                'touristDetails':res['touristDetails'],
                                                'submitRequest':res['submitRequest'],
                                                'location':res['location']
                                            }
                                        result.append(v)
                                    code = 2000
                                    status = True
                                else:
                                    code = 4000
                                    status = False
                                    message = "No data found"
                            else:
                                kycAcc  = yield self.touristKyc.find(
                                            {
                                                '_id':kycId,
                                            },
                                            {
                                                '_id': 1,
                                                'profileId':1,
                                                'verified':1,
                                                'disabled':1,
                                                'touristDetails':1,
                                                'documents':1,
                                                'faceProof':1,
                                                'location':1,
                                                'submitRequest':1
                                            }
                                        )
                                if len(kycAcc[0]['documents']) and len(kycAcc[0]['documents']):
                                    for docx in kycAcc[0]['documents']:
                                        docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                + str(self.entityId) + '/tourist_kyc/' \
                                                + str(kycAcc[0]['_id']) \
                                                + '/' + str(docx['time']) + docx['mimeType']
                                    for docx in kycAcc[0]['faceProof']:
                                        docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                + str(self.entityId) + '/tourist_kyc/' \
                                                + str(kycAcc[0]['_id']) \
                                                + '/' + str(docx['time']) + docx['mimeType']
                                if len(kycAcc):
                                        kycAcc[0]['id'] = str(kycAcc[0]['_id'])
                                        kycAcc[0]['profile'] = str(kycAcc[0]['profileId'])
                                        del kycAcc[0]['_id']
                                        del kycAcc[0]['profileId']
                                        result.append(kycAcc[0])
                                if len(result):
                                    status = True
                                    code = 2000
                                else:
                                    code = 4015
                                    status = False
                                    message = "No Data Found"
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
                faceProof = self.request.files['faceProof'][0]
            except Exception as e:
                code = 4100
                message = 'Need a facial Proof.'
                raise Exception

            try:
                idProof = self.request.files['idProof'][0]
            except Exception as e:
                code = 4102
                message = 'Need a Id Proof.'
                raise Exception

            try:
                addressProof = self.request.files['addressProof'][0]
            except Exception as e:
                code = 4103
                message = 'Need a Address Proof.'
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
                    if self.apiId in [ 402020, 402022]:
                        if self.apiId == 402020:
                            try:
                                kycId = ObjectId(self.get_arguments('kycId')[0])
                            except:
                                code = 4650
                                status = False
                                message = "Invalid KYC"
                                raise Exception

                            kycAcc = yield self.touristKyc.find(
                                        {
                                            '_id':kycId
                                        }
                                    )
                            if not len(kycAcc):
                                code = 4650
                                status = False
                                message = "Invalid KYC"
                                raise Exception

                            try:
                                addressProofId = str(self.get_arguments('addressProofType')[0])
                                code, message = Validate.i(
                                        addressProofId,
                                        'Address Proof Type',
                                        #maxNumber=90,
                                        #minNumber=-90
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ Address Proof Type ].'
                                raise Exception


                            try:
                                idProofId = str(self.get_arguments('idProofType')[0])
                                code, message = Validate.i(
                                        idProofId,
                                        'Id Proof Type',
                                        #maxNumber=90,
                                        #minNumber=-90
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ Id Proof Type ].'
                                raise Exception

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
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ longitude ].'
                                raise Exception

                            try:
                                aTime = long(self.get_arguments('time')[0])
                                code, message = Validate.i(
                                        aTime,
                                        'Time',
                                        #maxNumber=timeNow() + 3600000,
                                        #minNumber=-90
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ time ].'
                                raise Exception

                            accDetails = yield self.account.find(
                                        {
                                            '_id':self.accountId
                                        }
                                    )
                            if not len(accDetails):
                                status = False
                                code = 4235
                                message = "Invalid KYC verification"
                                raise Exception
                            filepath = []
                            faceProofType = faceProof['content_type']
                            faceProofType = yield mimetypes.guess_extension(
                                    faceProofType,
                                    strict=True
                                )
                            idProofType = idProof['content_type']
                            idProofType = yield mimetypes.guess_extension(
                                    idProofType,
                                    strict=True
                                )

                            addressProofType = addressProof['content_type']
                            addressProofType = yield mimetypes.guess_extension(
                                    addressProofType,
                                    strict=True
                                )

                            faceTime = aTime
                            if str(faceProofType) in ['.jpeg', '.jpg', '.jpe']:
                                fName = faceTime
                                fRaw = faceProof['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + faceProofType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                                # Converting to PNG
                                faceProofType = '.png'
                                fpx = fp + '/' + str(fName) + faceProofType
                                filepath.append(fpx)
                                im = Image.open(fpm)
                                im.save(fpx, 'PNG')
                                os.system('rm ' + fpm)
                                os.system('chmod 755 -R ' + fp + '*')

                            else:
                                message = 'Invalid File Type for Face Proof.'
                                code = 4011
                                raise Exception

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

                            else:
                                message = 'Invalid File Type for Id Proof.'
                                code = 4011
                                raise Exception

                            aTime = aTime + 1
                            addressTime = aTime
                            if str(addressProofType) in ['.jpeg', '.jpg', '.jpe']:
                                fName = addressTime
                                fRaw = addressProof['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + addressProofType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                                # Coverting to PNG
                                addressProofType = '.png'
                                fpx = fp + '/' + str(fName) + addressProofType
                                filepath.append(fpx)
                               	im = Image.open(fpm)
                            	im.save(fpx, 'PNG')
                                os.system('rm ' + fpm)
                                os.system('chmod 755 -R ' + fp + '*')
                            else:
                                message = 'Invalid File Type for Address Proof.'
                                code = 4011
                                raise Exception
                            try:
                                kycUpdate = yield self.touristKyc.update(
                                        {
                                            '_id':kycId
                                        },
                                        {
                                        '$set': {
                                                'faceProof':[
                                                                {
                                                                'time':faceTime,
                                                                'mimeType':faceProofType
                                                                }
                                                            ],
                                                'documents':[
                                                                {
                                                                'id':1,
                                                                'time':idTime,
                                                                'mimeType':idProofType,
                                                                'idType':idProofId
                                                                },
                                                                {
                                                                'id':2,
                                                                'time':addressTime,
                                                                'mimeType':addressProofType,
                                                                'idType':addressProofId
                                                                },
                                                            ],
                                                'location': [
                                                            {
                                                                'type': 'Point',
                                                                'coordinates': [aLongitude, aLatitude]
                                                            }
                                                        ],
                                                'subTouristCount':0,
                                                'submitRequest':[0,1],
                                        }
                                        }
                                    )
                                result.append(str(kycId))
                                uPath = self.fu.uploads + '/' + str(self.entityId)
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + '/tourist_kyc/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)

                                uPath = uPath + str(kycId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)
                                for i in filepath:
                                    os.system('mv ' + i + ' ' + uPath)

                                Log.d(uPath)
                                os.system('chmod 755 -R ' + uPath + '*')

                                code = 2000
                                status = True
                                message = "Tourist KYC verification has been submitted."
                            except:
                                code = 2000
                                status = False
                                message = "Invalid KYC verification"
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
                                                    'sub_members':0,
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
                            try:
                                kycId = ObjectId(self.request.arguments.get('kycId'))
                            except:
                                code = 4840
                                status = False
                                message = "Invalid KYC ID"
                            kycVerify = yield self.touristKyc.update(
                                            {
                                                '_id':kycId
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
                            if kycVerify['n']:
                                code = 2000
                                status = True
                                if statusValue:
                                    message = "KYC Verification has been accepted."
                                else:
                                    message = "KYC Verification has been declined."
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
                kycId = ObjectId(self.request.arguments['id'][0])
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
                    if app[0]['apiId'] == 402022:# TODO: till here
                        kycFind = yield self.touristKyc.find(
                                    {
                                        '_id':kycId
                                    }
                                )
                        if len(kycFind):
                            subkycDel = yield self.subTourist.remove(
                                    {
                                        'profileId':kycFind[0]['profileId']
                                    }
                                )
                        kycDel = yield self.touristKyc.remove(
                                    {
                                        '_id':kycId
                                    }
                                )
                        if kycDel['n']:
                            code = 2000
                            status = True
                            message = "KYC entry has been deleted."
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

