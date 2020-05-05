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
class MtimeWebSubTouristHandler(cyclone.web.RequestHandler,
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
    imgWrite = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][18]['name']
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
                    Log.i(self.apiId)
                    if self.apiId in [ 402020, 402022]:
                        if self.apiId == 402020:

                            try:
                                firstName = self.request.arguments.get('firstName')
                                code, message = Validate.i(
                                    firstName,
                                    'First Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=180
                                )
                                if code != 4100:
                                    raise Exception
                            except:
                                if code == 4000:
                                    code = 4120
                                    message = 'Invalid Argument - [ First Name ].'
                                raise Exception

                            try:
                                lastName = self.request.arguments.get('lastName')
                                code, message = Validate.i(
                                    lastName,
                                    'Last Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=180
                                )
                                if code != 4100:
                                    raise Exception
                            except:
                                if code == 4000:
                                    code = 4120
                                    message = 'Invalid Argument - [ Last Name ].'
                                raise Exception

                            try:
                                address = self.request.arguments.get('address')
                                code, message = Validate.i(
                                    address,
                                    'Address',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=180
                                )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                template = 'Exception: {0}. Argument: {1!r}'
                                iMessage = template.format(type(e).__name__, e.args)
                                Log.w('EXC', iMessage)
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = exc_tb.tb_frame.f_code.co_filename
                                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))

                                if code == 4000:
                                    code = 4150
                                    message = 'Invalid Argument - [ Address ].'
                                raise Exception

                            try:
                                subkycId =  ObjectId(self.request.arguments.get('subkycId'))
                            except:
                                code = 4040
                                status = False
                                message = "Invalid Sub Tourist ID"
                                raise Exception
                            sub = yield self.subTourist.find(
                                    {
                                        '_id':subkycId
                                    }
                                )
                            if not len(sub):
                                code = 4060
                                status = False
                                message = "No Account Found"
                                raise Exception

                            accDetails = yield self.account.find(
                                        {
                                            '_id':self.accountId
                                        }
                                    )
                            if not len(accDetails):
                                status = False
                                code = 4235
                                message = "Invalid Account"
                                raise Exception
                            subTouristDetails = []
                            v = {
                                    'firstName':firstName,
                                    'lastName':lastName,
                                    'address':address
                                }
                            subTouristDetails.append(v)
                            kycUpdate = yield self.subTourist.update(
                                    {
                                        '_id':subkycId
                                    },
                                    {
                                    '$set': {
                                                'subTouristDetails':subTouristDetails,
                                                'expireAt': None
                                            }
                                    }
                                    )
                            if kycUpdate['n']:
                                code = 2000
                                status = True
                                message = "Verification has been submitted"
                                subUpdate = yield self.touristKyc.update(
                                            {
                                                'profileId':self.profileId
                                            },
                                            {
                                            '$inc': {
                                                        "subTouristCount":1
                                                    }
                                            }
                                        )
                            else:
                                code = 4068
                                status = False
                                message = "Invalid verification"
                        elif self.apiId == 402022:
                            statusValue = self.request.arguments.get('statusValue')
                            code,message = Validate.i(
                                            statusValue,
                                            'Status Value',
                                            dataType = bool,
                                        )
                            if code != 4100:
                                raise Exception
                            try:
                                kycId = ObjectId(self.request.arguments.get('kycId'))
                            except:
                                code = 4840
                                status = False
                                message = "Invalid KYC ID"
                            kycVerify = yield self.subTourist.update(
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
            proId = ObjectId(self.request.arguments['id'][0])
        except:
            proId = None
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
                    Log.i('api-ID',self.apiId)
                    if app[0]['apiId'] in [ 402020, 402022]: # TODO: till here

                        # For Service Provider GET
                        if self.apiId == 402020:
                            kycAcc  = yield self.subTourist.find(
                                            {
                                                'profileId':self.profileId,
                                                '$where': 'this.expireAt == null'
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
                            for res in kycAcc:
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
                                del res['_id']
                                result.append(res)
                            if len(result):
                                result.reverse()
                                status = True
                                code = 2000
                            else:
                                code = 4015
                                status = False
                                message = "No Data Found"
                        elif self.apiId == 402022:
                            kycAcc  = yield self.subTourist.find(
                                            {
                                                'profileId':proId,
                                                '$where': 'this.expireAt == null'
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
                            for res in kycAcc:
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
                                del res['_id']
                                result.append(res)
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
                                #idProofId = str(self.get_arguments('idProofType')[0])
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
                                #aLatitude = float(self.request.arguments['latitude'][0])
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
                                #aLongitude = float(self.request.arguments['longitude'][0])
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

                            #aTime = timeNow()
                            accDetails = yield self.account.find(
                                        {
                                            '_id':self.accountId
                                        }
                                    )
                            if not len(accDetails):
                                status = False
                                code = 4235
                                message = "Invalid registration"
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
                                Log.i(faceProofType)
                                message = 'Invalid File Type for Face Proof.'
                                code = 4011
                                raise Exception

                            aTime = aTime + 1
                            idTime = aTime
                            ocrData = {}
                            if str(idProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
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

                                mainFile = ''
                                # Converting to PNG
                                if str(idProofType) not in ['.png']:
                                    idProofType = '.png'
                                    fpx = fp + '/' + str(fName) + idProofType
                                    filepath.append(fpx)
                                    im = Image.open(fpm)
                                    im.save(fpx, 'PNG')
                                    os.system('rm ' + fpm)
                                    os.system('chmod 755 -R ' + fp + '*')
                                    mainFile = fpx
                                else:
                                    os.system('chmod 755 -R ' + fpm + '*')
                                    mainFile = fpm

                                # OCR CONVERTION BY GOOGLE_OCR
                                try:
                                    p = steps(mainFile)
                                    if 'front' in p['fileIdentified']:
                                        fName = p['name'].split(' ')
                                        ocrData['firstName'] = fName[0]
                                        ocrData['lastName'] = fName[1]
                                        ocrData['idNumber'] = p.get('idNumber')
                                        ocrData['dateOfBirth'] = p.get('dob')
                                        ocrData['gender'] = p.get('gender')
                                        ocrData['age'] = p.get('age')
                                    else:
                                        ocrData['address'] = p['address']
                                    Log.i(ocrData)
                                except Exception as e:
                                    Log.i(e)

                                '''
                                # OCR CONVERTION BY pytesseract
                                try:
                                    import pytesseract
                                    a = pytesseract.image_to_string(Image.open(fpx))
                                    b = a.encode('utf-8')
                                    c = b.split()
                                    ocrData['firstName'] = c[0]
                                    ocrData['lastName'] = c[1]
                                except Exception as e:
                                    Log.i(e)
                                '''
                            else:
                                message = 'Invalid File Type for Id Proof.'
                                code = 4011
                                raise Exception

                            subkyccount = yield self.subTourist.count(
                                            {
                                                'profileId':self.profileId
                                            }
                                        )
                            if subkyccount == 0:
                                primary = True
                            else:
                                primary = False
                            try:
                                subkycId = yield self.subTourist.insert(
                                        {
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
                                                            ],
                                                'location': [
                                                            {
                                                                'type': 'Point',
                                                                'coordinates': [aLongitude, aLatitude]
                                                            }
                                                        ],
                                                'expireAt': dtime.now(),
                                                'profileId':self.profileId,
                                                'entityId':self.entityId,
                                                'submitRequest':[0,1],
                                                'verified':True,
                                                'disabled':False,
                                                'primary':primary
                                        }
                                    )
                                imgUpdate = yield self.imgWrite.insert(
                                        {
                                                'subkycId':subkycId,
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
                                                            ],
                                                'location': [
                                                            {
                                                                'type': 'Point',
                                                                'coordinates': [aLongitude, aLatitude]
                                                            }
                                                        ],
                                                'expireAt': dtime.now(),
                                                'profileId':self.profileId,
                                                'entityId':self.entityId,
                                                'submitRequest':[0,1],
                                                'verified':True,
                                                'disabled':False,
                                                'primary':primary
                                        }
                                    )
                                result.append(str(subkycId))
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

                                uPath = uPath + str(subkycId) + '/'
                                if not os.path.exists(uPath):
                                    os.system('mkdir -p ' + uPath)
                                    os.system('chmod 755 -R ' + uPath)
                                for i in filepath:
                                    os.system('mv ' + i + ' ' + uPath)

                                Log.d(uPath)
                                os.system('chmod 755 -R ' + uPath + '*')

                                result.append(ocrData)
                                code = 2000
                                status = True
                                message = "Documents has been submitted."
                            except:
                                code = 2000
                                status = False
                                message = "Invalid process"
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
    def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            '''
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body)
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            '''
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
                            kycId = ObjectId(self.get_arguments('id')[0])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception
                        kycDel = yield self.subTourist.remove(
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

