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
import requests

@xenSecureV1
class MedServiceProviderV2Handler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('POST', 'PUT', 'GET', 'DELETE')

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
    serviceBook = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][0]['name']
                ]
    serviceList = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][1]['name']
                ]
    cancelFee = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][2]['name']
                ]
    serviceProvider = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][3]['name']
                ]
    pincode = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][5]['name']
                ]
    serviceProviderServices = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][6]['name']
                ]



    fu = FileUtil()

    @defer.inlineCallbacks
    def post(self):

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
		    if self.apiId in [ 502021]:
			if self.apiId == 502021: # TODO: till here
                            serProFind = yield self.serviceProvider.find(
                                            {
                                                'entityId':self.entityId,
                                                'profileId':self.profileId
                                            }
                                        )
                            if len(serProFind):
                                profilePicTime = serProFind[0]['profilePic'][0]['time']
                                documentTime = serProFind[0]['document'][0]['time']
                                declarationTime = serProFind[0]['declaration'][0]['time']
                                signatureTime = serProFind[0]['signature'][0]['time']
                                profilePicType = documentType = declarationType = signatureType = ".png"
                                serId = serProFind[0]['_id']
                            Log.i("serviceList in registration")
                            Log.i(self.request.arguments.get('serviceList'))
                            try:
                                serviceList = self.request.arguments.get('serviceList')
                            except:
                                code = 4565
                                status = False
                                message = "Missing Argument - [ serviceList ]"
                                raise Exception
                            serviceList = serviceList[0].replace("['","")
                            serviceList = serviceList.replace("']","")
                            serviceList = list(serviceList.split (","))
                            serviceList = list(dict.fromkeys(serviceList))
                            if type(serviceList) != list:
                                code = 7229
                                status = False
                                message = "Invalid Service List"
                                raise Exception
                            for i in serviceList:
                                serFind = yield self.serviceList.find(
                                                {
                                                    '_id':ObjectId(i),
                                                    'disabled':False
                                                }
                                            )
                                if not len(serFind):
                                    serFind = yield self.serviceList.find(
                                                {
                                                    '_id':ObjectId(i)
                                                }
                                            )
                                    if len(serFind):
                                        serviceName = serFind[0]['serNameEnglish']
                                    else:
                                        serviceName = ""
                                    code = 7280
                                    status = False
                                    message = "Invalid Service selected -" + serviceName
                                    raise Exception
                            try:
                                qualification = str(self.get_arguments('qualification')[0])
                                code, message = Validate.i(
                                        qualification,
                                        'qualification',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Missing Argument - [ Qualification ].'
                                raise Exception
                            try:
                                profilePic = self.request.files['profilePic'][0]
                            except:
                                if not len(serProFind):
                                    code = 4558
                                    status = False
                                    message = "Profile picture is missing"
                                    raise Exception
                                else:
                                    profilePic = None
                            try:
                                document = self.request.files['document'][0]
                            except:
                                if not len(serProFind):
                                    code = 4558
                                    status = False
                                    message = "Document is missing"
                                    raise Exception
                                else:
                                    document = None
                            try:
                                declaration = self.request.files['declaration'][0]
                            except:
                                if not len(serProFind):
                                    code = 4558
                                    status = False
                                    message = "Declaration is missing"
                                    raise Exception
                                else:
                                    declaration = None
                            try:
                                address = str(self.get_arguments('address')[0])
                                code, message = Validate.i(
                                        address,
                                        'address',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Missing Argument - [ Address ].'
                                raise Exception
                            try:
                                state = str(self.get_arguments('state')[0])
                                code, message = Validate.i(
                                        state,
                                        'state',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Missing Argument - [ state ].'
                                raise Exception
                            try:
                                district = str(self.get_arguments('district')[0])
                                code, message = Validate.i(
                                        district,
                                        'district',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Missing Argument - [ district ].'
                                raise Exception

                            try:
                                areaOfOperation = self.request.arguments.get('areaOfOperation')
                                code, message = Validate.i(
                                        areaOfOperation,
                                        'areaOfOperation',
                                    )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Missing Argument - [ areaOfOperation ].'
                                raise Exception
                            areaOfOperation = areaOfOperation[0].replace("['","")
                            areaOfOperation = areaOfOperation.replace("']","")
                            areaOfOperation = list(areaOfOperation.split (","))
                            terms = False
                            try:
                                terms = bool(self.get_arguments('terms')[0])
                            except:
                                code = 2196
                                status = False
                                message = "Missing Argument - [terms]"
                                raise Exception
                            if terms != True:
                                code = 5000
                                status = False
                                message = "Terms and Conditions must be accepted."
                                raise Exception

                            try:
                                signature = self.request.files['signature'][0]
                            except:
                                if not len(serProFind):
                                    code = 4558
                                    status = False
                                    message = "Signature is missing"
                                    raise Exception
                                else:
                                    signature = None

                            filepath = []
                            aTime = timeNow()
                            if profilePic:
                                profilePicType = profilePic['content_type']
                                profilePicType = yield mimetypes.guess_extension(
                                            profilePicType,
                                            strict=True
                                )
                                profilePicTime = aTime
                                if str(profilePicType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                    fName = profilePicTime
                                    fRaw = profilePic['body']
                                    fp = self.fu.tmpPath
                                    if not os.path.exists(fp):
                                        Log.i('DRV-Profile', 'Creating Directories')
                                        os.system('mkdir -p ' + fp)
                                    fpm = fp + '/' + str(fName) + profilePicType
                                    fh = open(fpm, 'w')
                                    fh.write(fRaw)
                                    fh.close()

                                    mainFile = ''
                                    # Converting to PNG
                                    if str(profilePicType) not in ['.png']:
                                        profilePicType = '.png'
                                        fpx = fp + '/' + str(fName) + profilePicType
                                        filepath.append(fpx)
                                        im = Image.open(fpm)
                                        im.save(fpx, 'PNG')
                                        os.system('rm ' + fpm)
                                        os.system('chmod 755 -R ' + fp + '*')
                                        mainFile = fpx
                                    else:
                                        filepath.append(fpm)
                                        os.system('chmod 755 -R ' + fpm + '*')
                                        mainFile = fpm
                                else:
                                    message = 'Invalid File Type for Profile Picture'
                                    code = 4011
                                    raise Exception
                            if document:
                                documentType = document['content_type']
                                documentType = yield mimetypes.guess_extension(
                                            documentType,
                                            strict=True
                                )
                                aTime = aTime + 1
                                documentTime = aTime
                                if str(documentType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                    fName = documentTime
                                    fRaw = document['body']
                                    fp = self.fu.tmpPath
                                    if not os.path.exists(fp):
                                        Log.i('DRV-Profile', 'Creating Directories')
                                        os.system('mkdir -p ' + fp)
                                    fpm = fp + '/' + str(fName) + documentType
                                    fh = open(fpm, 'w')
                                    fh.write(fRaw)
                                    fh.close()

                                    mainFile = ''
                                    # Converting to PNG
                                    if str(documentType) not in ['.png']:
                                        documentType = '.png'
                                        fpx = fp + '/' + str(fName) + documentType
                                        filepath.append(fpx)
                                        im = Image.open(fpm)
                                        im.save(fpx, 'PNG')
                                        os.system('rm ' + fpm)
                                        os.system('chmod 755 -R ' + fp + '*')
                                        mainFile = fpx
                                    else:
                                        filepath.append(fpm)
                                        os.system('chmod 755 -R ' + fpm + '*')
                                        mainFile = fpm
                                else:
                                    message = 'Invalid File Type for Document'
                                    code = 4011
                                    raise Exception
                            if declaration:
                                declarationType = declaration['content_type']
                                declarationType = yield mimetypes.guess_extension(
                                            declarationType,
                                            strict=True
                                )
                                aTime = aTime + 1
                                declarationTime = aTime
                                if str(declarationType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                    fName = declarationTime
                                    fRaw = declaration['body']
                                    fp = self.fu.tmpPath
                                    if not os.path.exists(fp):
                                        Log.i('DRV-Profile', 'Creating Directories')
                                        os.system('mkdir -p ' + fp)
                                    fpm = fp + '/' + str(fName) + declarationType
                                    fh = open(fpm, 'w')
                                    fh.write(fRaw)
                                    fh.close()

                                    mainFile = ''
                                    # Converting to PNG
                                    if str(declarationType) not in ['.png']:
                                        declarationType = '.png'
                                        fpx = fp + '/' + str(fName) + declarationType
                                        filepath.append(fpx)
                                        im = Image.open(fpm)
                                        im.save(fpx, 'PNG')
                                        os.system('rm ' + fpm)
                                        os.system('chmod 755 -R ' + fp + '*')
                                        mainFile = fpx
                                    else:
                                        filepath.append(fpm)
                                        os.system('chmod 755 -R ' + fpm + '*')
                                        mainFile = fpm
                                else:
                                    message = 'Invalid File Type for Declaration'
                                    code = 4011
                                    raise Exception
                            if signature:
                                signatureType = signature['content_type']
                                signatureType = yield mimetypes.guess_extension(
                                            signatureType,
                                            strict=True
                                )
                                aTime = aTime + 1
                                signatureTime = aTime
                                if str(signatureType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                    fName = signatureTime
                                    fRaw = signature['body']
                                    fp = self.fu.tmpPath
                                    if not os.path.exists(fp):
                                        Log.i('DRV-Profile', 'Creating Directories')
                                        os.system('mkdir -p ' + fp)
                                    fpm = fp + '/' + str(fName) + signatureType
                                    fh = open(fpm, 'w')
                                    fh.write(fRaw)
                                    fh.close()

                                    mainFile = ''
                                    # Converting to PNG
                                    if str(signatureType) not in ['.png']:
                                        signatureType = '.png'
                                        fpx = fp + '/' + str(fName) + signatureType
                                        filepath.append(fpx)
                                        im = Image.open(fpm)
                                        im.save(fpx, 'PNG')
                                        os.system('rm ' + fpm)
                                        os.system('chmod 755 -R ' + fp + '*')
                                        mainFile = fpx
                                    else:
                                        filepath.append(fpm)
                                        os.system('chmod 755 -R ' + fpm + '*')
                                        mainFile = fpm
                                else:
                                    message = 'Invalid File Type for Signature'
                                    code = 4011
                                    raise Exception

                            if not len(serProFind):
                                serId = yield self.serviceProvider.insert(
                                        {
                                            'entityId':self.entityId,
                                            'profileId':self.profileId,
                                            'serviceList':serviceList,
                                            'disabled': False,
                                            'verified':False,
                                            'submitRequest':[0,1],
                                            'address':address,
                                            'qualification':qualification,
                                            'state':state,
                                            'district':district,
                                            'areaOfOperation':areaOfOperation,
                                            'terms':terms,
                                            'profilePic':[
                                                            {
                                                                'time':profilePicTime,
                                                                'mimeType':profilePicType
                                                            }
                                                        ],
                                            'document':[
                                                            {
                                                                'time':documentTime,
                                                                'mimeType':documentType
                                                            }
                                                        ],
                                            'declaration':[
                                                            {
                                                                'time':declarationTime,
                                                                'mimeType':declarationType
                                                            }
                                                        ],
                                            'signature':[
                                                            {
                                                                'time':signatureTime,
                                                                'mimeType':signatureType
                                                            }
                                                        ],
                                        }
                                    )
                                if serId:
                                    for i in serviceList:
                                        serListProvider = yield self.serviceProviderServices.insert(
                                                    {
                                                        'profileId':self.profileId,
                                                        'entityId':self.entityId,
                                                        'serviceProviderId':serId,
                                                        'serviceId':ObjectId(i),
                                                        'status':None
                                                    }
                                                )
                                    uPath = self.fu.uploads + '/' + str(self.entityId)
                                    if not os.path.exists(uPath):
                                        os.system('mkdir -p ' + uPath)
                                        os.system('chmod 755 -R ' + uPath)

                                    uPath = uPath + '/service_provider/'
                                    if not os.path.exists(uPath):
                                        os.system('mkdir -p ' + uPath)
                                        os.system('chmod 755 -R ' + uPath)

                                    uPath = uPath + str(serId) + '/'
                                    if not os.path.exists(uPath):
                                        os.system('mkdir -p ' + uPath)
                                        os.system('chmod 755 -R ' + uPath)

                                    for i in filepath:
                                        os.system('mv ' + i + ' ' + uPath)
                                        Log.d(uPath)
                                    code = 2000
                                    status = True
                                    message = "Service Information is submitted."
                            else:
                                serUpdate = yield self.serviceProvider.update(
                                                {
                                                    'profileId':self.profileId,
                                                    'entityId':self.entityId
                                                },
                                                {
                                                '$set':{
                                                            'address':address,
                                                            'serviceList':serviceList,
                                                            'qualification':qualification,
                                                            'state':state,
                                                            'district':district,
                                                            'areaOfOperation':areaOfOperation,
                                                            'terms':terms,
                                                            'profilePic':[
                                                                {
                                                                    'time':profilePicTime,
                                                                    'mimeType':profilePicType
                                                                }
                                                            ],
                                                            'document':[
                                                                {
                                                                    'time':documentTime,
                                                                    'mimeType':documentType
                                                                }
                                                            ],
                                                            'declaration':[
                                                                {
                                                                    'time':declarationTime,
                                                                    'mimeType':declarationType
                                                                }
                                                            ],
                                                            'signature':[
                                                                {
                                                                    'time':signatureTime,
                                                                    'mimeType':signatureType
                                                                }
                                                            ],
                                                    }
                                                }
                                        )
                                if serUpdate['n']:
                                    serListFind = yield self.serviceProviderServices.find(
                                                        {
                                                            'profileId':self.profileId
                                                        }
                                                )
                                    serCount = []
                                    for res in serListFind:
                                        serCount.append(str(res['_id']))
                                        if str(res['_id']) not in serviceList:
                                            serRemove = yield self.serviceProviderServices.remove(
                                                        {
                                                            '_id':res['_id']
                                                        }
                                                    )
                                    for i in serviceList:
                                        if i not in serCount:
                                            serListProvider = yield self.serviceProviderServices.insert(
                                                    {
                                                        'profileId':self.profileId,
                                                        'entityId':self.entityId,
                                                        'serviceProviderId':serId,
                                                        'serviceId':ObjectId(i),
                                                        'status':None
                                                    }
                                                )
                                    if len(filepath):
                                        uPath = self.fu.uploads + '/' + str(self.entityId)
                                        if not os.path.exists(uPath):
                                            os.system('mkdir -p ' + uPath)
                                            os.system('chmod 755 -R ' + uPath)

                                        uPath = uPath + '/service_provider/'
                                        if not os.path.exists(uPath):
                                            os.system('mkdir -p ' + uPath)
                                            os.system('chmod 755 -R ' + uPath)

                                        uPath = uPath + str(serId) + '/'
                                        if not os.path.exists(uPath):
                                            os.system('mkdir -p ' + uPath)
                                            os.system('chmod 755 -R ' + uPath)

                                        for i in filepath:
                                            os.system('mv ' + i + ' ' + uPath)
                                            Log.d(uPath)
                                    code = 2000
                                    status = True
                                    message = "Service Information has been submitted"
                                else:
                                    code = 7382
                                    status = False
                                    message = "Service Information could not be submitted"
                                    raise Exception
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
                    if self.apiId in [502022,502021]:
                        if self.apiId in [ 502022 ]: # TODO: till here
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
                            accConfVerify = yield self.serviceProvider.update(
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
                                    message = "Service Provider has been accepted."
                                else:
                                    message = "Service Provider has been declined."
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
                serAccId = ObjectId(self.request.arguments['id'][0])
                print serAccId
            except:
                code = 4850
                status = False
                message = "Invalid Service Account ID"
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
                    if app[0]['apiId'] == 402022: # TODO: till here
                        updateResult = yield self.serviceAccount.update(
                                        {
                                            '_id': serAccId,
                                            'disabled': False,
                                            'entityId': self.entityId,
                                            'serviceType':1
                                        },
                                        {
                                        '$set': {
                                                    'disabled': True
                                                }
                                        }
                            )
                        print updateResult
                        if updateResult['n']:
                            status = True
                            code = 2000
                            message = 'Service Account has been removed'
                        else:
                            code = 4210
                            message = 'Service Account does not exist.'
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
                    if app[0]['apiId'] in [ 502021, 502022]: # TODO: till here

                        # For Service Provider GET
                        if self.apiId == 502021:
                            serProf = yield self.serviceProvider.find(
                                            {
                                                'profileId':self.profileId
                                            }
                                        )
                            if len(serProf):
                                for res in serProf:
                                    v = {
                                            '_id':str(res['_id']),
                                            'address':res['address'],
                                            'district':res['district'],
                                            'terms':res['terms'],
                                            'qualification':res['qualification'],
                                            'document':res['document'],
                                            'declaration':res['declaration'],
                                            'profilePic':res['profilePic'],
                                            'signature':res['signature'],
                                            'verified':res['verified'],
                                            'state':res['state'],
                                            'areaOfOperation':res['areaOfOperation']
                                        }
                                    if len(res['serviceList']):
                                        serviceListA = []
                                        for i in res['serviceList']:
                                            serviceFind = yield self.serviceList.find(
                                                            {
                                                                '_id':ObjectId(i),
                                                            }
                                                        )
                                            if len(serviceFind):
                                                b = {
                                                        'serviceId':i,
                                                        'serviceName':serviceFind[0]['serNameEnglish']
                                                    }
                                                serviceListA.append(b)
                                        v['serviceList'] = serviceListA
                                    '''
                                    if len(res['serviceList']):
                                        areaOfOperation = []
                                        for i in res['areaOfOperation']:
                                            pincodeFind = yield self.pincode.find(
                                                            {
                                                                'pincode':int(i),
                                                            }
                                                        )
                                            if len(pincodeFind):
                                                c = {
                                                        'pincode':i,
                                                        'placeName':pincodeFind[0]['placeName']
                                                    }
                                                areaOfOperation.append(c)
                                        v['areaOfOperation'] = areaOfOperation
                                    '''
                                    if len(res['document']):
                                        for docx in res['document']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/service_provider/' \
                                                        + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                    if len(res['declaration']):
                                        for docx in res['declaration']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/service_provider/' \
                                                        + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                    if len(res['profilePic']):
                                        for docx in res['profilePic']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/service_provider/' \
                                                        + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                    if len(res['signature']):
                                        for docx in res['signature']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/service_provider/' \
                                                        + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                    result.append(v)
                                    code = 2000
                                    status = True
                                    message = "Service Provider Information"
                            else:
                                code = 4655
                                status = False
                                message = "No Data Found"
                        elif self.apiId == 502022:
                            try:
                                verified = int(self.request.arguments['verified'][0])
                            except:
                                verified = None


                            if verified != None:
                                if  verified not in [0,1]:
                                    code = 4355
                                    status = False
                                    message = "Invalid Verification Status"
                                    raise Exception
                                if int(verified) == 0:
                                    verified = False
                                else:
                                    verified = True


                            try:
                                serviceId = ObjectId(self.request.arguments['serviceId'][0])
                            except:
                                serviceId = None
                            # For Admin GET
                            try:
                                serProId = ObjectId(self.request.arguments['serviceProviderId'][0])
                            except:
                                serProId = None
                            if serviceId == None:
                                if verified == None:
                                    serProf = yield self.serviceProvider.find(
                                                {
                                                    'disabled': False,
                                                },
                                                {
                                                    '_id': 1,
                                                    'address':1,
                                                    'district':1,
                                                    'profileId':1,
                                                    'qualification':1,
                                                    'disabled':1,
                                                    'verified':1,
                                                    'document':1,
                                                    'profilePic':1,
                                                    'declaration':1,
                                                    'signature':1
                                                }
                                            )
                                else:
                                    serProf = yield self.serviceProvider.find(
                                                {
                                                    'disabled': False,
                                                    'verified': verified
                                                },
                                                {
                                                    '_id': 1,
                                                    'address':1,
                                                    'district':1,
                                                    'qualification':1,
                                                    'profileId':1,
                                                    'disabled':1,
                                                    'serviceId':1,
                                                    'verified':1,
                                                    'document':1,
                                                    'declaration':1,
                                                    'profilePic':1,
                                                    'signature':1,
                                                }
                                            )

                            else:
                                if verified == None:
                                    serProf = yield self.serviceProvider.find(
                                            {
                                                'serviceId':serviceId,
                                                'disabled': False,
                                            },
                                            {
                                                '_id': 1,
                                                'address':1,
                                                'district':1,
                                                'qualification':1,
                                                'profileId':1,
                                                'disabled':1,
                                                'serviceId':1,
                                                'verified':1,
                                                'document':1,
                                                'declaration':1,
                                                'profilePic':1,
                                                'signature':1,
                                            }
                                        )
                                else:
                                    serProf = yield self.serviceProvider.find(
                                            {
                                                'serviceId':serviceId,
                                                'disabled': False,
                                                'verified':verified
                                            },
                                            {
                                                '_id': 1,
                                                'address':1,
                                                'district':1,
                                                'qualification':1,
                                                'profileId':1,
                                                'disabled':1,
                                                'serviceId':1,
                                                'verified':1,
                                                'document':1,
                                                'declaration':1,
                                                'profilePic':1,
                                                'signature':1,
                                            }
                                        )

                            for res in serProf:
                                proFind = yield self.profile.find(
                                            {
                                                '_id':res['profileId']
                                            }
                                        )
                                if len(proFind):
                                    accFind = yield self.account.find(
                                            {
                                                '_id':proFind[0]['accountId']
                                            }
                                        )
                                    if len(accFind):
                                        regNum = accFind[0]['contact'][0]['value'] - 910000000000
                                        v = {
                                                'registeredPhoneNum':regNum,
                                                'address':res['address'],
                                                'district':res['district'],
                                                'qualification':res['qualification'],
                                                'fullName' : accFind[0]['firstName'] + ' ' + accFind[0]['lastName'],
                                                'disabled':res['disabled'],
                                                'verified':res['verified'],
                                                'serviceProfileId':str(res['profileId']),
                                                'document':res['document'],
                                                'declaration':res['declaration'],
                                                'signature':res['signature'],
                                                'profilePic':res['profilePic'],
                                                'id':str(res['_id'])
                                            }
                                        if len(res['document']):
                                            for docx in res['document']:
                                                docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(self.entityId) + '/service_provider/' \
                                                    + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                        if len(res['declaration']):
                                            for docx in res['declaration']:
                                                docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(self.entityId) + '/service_provider/' \
                                                    + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                        if len(res['signature']):
                                            for docx in res['signature']:
                                                docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(self.entityId) + '/service_provider/' \
                                                    + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                        if len(res['profilePic']):
                                            for docx in res['profilePic']:
                                                docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(self.entityId) + '/service_provider/' \
                                                    + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                result.append(v)
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
                    if self.apiId in [502022,502021]:
                        if self.apiId in [ 502021 ]: # TODO: till here
                            code = 4755
                            status = False
                            message = "API not yet implemeted."
                            raise Exception
                        elif self.apiId in [ 502022 ]: # TODO: till here
                            statusValue = self.request.arguments.get('statusValue')
                            code,message = Validate.i(
                                            statusValue,
                                            'Status Value',
                                            dataType = bool,
                                        )
                            if code != 4100:
                                raise Exception
                            #TODO::Need to send notication based on status
                            accConfId = self.request.arguments.get('id')
                            accConfVerify = yield self.serviceProvider.update(
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
                                    message = "Service Account has been approved"
                                else:
                                    message = "Service Account has been declined."
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

