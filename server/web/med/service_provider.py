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
class MedServiceProviderHandler(cyclone.web.RequestHandler,
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



    fu = FileUtil()

    @defer.inlineCallbacks
    def post(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:


            # GET FILES FROM REQUEST BODY
            '''
            try:
                liveProof = self.request.files['liveProof'][0]
            except Exception as e:
                code = 4100
                message = 'Need a Live Video Proof.'
                raise Exception
            '''


            try:
                id1Proof = self.request.files['id1Proof'][0]
            except Exception as e:
                code = 4102
                message = 'Please upload the image of the relevant document'
                raise Exception

            try:
                id2Proof = self.request.files['id2Proof'][0]
            except Exception as e:
                code = 4102
                message = 'Please upload the image of the relevant declaration'
                raise Exception

            print self.entityId
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
                            try:
                                serviceId = ObjectId(self.request.arguments['serviceId'][0])
                            except:
                                code = 4565
                                status = False
                                message = "Invalid Argument - [ ServiceId ]"
                                raise Exception
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
                                message = 'Invalid Argument - [ Address ].'
                                raise Exception

                            filepath = []

                            id1ProofType = id1Proof['content_type']
                            id1ProofType = yield mimetypes.guess_extension(
                                            id1ProofType,
                                            strict=True
                                )

                            id2ProofType = id2Proof['content_type']
                            id2ProofType = yield mimetypes.guess_extension(
                                            id2ProofType,
                                            strict=True
                                )

                            aTime = timeNow()
                            id1Time = aTime
                            if str(id1ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                fName = id1Time
                                fRaw = id1Proof['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + id1ProofType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                                mainFile = ''
                                # Converting to PNG
                                if str(id1ProofType) not in ['.png']:
                                    id1ProofType = '.png'
                                    fpx = fp + '/' + str(fName) + id1ProofType
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

                            aTime = aTime + 1
                            id2Time = aTime
                            if str(id2ProofType) in [ '.png','.jpeg', '.jpg', '.jpe']:
                                fName = id2Time
                                fRaw = id2Proof['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + id2ProofType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                                mainFile = ''
                                # Converting to PNG
                                if str(id2ProofType) not in ['.png']:
                                    id2ProofType = '.png'
                                    fpx = fp + '/' + str(fName) + id2ProofType
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
                                message = 'Invalid File Type for Declaration.'
                                code = 4011
                                raise Exception

                            serviceFind = yield self.serviceList.find(
                                            {
                                                '_id':serviceId,
                                                'disabled':False
                                            }
                                        )
                            if not len(serviceFind):
                                code = 4775
                                status = False
                                message = "Invalid Service"
                                raise Exception

                            serFind = yield self.serviceProvider.find(
                                            {
                                                'profileId':self.profileId,
                                                'serviceId':serviceId,
                                                'disabled':False
                                            }
                                        )

                            if len(serFind) :
                                serId = serFind[0]['_id']
                                accConfId = yield self.serviceProvider.update(
                                            {
                                                'entityId':self.entityId,
                                                'profileId':self.profileId,
                                                'serviceId':serviceId
                                            },
                                            {
                                            '$set':{
                                                        'address':address,
                                                        'docUpload':[
                                                                        {
                                                                            'time':id1Time,
                                                                            'mimeType':id1ProofType
                                                                        }
                                                                    ],
                                                        'declarationUpload':[
                                                                                {
                                                                                    'time':id2Time,
                                                                                    'mimeType':id2ProofType
                                                                                }
                                                                            ],
                                                    }
                                            }
                                        )
                                if accConfId['n']:
                                    code = 2000
                                    status = True
                                    message = "Service Information has been submitted"
                                else:
                                    code = 4885
                                    status = False
                                    message = "Service Information could not be submitted."


                            else:
                                serId = yield self.serviceProvider.insert(
                                        {
                                            'entityId':self.entityId,
                                            'profileId':self.profileId,
                                            'serviceId':serviceId,
                                            'disabled': False,
                                            'verified':False,
                                            'submitRequest':[0,1],
                                            'address':address,
                                            'docUpload':[
                                                            {
                                                                'time':id1Time,
                                                                'mimeType':id1ProofType
                                                            }
                                                        ],
                                            'declarationUpload':[
                                                                    {
                                                                        'time':id2Time,
                                                                        'mimeType':id2ProofType
                                                                    }
                                                                ]
                                        }
                                    )

                                code = 2000
                                status = True
                                message = "Service Information is submitted."

                            # Moving Temp dir to booking dir
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

        '''
        try:
            profileId = ObjectId(self.request.arguments['id'][0])
        except:
            profileId = None
        '''

        try:
            serId = ObjectId(self.request.arguments['id'][0])
        except:
            serId = None

        try:
            method = int(self.request.arguments['method'][0])
        except:
            method = None

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
                            if serId:
                                serProf = yield self.serviceProvider.find(
                                            {
                                                '_id':serId,
                                                'profileId':self.profileId
                                            }
                                        )
                            else:
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
                                            'docUpload':res['docUpload'],
                                            'declaration':res['declarationUpload'],
                                            'verified':res['verified']
                                        }
                                    if len(res['docUpload']):
                                        for docx in res['docUpload']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/service_provider/' \
                                                        + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                    if len(res['declarationUpload']):
                                        for docx in res['declarationUpload']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/service_provider/' \
                                                        + str(res['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                    result.append(v)
                            else:
                                code = 4655
                                status = False
                                message = "No Data Found"
                        elif self.apiId == 502022:
                            # For Admin GET
                            if serId:
                                serProf = yield self.serviceProvider.find(
                                            {
                                                '_id': serId,
                                                'disabled': False,
                                            },
                                            {
                                                '_id':1,
                                                'docUpload':1,
                                                'declarationUpload':1
                                            }
                                        )
                                if len(serProf):
                                    if len(serProf[0]['docUpload']):
                                        for docx in serProf[0]['docUpload']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/service_provider/' \
                                                        + str(serProf[0]['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                    if len(serProf[0]['declarationUpload']):
                                        for docx in serProf[0]['declarationUpload']:
                                            docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(self.entityId) + '/service_provider/' \
                                                        + str(serProf[0]['_id']) + '/' + str(docx['time']) + docx['mimeType']
                                    serProf[0]['id'] = str(serProf[0]['_id'])
                                    del serProf[0]['_id']
                                    result.append(serProf)
                                else:
                                    code = 4555
                                    status = False
                                    message = "No Data Found"
                            else:
                                serProf = yield self.serviceProvider.find(
                                            {
                                                'disabled': False,
                                            },
                                            {
                                                '_id': 1,
                                                'profileId':1,
                                                'disabled':1,
                                                'serviceId':1,
                                                'verified':1,
                                                'address':1,
                                                'docUpload':1,
                                                'declarationUpload':1
                                            }
                                        )
                                for res in serProf:
                                    service = yield self.serviceList.find(
                                                {
                                                    '_id':res['serviceId']
                                                }
                                            )
                                    serviceName = service[0]['serNameEnglish']
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
                                        regNum = accFind[0]['contact'][0]['value'] - 910000000000
                                    else:
                                        regNum = None
                                    v = {
                                            'registeredPhoneNum':regNum,
                                            'fullName' : accFind[0]['firstName'] + ' ' + accFind[0]['lastName'],
                                            'serviceId':str(res['serviceId']),
                                            'serviceName':serviceName,
                                            'disabled':res['disabled'],
                                            'verified':res['verified'],
                                            'serviceProfileId':str(res['profileId']),
                                            'address':res['address'],
                                            'docUpload':res['docUpload'],
                                            'declarationUpload':res['declarationUpload'],
                                            'id':str(res['_id'])
                                        }
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

