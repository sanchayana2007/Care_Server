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


from lib import *
from PIL import Image

@xenSecureV1
class DriverPictureProfileHandler(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('PUT')

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

    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][6]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]

    vehicleCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][1]['name']
                ]

    vehicleSubCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][2]['name']
                ]

    fu = FileUtil()

    @defer.inlineCallbacks
    def put(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # TODO: this need to be moved in a global class, from here
            profile = yield self.profile.find(
                            {
                                'accountId': self.accountId,
                                'applicationId': self.applicationId,
                                'entityId': self.entityId
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
                                'apiId': 1
                            },
                            limit=1
                        )
                if len(app):
                    if app[0]['apiId'] == 20216: # TODO: till here
                        try:
                            driverId = ObjectId(self.get_arguments('id')[0])
                        except:
                            code = 4290
                            message = 'Invalid Driver Id'
                            raise Exception
                        driverAccount = []
                        driverProfile = yield self.profile.find(
                                            {
                                                '_id': driverId
                                            },
                                            {
                                                '_id': 1,
                                                'accountId': 1
                                            },
                                            limit=1
                                        )
                        if not len(driverProfile):
                            code = 4291
                            message = 'Driver not found.'
                            raise Exception

                        uFile = self.request.files['file'][0]
                        fType = uFile['content_type']
                        fType = yield mimetypes.guess_extension(
                                fType,
                                strict=True
                            )
                        if str(fType) in ['.jpeg', '.jpg', '.png', '.jpe']:
                            fName = 'profile'
                            fRaw = uFile['body']
                            '''
                                Saving Profile Picture of driver
                                TODO: will moved to mongodb
                            '''
                            fp = self.fu.uploads + str(self.entityId) + '/profile/' + str(driverId)
                            if not os.path.exists(fp):
                                Log.i('DRV-Profile', 'Creating Directories')
                                os.system('mkdir -p ' + fp)
                            fpm = fp + '/' + fName + fType
                            fpx = fp + '/' + fName
                            # Saving File
                            fh = open(fpm, 'w')
                            fh.write(fRaw)
                            fh.close()
                            '''
                                Converting to PNG from JPEG, JPG
                            '''
                            im = Image.open(fpm)
                            # Removing old file
                            os.system('rm ' + fpm)
                            fpn = fpx + '.png'
                            im.save(fpn, 'PNG')
                            # setting up permissions
                            os.system('chmod 755 -R ' + self.fu.uploads + '*')
                            fpn2 = fpn
                            fpp = fpn2.replace(self.fu.uploads, self.fu.uploadsPath)
                            result.append(fpp)
                            status = True
                            code = 2000
                            message = 'Driver Profile picture has been updated.'
                        else:
                            message = 'Invalid File Type.'
                            code = 4010
                    else:
                        self.set_status(401)
                        code = 4003
                        message = 'You are not Authorized.'
                else:
                    self.set_status(401)
                    code = 4003
                    message = 'You are not Authorized.'
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not Authorized.'
        except Exception as e:
            status = False
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error, Please Contact the Support Team.'
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
            message = 'Internal Error, Please Contact the Support Team.'
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

