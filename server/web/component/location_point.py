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
import base64
from PIL import Image

@xenSecureV1
class LocationPointHandler(cyclone.web.RequestHandler, MongoMixin):

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

    vehicleType = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][2]['name']
                ]

    serviceArea = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][5]['name']
                ]
    locationPoint = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][13]['name']
                ]

    fu = FileUtil()

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            locationId = ObjectId(self.request.arguments['id'][0])
        except:
            locationId = None

        try:
            # TODO: this need to be moved in a global class
            profile = yield self.profile.find(
                            {
                                'entityId': self.entityId,
                                'accountId': self.accountId,
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
                        if locationId:
                            locDetails = yield self.locationPoint.find(
                                            {
                                                'entityId': self.entityId,
                                                '_id':locationId
                                            },
                                            {
                                            '_id':1,
                                            'entityId':1,
                                            'locName':1,
                                            'locAddress':1,
                                            'location':1,
                                            'media':1
                                            }
                                        )
                            if len(locDetails):
                                for docx in locDetails[0]['media']:
                                    docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                    + str(locDetails[0]['entityId']) + '/locationPoint/' \
                                                    + str(locDetails[0]['_id']) + '/' + \
                                                    str(docx['time']) + docx['mimeType']
                                    locDetails[0]['id'] = str(locDetails[0]['_id'])
                                    locDetails[0]['entity'] = str(locDetails[0]['entityId'])
                                    del locDetails[0]['_id']
                                    del locDetails[0]['entityId']
                                    code = 2000
                                    status = True
                                result.append(locDetails[0])
                            else:
                                code = 4004
                                status = False
                                message = "No Data Found"
                        else:
                            locDetails = yield self.locationPoint.find(
                                            {
                                                'entityId': self.entityId,
                                            },
                                            {
                                            '_id':1,
                                            'entityId':1,
                                            'locName':1,
                                            'locAddress':1,
                                            'location':1,
                                            'media':1
                                            }
                                        )
                            if len(locDetails):
                                code = 2000
                                status = True
                                for docx in locDetails:
                                    docx['media'][0]['link'] = self.fu.serverUrl + '/uploads/' \
                                                        + str(docx['entityId']) + '/locationPoint/' \
                                                        + str(docx['_id']) + '/' + \
                                                        str(docx['media'][0]['time']) + docx['media'][0]['mimeType']
                                    docx['id'] = str(docx['_id'])
                                    docx['entity'] = str(docx['entityId'])
                                    del docx['_id']
                                    del docx['entityId']
                                    result.append(docx)
                            else:
                                code = 4004
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
                                'entityId': self.entityId,
                                'accountId': self.accountId,
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


                        locName = self.request.arguments.get('locName')
                        code, message = Validate.i(
                                    locName,
                                    'Location Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=40
                                )
                        if code != 4100:
                            raise Exception

                        locAddress = self.request.arguments.get('locAddress')
                        code, message = Validate.i(
                                    locAddress,
                                    'Location Address',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=200
                                )
                        if code != 4100:
                            raise Exception


                        media = self.request.arguments.get('media')
                        if not len(media):
                            code = 4000
                            status = False
                            message = "Media file missing"

                        filepath = []

                        img_dec = [x.strip() for x in media.split(',')]
                        extension = str(img_dec[0])
                        result = re.search('/(.*);', extension)
                        mediaType = str(result.group(1)).lower()

                        mediaTime = timeNow()
                        if mediaType in ['jpeg', 'jpg', 'jpe']:
                            fName = mediaTime
                            fp = self.fu.tmpPath
                            if not os.path.exists(fp):
                                Log.i('DRV-Profile', 'Creating Directories')
                                os.system('mkdir -p ' + fp)
                            fpm = fp + '/' + str(fName) + '.' + mediaType
                            decoded = base64.b64decode(img_dec[1])
                            filehandle = open(fpm,'w+b')
                            filehandle.write(bytearray(decoded))
                            filehandle.close()

                            # Converting to PNG
                            mediaType = '.png'
                            fpx = fp + '/' + str(fName) + mediaType
                            filepath.append(fpx)
                            im = Image.open(fpm)
                            im.save(fpx, 'PNG')
                            os.system('rm ' + fpm)
                            os.system('chmod 755 -R ' + fp + '*')
                            mediaType = 'png'

                        elif mediaType == 'png':
                            fName = mediaTime
                            fp = self.fu.tmpPath
                            if not os.path.exists(fp):
                                Log.i('DRV-Profile', 'Creating Directories')
                                os.system('mkdir -p ' + fp)
                            fpm = fp + '/' + str(fName) + '.' + mediaType
                            decoded = base64.b64decode(img_dec[1])
                            filehandle = open(fpm,'w+b')
                            filehandle.write(bytearray(decoded))
                            filehandle.close()

                            fpx = fp + '/' + str(fName) + '.' + mediaType
                            filepath.append(fpx)
                            im = Image.open(fpm)
                            im.save(fpx, 'PNG')
                            os.system('chmod 755 -R ' + fp + '*')

                        else:
                            message = 'Invalid Media File Type'
                            code = 4012


                        locationId = yield self.locationPoint.insert(
                                    {
                                        'disabled':False,
                                        'entityId':self.entityId,
                                        'location': [
                                            {
                                                'type': 'Point',
                                                'coordinates': [aLongitude, aLatitude]
                                            }
                                        ],
                                        'locName':locName,
                                        'locAddress':locAddress,
                                        'media':[
                                            {
                                                'time':mediaTime,
                                                'mimeType':'.' + mediaType
                                            }
                                        ]
                                    }
                                )
                        uPath = self.fu.uploads + str(self.entityId)
                        if not os.path.exists(uPath):
                            os.system('mkdir -p ' + uPath)
                            os.system('chmod 755 -R ' + uPath)

                        uPath = uPath + '/locationPoint/'
                        if not os.path.exists(uPath):
                            os.system('mkdir -p ' + uPath)
                            os.system('chmod 755 -R ' + uPath)

                        uPath = uPath + str(locationId) + '/'
                        if not os.path.exists(uPath):
                            os.system('mkdir -p ' + uPath)
                            os.system('chmod 755 -R ' + uPath)

                        for i in filepath:
                            os.system('mv ' + i + ' ' + uPath)
                        Log.d(uPath)
                        os.system('chmod 755 -R ' + uPath + '*')
                        status = True
                        code = 2000
                        message = 'New Location Point has been created.'
                        result = str(locationId)
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
                                'entityId': self.entityId,
                                'accountId': self.accountId,
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


                        locName = self.request.arguments.get('locName')
                        code, message = Validate.i(
                                    locName,
                                    'Location Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=40
                                )
                        if code != 4100:
                            raise Exception

                        locAddress = self.request.arguments.get('locAddress')
                        code, message = Validate.i(
                                    locAddress,
                                    'Location Address',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=200
                                )
                        if code != 4100:
                            raise Exception

                        try:
                            media = self.request.arguments.get('media')
                            if not len(media):
                                code = 4100
                                message = 'Media file missing'
                                raise Exception
                        except Exception as e:
                            code = 4100
                            message = 'Media file missing'
                            raise Exception


                        tDisabled = self.request.arguments.get('disabled')
                        code, message = Validate.i(
                                    tDisabled,
                                    'Disabled',
                                    dataType=bool
                                )
                        if code != 4100:
                            raise Exception


                        try:
                            vTypeId = ObjectId(self.request.arguments['id'])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception

                        try:
                            updateResult = yield self.serviceArea.find_and_modify(
                                    query = {
                                            '_id': vTypeId,
                                            'entityId': self.entityId
                                        },
                                    update = {
                                        '$set': {
                                            'disabled': tDisabled,
                                            'name': tName,
                                            'area': {
                                                        'type': 'Polygon',
                                                        'coordinates': [sArea]
                                                    },
                                            'description': tDescription
                                        }
                                    }
                            )
                            if updateResult:
                                status = True
                                code = 2000
                                message = 'Service Area details has been updated.'
                            else:
                                code = 4210
                                message = 'This Service Area does not exist.'
                        except:
                            status = False
                            code = 4280
                            message = 'This Service Area is already exists.'
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
            # TODO: this need to be moved in a global class, from here
            profile = yield self.profile.find(
                            {
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
                    if app[0]['apiId'] == 20216: # TODO: till here
                        try:
                            vTypeId = ObjectId(self.get_arguments('id')[0])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception
                        updateResult = yield self.serviceArea.find_and_modify(
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
                            message = 'Service Area has been Disabled.'
                        else:
                            code = 4210
                            message = 'This Service Area does not exist.'
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

