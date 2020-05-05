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
class MtimeWebServiceUpdateHandler(cyclone.web.RequestHandler,
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

    fu = FileUtil()

    @defer.inlineCallbacks
    def put(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # GET FILES FROM REQUEST BODY
            try:
                serviceMedia = self.request.files['serviceMedia'][0]
            except Exception as e:
                code = 4100
                message = 'Media file missing'
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
                            try:
                                serviceId = self.request.arguments['id'][0]
                                if not serviceId:
                                    raise Exception
                                else:
                                    serviceId = ObjectId(serviceId)
                            except:
                                code = 4050
                                status = False
                                message = "Invalid Service Id"
                                raise Exception
                            filepath = []
                            serviceMediaType = serviceMedia['content_type']
                            serviceMediaType = yield mimetypes.guess_extension(
                                            serviceMediaType,
                                            strict=True
                                )

                            if str(serviceMediaType) in ['.jpeg', '.jpg', '.png', '.jpe']:
                                fName = timeNow()
                                fRaw = serviceMedia['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('DRV-Profile', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + serviceMediaType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                                # Converting to PNG
                                serviceMediaType = '.png'
                                fpx = fp + '/' + str(fName) + serviceMediaType
                                filepath.append(fpx)
                                im = Image.open(fpm)
                                im.save(fpx, 'PNG')
                                os.system('rm ' + fpm)
                                os.system('chmod 755 -R ' + fp + '*')

                            else:
                                message = 'Invalid File Type'
                                code = 4011
                                raise Exception


                            serUpdate = yield self.serviceAccount.update(
                                        {
                                            '_id': serviceId
                                        },
                                        {
                                        '$push':
                                                {
                                                    'media':
                                                    {
                                                        'time':fName,
                                                        'mimeType':serviceMediaType
                                                    }
                                                }
                                        }
                                    )
                            if serUpdate['n']:
                                code = 2000
                                status = True
                                message = "Media has been uploaded"
                            else:
                                code = 4140
                                status = False
                                message = "Invalid upload"
                            # Moving Temp dir to service dir
                            uPath = self.fu.uploads + '/' + '/service_media/' + str(serviceId)
                            if not os.path.exists(uPath):
                                os.system('mkdir -p ' + uPath)
                                os.system('chmod 755 -R ' + uPath)

                            for i in filepath:
                                os.system('mv ' + i + ' ' + uPath)
                            os.system('chmod 755 -R ' + uPath + '*')

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
                            serviceId = ObjectId(self.request.arguments.get('serviceId'))
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
                            #TODO:: Need to verify max number of re-submissions
                            serUpdate = yield self.serviceAccount.update(
                                        {
                                            '_id':serviceId
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
                                                }
                                        }
                                    )
                            if serUpdate['n']:
                                code = 2000
                                status = True
                                message = "Service Account Information has been updated"
                            else:
                                code = 4068
                                status = False
                                message = "Invalid Service Account Update"
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

