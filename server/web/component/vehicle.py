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

@xenSecureV1
class VehicleHandler(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('GET', 'POST', 'DELETE','PUT')

    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][6]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]

    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    locationSource = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][7]['name']
                ]

    serviceAccount = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][0]['name']
                ]

    geofence = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][6]['name']
                ]

    vehicle = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][4]['name']
                ]

    device = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][9]['name']
                ]

    vehicleType = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][2]['name']
                ]

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
                    if app[0]['apiId'] == 20216: # TODO: till here
                        try:
                            tDisabled = bool(int(self.get_arguments('disabled')[0]))
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ disabled ].'
                            raise Exception
                        try:
                            vTypeId = ObjectId(self.get_arguments('id')[0])
                        except:
                            vTypeId = None

                        try:
                            vvTypeId = ObjectId(self.get_arguments('typeId')[0])
                        except:
                            vvTypeId = None

                        if vTypeId != None:
                            vTypes = yield self.vehicle.find(
                                        {
                                            '_id': vTypeId,
                                            'entityId': self.entityId,
                                            'disabled': tDisabled
                                        },
                                        limit=1
                                    )
                            if len(vTypes):
                                for v in vTypes:
                                    v['id'] = str(v['_id'])
                                    del v['_id']
                                    del v['entityId']
                                    vType = yield self.vehicleType.find(
                                            {
                                                '_id': v['typeId'],
                                                'entityId': self.entityId,
                                            },
                                            limit=1
                                        )
                                    if len(vType):
                                        v['typeName'] = vType[0]['name']
                                    vLocationSource = yield self.locationSource.find(
                                        {
                                            '_id': v['locationSourceId']
                                            },
                                        limit=1
                                    )
                                    if len(vLocationSource):
                                        if vLocationSource[0]['apiId'] != 200:
                                            vDevice = yield self.device.find(
                                                {
                                                    '_id': v['deviceId']
                                                }
                                            )
                                            if len(vDevice):
                                                v['deviceSerialNumber'] = str(vDevice[0]['serialNumber'])
                                    else:
                                        Log.i('VID', 'Loc-Src Not Found: ' + v['id'])
                                    vDriverProfile = yield self.profile.find(
                                            {
                                                '_id': v['driverId']
                                            },
                                            limit=1
                                        )
                                    if len(vDriverProfile):
                                        vDriverAccount = yield self.account.find(
                                                        {
                                                            '_id': vDriverProfile[0]['accountId']
                                                        },
                                                        {
                                                            'firstName': 1,
                                                            'lastName': 1,
                                                            'contact': 1
                                                        },
                                                        limit=1
                                                    )
                                        if len(vDriverAccount):
                                            v['driverFullName'] = \
                                                    vDriverAccount[0]['firstName'] \
                                                    + ' ' + vDriverAccount[0]['lastName']
                                            v['driverContactNumber'] = \
                                                    vDriverAccount[0]['contact'][0]['value']
                                        vDriverAccount = yield self.serviceAccount.find(
                                                {
                                                    'profileId': v['driverId']
                                                },
                                                {
                                                    'firstName': 1,
                                                    'lastName': 1
                                                },
                                                limit=1
                                            )
                                        if len(vDriverAccount):
                                            v['driverFullName'] = \
                                                    vDriverAccount[0]['firstName'] \
                                                    + ' ' + vDriverAccount[0]['lastName']
                                    else:
                                        Log.i('VID', 'Driver Not Found: ' + v['id'])
                                    vGeofence = yield self.geofence.find(
                                            {
                                                '_id': v['geofenceId']
                                            },
                                            limit=1
                                        )
                                    if len(vGeofence):
                                        v['geofenceName'] = vGeofence[0]['name']
                                    else:
                                        Log.i('VID', 'Geofence Not Found: ' + v['id'])
                                    v['driverId'] = str(v['driverId'])
                                    v['typeId'] = str(v['typeId'])
                                    v['deviceId'] = str(v['deviceId'])
                                    v['geofenceId'] = str(v['geofenceId'])
                                    v['locationSourceId'] = str(v['locationSourceId'])
                                    result.append(v)
                                status = True
                                code = 2000
                            else:
                                code = 3001
                                message = 'No Vehicle Found.'
                        else:
                            try:
                                limit = int(self.get_arguments('limit')[0])
                            except:
                                limit = None

                            try:
                                skip = int(self.get_arguments('skip')[0])
                            except:
                                skip = 0

                            if not vvTypeId:
                                vehicleQuery = {
                                            'entityId': self.entityId,
                                            'disabled': tDisabled
                                        }
                            else:
                                vehicleQuery = {
                                            'entityId': self.entityId,
                                            'disabled': tDisabled,
                                            'typeId': vvTypeId
                                        }
                            if limit != None:
                                vTypes = yield self.vehicle.find(
                                        vehicleQuery,
                                        limit=limit,
                                        skip=skip
                                    )
                                if len(vTypes):
                                    for v in vTypes:
                                        v['id'] = str(v['_id'])
                                        del v['_id']
                                        del v['entityId']
                                        vType = yield self.vehicleType.find(
                                                {
                                                    '_id': v['typeId'],
                                                    'entityId': self.entityId,
                                                },
                                                limit=1
                                            )
                                        if len(vType):
                                            v['typeName'] = vType[0]['name']
                                        vLocationSource = yield self.locationSource.find(
                                            {
                                                '_id': v['locationSourceId']
                                            },
                                            limit=1
                                        )
                                        if len(vLocationSource):
                                            if vLocationSource[0]['apiId'] != 200:
                                                vDevice = yield self.device.find(
                                                    {
                                                        '_id': v['deviceId']
                                                    }
                                                )
                                                if len(vDevice):
                                                    v['deviceSerialNumber'] = str(vDevice[0]['serialNumber'])
                                        else:
                                            Log.i('VID', 'Loc-Src Not Found: ' + v['id'])
                                        vDriverProfile = yield self.profile.find(
                                                {
                                                    '_id': v['driverId']
                                                },
                                                limit=1
                                            )
                                        if len(vDriverProfile):
                                            vDriverAccount = yield self.account.find(
                                                        {
                                                            '_id': vDriverProfile[0]['accountId']
                                                        },
                                                        {
                                                            'firstName': 1,
                                                            'lastName': 1,
                                                            'contact': 1
                                                        },
                                                        limit=1
                                                    )
                                            if len(vDriverAccount):
                                                v['driverFullName'] = \
                                                        vDriverAccount[0]['firstName'] \
                                                        + ' ' + vDriverAccount[0]['lastName']
                                                v['driverContactNumber'] = \
                                                        vDriverAccount[0]['contact'][0]['value']
                                                vDriverAccount = yield self.serviceAccount.find(
                                                    {
                                                        'profileId': v['driverId']
                                                    },
                                                    {
                                                        'firstName': 1,
                                                        'lastName': 1
                                                    },
                                                    limit=1
                                                )
                                                if len(vDriverAccount):
                                                    v['driverFullName'] = \
                                                            vDriverAccount[0]['firstName'] \
                                                            + ' ' + vDriverAccount[0]['lastName']

                                        else:
                                            Log.i('VID', 'Driver Not Found: ' + v['id'])
                                        vGeofence = yield self.geofence.find(
                                                {
                                                    '_id': v['geofenceId']
                                                },
                                                limit=1
                                            )
                                        if len(vGeofence):
                                            v['geofenceName'] = vGeofence[0]['name']
                                        else:
                                            Log.i('VID', 'Geofence Not Found: ' + v['id'])
                                        v['driverId'] = str(v['driverId'])
                                        v['typeId'] = str(v['typeId'])
                                        v['deviceId'] = str(v['deviceId'])
                                        v['geofenceId'] = str(v['geofenceId'])
                                        v['locationSourceId'] = str(v['locationSourceId'])
                                        result.append(v)
                                    status = True
                                    code = 2000
                                else:
                                    code = 3001
                                    message = 'No Vehicle Found.'
                            else:
                                vTypes = yield self.vehicle.find(
                                        vehicleQuery
                                    )
                                if len(vTypes):
                                    for v in vTypes:
                                        v['id'] = str(v['_id'])
                                        del v['_id']
                                        del v['entityId']
                                        vType = yield self.vehicleType.find(
                                                {
                                                    '_id': v['typeId'],
                                                    'entityId': self.entityId,
                                                },
                                                limit=1
                                            )
                                        if len(vType):
                                            v['typeName'] = vType[0]['name']
                                        vLocationSource = yield self.locationSource.find(
                                            {
                                                '_id': v['locationSourceId']
                                            },
                                            limit=1
                                        )
                                        if len(vLocationSource):
                                            if vLocationSource[0]['apiId'] != 200:
                                                vDevice = yield self.device.find(
                                                    {
                                                        '_id': v['deviceId']
                                                    }
                                                )
                                                if len(vDevice):
                                                    v['deviceSerialNumber'] = str(vDevice[0]['serialNumber'])
                                        else:
                                            Log.i('VID', 'Loc-Src Not Found: ' + v['id'])
                                        vDriverProfile = yield self.profile.find(
                                                {
                                                    '_id': v['driverId']
                                                },
                                                limit=1
                                            )
                                        if len(vDriverProfile):
                                            vDriverAccount = yield self.account.find(
                                                        {
                                                            '_id': vDriverProfile[0]['accountId']
                                                        },
                                                        {
                                                            'firstName': 1,
                                                            'lastName': 1,
                                                            'contact': 1
                                                        },
                                                        limit=1
                                                    )
                                            if len(vDriverAccount):
                                                v['driverFullName'] = \
                                                        vDriverAccount[0]['firstName'] \
                                                        + ' ' + vDriverAccount[0]['lastName']
                                                v['driverContactNumber'] = \
                                                        vDriverAccount[0]['contact'][0]['value']
                                                vDriverAccount = yield self.serviceAccount.find(
                                                    {
                                                        'profileId': v['driverId']
                                                    },
                                                    {
                                                        'firstName': 1,
                                                        'lastName': 1
                                                    },
                                                    limit=1
                                                )
                                                if len(vDriverAccount):
                                                    v['driverFullName'] = \
                                                            vDriverAccount[0]['firstName'] \
                                                            + ' ' + vDriverAccount[0]['lastName']

                                        else:
                                            Log.i('VID', 'Driver Not Found: ' + v['id'])
                                        vGeofence = yield self.geofence.find(
                                                {
                                                    '_id': v['geofenceId']
                                                },
                                                limit=1
                                            )
                                        if len(vGeofence):
                                            v['geofenceName'] = vGeofence[0]['name']
                                        else:
                                            Log.i('VID', 'Geofence Not Found: ' + v['id'])
                                        v['driverId'] = str(v['driverId'])
                                        v['typeId'] = str(v['typeId'])
                                        v['deviceId'] = str(v['deviceId'])
                                        v['geofenceId'] = str(v['geofenceId'])
                                        v['locationSourceId'] = str(v['locationSourceId'])
                                        result.append(v)
                                    status = True
                                    code = 2000
                                else:
                                    code = 3001
                                    message = 'No Vehicle Found.'
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
                    if app[0]['apiId'] == 20216: # TODO: till here

                        vRegistrationNumber = self.request.arguments.get('registrationNumber')
                        code, message = Validate.i(
                                    vRegistrationNumber,
                                    'Registration Number',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial2=True,
                                    maxLength=80,
                                    minLength=5
                                )
                        if code != 4100:
                            raise Exception

                        vMake = self.request.arguments.get('make')
                        code, message = Validate.i(
                                    vMake,
                                    'Make',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=60
                                )
                        if code != 4100:
                            raise Exception

                        vModel = self.request.arguments.get('model')
                        code, message = Validate.i(
                                    vModel,
                                    'Model',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=60
                                )
                        if code != 4100:
                            raise Exception

                        vColor = self.request.arguments.get('color')
                        code, message = Validate.i(
                                    vColor,
                                    'Color',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=60
                                )
                        if code != 4100:
                            raise Exception

                        try:
                            vTypeId = ObjectId(self.request.arguments.get('typeId'))
                            vType = yield self.vehicleType.find(
                                        {
                                            '_id': vTypeId,
                                            'entityId': self.entityId,
                                        },
                                        limit=1
                                    )
                            if not len(vType):
                                raise Exception
                        except:
                            code = 4132
                            message = 'Invalid Argument - [ typeId ].'
                            raise Exception

                        driverApplication = yield self.applications.find(
                            {
                                'apiId': 30216,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
                        if not len(driverApplication):
                            raise Exception
                        try:
                            vDriverId = ObjectId(self.request.arguments.get('driverId'))
                            vDriver = yield self.profile.find(
                                        {
                                            '_id': vDriverId,
                                            'entityId': self.entityId,
                                            'applicationId': driverApplication[0]['_id']
                                        },
                                        limit=1
                                    )
                            if not len(vDriver):
                                raise Exception
                        except:
                            code = 4130
                            message = 'Invalid Argument - [ driverId ].'
                            raise Exception

                        try:
                            vLocationSourceId = ObjectId(self.request.arguments.get('locationSourceId'))
                            vLocationSource = yield self.locationSource.find(
                                        {
                                            '_id': vLocationSourceId
                                        },
                                        limit=1
                                    )
                            if not len(vLocationSource):
                                raise Exception
                        except:
                            code = 4132
                            message = 'Invalid Argument - [ locationSourceId ].'
                            raise Exception
                        if vLocationSource[0]['apiId'] == 200:
                            vDeviceId = vDriverId
                        else:
                            try:
                                vDeviceId = ObjectId(self.request.arguments.get('deviceId'))
                                vDevice = yield self.device.find(
                                        {
                                            '_id': vDeviceId,
                                            'entityId': self.entityId,
                                        },
                                        limit=1
                                    )
                                if not len(vDevice):
                                    raise Exception
                            except:
                                code = 4131
                                message = 'Invalid Argument - [ deviceId ].'
                                raise Exception

                        try:
                            vGeofenceId = ObjectId(self.request.arguments.get('geofenceId'))
                            vGeofence = yield self.geofence.find(
                                        {
                                            '_id': vGeofenceId,
                                            'entityId': self.entityId
                                        },
                                        limit=1
                                    )
                            if not len(vGeofence):
                                raise Exception
                        except:
                            code = 4133
                            message = 'Invalid Argument - [ geofenceId ].'
                            raise Exception
                        vEntity = yield self.entity.find(
                                    {
                                        '_id': self.entityId
                                    },
                                    limit=1
                                )
                        if not vEntity:
                            raise Exception
                        try:
                            vLocation = [vEntity[0]['location']]
                            vLocation.append(
                                    {
                                        'time': self.time,
                                        'ignition': False,
                                        'orientation': 0,
                                        'distance': 0,
                                        'speed': 0
                                    }
                                )
                            yield self.vehicle.insert(
                                    {
                                        'disabled': False,
                                        'registrationNumber': vRegistrationNumber,
                                        'make': vMake,
                                        'model': vModel,
                                        'color': vColor,
                                        'driverId': vDriverId,
                                        'deviceId': vDeviceId,
                                        'geofenceId': vGeofenceId,
                                        'typeId': vTypeId,
                                        'locationSourceId': vLocationSourceId,
                                        'location': vLocation,
                                        'entityId': self.entityId
                                    }
                                )
                            status = True
                            code = 2000
                            message = 'New Vehicle has been added.'
                        except Exception as e:
                            exe = str(e).split(':')
                            if len(exe) < 2:
                                status = False
                                code = 4280
                                message = 'This Vehicle is already exists.'
                            elif 'registrationNumber_1' in exe[2]:
                                status = False
                                code = 4281
                                message = 'This Registration is already exists.'
                            elif 'driverId_1' in exe[2]:
                                status = False
                                code = 4282
                                message = 'This Driver is already assigned with another Vehicle.'
                            elif 'deviceId_1' in exe[2]:
                                status = False
                                code = 4283
                                message = 'This Device is already attached with another Vehicle.'
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
                    if app[0]['apiId'] == 20216: # TODO: till here

                        tDisabled = self.request.arguments.get('disabled')
                        code, message = Validate.i(
                                    tDisabled,
                                    'Disabled',
                                    dataType=bool
                                )
                        if code != 4100:
                            raise Exception

                        try:
                            vVehicleId = ObjectId(self.request.arguments['id'])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception

                        vRegistrationNumber = self.request.arguments.get('registrationNumber')
                        code, message = Validate.i(
                                    vRegistrationNumber,
                                    'Registration Number',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial2=True,
                                    maxLength=80,
                                    minLength=5
                                )
                        if code != 4100:
                            raise Exception

                        vMake = self.request.arguments.get('make')
                        code, message = Validate.i(
                                    vMake,
                                    'Make',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=60
                                )
                        if code != 4100:
                            raise Exception

                        vModel = self.request.arguments.get('model')
                        code, message = Validate.i(
                                    vModel,
                                    'Model',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=60
                                )
                        if code != 4100:
                            raise Exception

                        vColor = self.request.arguments.get('color')
                        code, message = Validate.i(
                                    vColor,
                                    'Color',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=60
                                )
                        if code != 4100:
                            raise Exception

                        try:
                            vTypeId = ObjectId(self.request.arguments.get('typeId'))
                            vType = yield self.vehicleType.find(
                                        {
                                            '_id': vTypeId,
                                            'entityId': self.entityId,
                                        },
                                        limit=1
                                    )
                            if not len(vType):
                                raise Exception
                        except:
                            code = 4132
                            message = 'Invalid Argument - [ typeId ].'
                            raise Exception


                        driverApplication = yield self.applications.find(
                            {
                                'apiId': 30216,
                                'entityId': self.entityId
                            },
                            limit=1
                        )
                        if not len(driverApplication):
                            raise Exception
                        try:
                            vDriverId = ObjectId(self.request.arguments.get('driverId'))
                            vDriver = yield self.profile.find(
                                        {
                                            '_id': vDriverId,
                                            'entityId': self.entityId,
                                            'applicationId': driverApplication[0]['_id']
                                        },
                                        limit=1
                                    )
                            if not len(vDriver):
                                raise Exception
                        except:
                            code = 4130
                            message = 'Invalid Argument - [ driverId ].'
                            raise Exception

                        try:
                            vLocationSourceId = ObjectId(self.request.arguments.get('locationSourceId'))
                            vLocationSource = yield self.locationSource.find(
                                        {
                                            '_id': vLocationSourceId
                                        },
                                        limit=1
                                    )
                            if not len(vLocationSource):
                                raise Exception
                        except:
                            code = 4132
                            message = 'Invalid Argument - [ locationSourceId ].'
                            raise Exception
                        if vLocationSource[0]['apiId'] == 200:
                            vDeviceId = vDriverId
                        else:
                            try:
                                vDeviceId = ObjectId(self.request.arguments.get('deviceId'))
                                vDevice = yield self.device.find(
                                        {
                                            '_id': vDeviceId,
                                            'entityId': self.entityId,
                                        },
                                        limit=1
                                    )
                                if not len(vDevice):
                                    raise Exception
                            except:
                                code = 4131
                                message = 'Invalid Argument - [ deviceId ].'
                                raise Exception

                        try:
                            vGeofenceId = ObjectId(self.request.arguments.get('geofenceId'))
                            vGeofence = yield self.geofence.find(
                                        {
                                            '_id': vGeofenceId,
                                            'entityId': self.entityId
                                        },
                                        limit=1
                                    )
                            if not len(vGeofence):
                                raise Exception
                        except:
                            code = 4133
                            message = 'Invalid Argument - [ geofenceId ].'
                            raise Exception
                        vEntity = yield self.entity.find(
                                    {
                                        '_id': self.entityId
                                    },
                                    limit=1
                                )
                        if not vEntity:
                            raise Exception
                        try:
                            updateResult = yield self.vehicle.find_and_modify(
                                    query = {
                                            '_id': vVehicleId,
                                            'entityId': self.entityId
                                        },
                                    update = {
                                        '$set': {
                                            'disabled': tDisabled,
                                            'registrationNumber': vRegistrationNumber,
                                            'make': vMake,
                                            'model': vModel,
                                            'color': vColor,
                                            'driverId': vDriverId,
                                            'typeId': vTypeId,
                                            'deviceId': vDeviceId,
                                            'geofenceId': vGeofenceId,
                                            'locationSourceId': vLocationSourceId,
                                        }
                                    }
                            )
                            if updateResult:
                                status = True
                                code = 2000
                                message = 'Vehicle details has been updated.'
                            else:
                                code = 4210
                                message = 'This Vehicle does not exist.'
                        except Exception as e:
                            exe = str(e).split(':')
                            if len(exe) < 2:
                                status = False
                                code = 4280
                                message = 'This Vehicle is already exists.'
                            elif 'registrationNumber_1' in exe[2]:
                                status = False
                                code = 4281
                                message = 'This Registration is already exists.'
                            elif 'driverId_1' in exe[2]:
                                status = False
                                code = 4282
                                message = 'This Driver is already assigned with another Vehicle.'
                            elif 'deviceId_1' in exe[2]:
                                status = False
                                code = 4283
                                message = 'This Device is already attached with another Vehicle.'
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

