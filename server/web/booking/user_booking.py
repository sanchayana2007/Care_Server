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
class MmsWebUserBookingHandler(cyclone.web.RequestHandler,
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
                                        vDriverAccount = yield self.serviceAccount.find(
                                                {
                                                    'profileId': v['driverId']
                                                },
                                                limit=1
                                            )
                                        if not len(vDriverAccount):
                                            vDriverAccount = yield self.serviceAccount.find(
                                                    {
                                                        '_id': vDriverProfile[0]['accountId']
                                                    },
                                                    limit=1
                                                )
                                            if len(vDriverAccount):
                                                v['driverFullName'] = \
                                                        vDriverAccount[0]['firstName'] \
                                                        + ' ' + vDriverAccount[0]['lastName']
                                            else:
                                                Log.i('VID', 'Driver Not Found: ' + v['id'])
                                        else:
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

                            if limit != None:
                                vTypes = yield self.vehicle.find(
                                        {
                                            'entityId': self.entityId,
                                            'disabled': tDisabled
                                        },
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
                                            vDriverAccount = yield self.serviceAccount.find(
                                                    {
                                                        'profileId': v['driverId']
                                                    },
                                                    limit=1
                                                )
                                            if not len(vDriverAccount):
                                                vDriverAccount = yield self.serviceAccount.find(
                                                        {
                                                            '_id': vDriverProfile[0]['accountId']
                                                        },
                                                        limit=1
                                                    )
                                                if len(vDriverAccount):
                                                    v['driverFullName'] = \
                                                            vDriverAccount[0]['firstName'] \
                                                            + ' ' + vDriverAccount[0]['lastName']
                                                else:
                                                    Log.i('VID', 'Driver Not Found: ' + v['id'])
                                            else:
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
                                    status = True
                                    code = 2000
                                else:
                                    code = 3001
                                    message = 'No Vehicle Found.'
                            else:
                                vTypes = yield self.vehicle.find(
                                        {
                                            'entityId': self.entityId,
                                            'disabled': tDisabled
                                        }
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
                                            vDriverAccount = yield self.serviceAccount.find(
                                                    {
                                                        'profileId': v['driverId']
                                                    },
                                                    limit=1
                                                )
                                            if not len(vDriverAccount):
                                                vDriverAccount = yield self.serviceAccount.find(
                                                        {
                                                            '_id': vDriverProfile[0]['accountId']
                                                        },
                                                        limit=1
                                                    )
                                                if len(vDriverAccount):
                                                    v['driverFullName'] = \
                                                            vDriverAccount[0]['firstName'] \
                                                            + ' ' + vDriverAccount[0]['lastName']
                                                else:
                                                    Log.i('VID', 'Driver Not Found: ' + v['id'])
                                            else:
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

            '''
                Geting Last Booking Request Time
                Blocking for 5 second ( in microsecond )
            '''
            profile = yield self.profile.find(
                            {
                                'entityId': self.entityId,
                                'accountId': self.accountId,
                                'applicationId': self.applicationId,
                                '$or': [
                                    {
                                        'lastBookingRequest': None
                                    },
                                    {
                                        'lastBookingRequest':
                                        {
                                            '$lt': self.time - 5000000
                                        }
                                    }
                                ]
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
                self.profileId = profile[0]['_id']
                if len(app):
                    if app[0]['apiId'] == 40216: # TODO: till here

                        bStartPoint = self.request.arguments.get('startPoint')
                        code, message = Validate.i(
                                    bStartPoint,
                                    'startPoint',
                                    dataType=dict,
                                    maxLength=2,
                                    minLength=2
                                )
                        if code != 4100:
                            raise Exception

                        code, message = Validate.i(
                                    bStartPoint.get('address'),
                                    'startpoint.address',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=120
                                )
                        if code != 4100:
                            raise Exception

                        code, message = Validate.i(
                                    bStartPoint.get('coordinates'),
                                    'startPoint.coordinates',
                                    dataType=list,
                                    maxLength=2,
                                    minLength=2
                                )
                        if code != 4100:
                            raise Exception

                        code, message = Validate.i(
                                    bStartPoint.get('coordinates')[0],
                                    'startPoint.coordinates.0',
                                    dataType=float,
                                    exception=0.0,
                                    maxNumber=180,
                                    minNumber=-180
                                )
                        if code != 4100:
                            raise Exception

                        code, message = Validate.i(
                                    bStartPoint.get('coordinates')[1],
                                    'start.Point.coordinates.1.',
                                    dataType=float,
                                    exception=0.0,
                                    maxNumber=90,
                                    minNumber=-90
                                )
                        if code != 4100:
                            raise Exception

                        bEndPoint = self.request.arguments.get('endPoint')
                        code, message = Validate.i(
                                    bEndPoint,
                                    'endPoint',
                                    dataType=dict,
                                    maxLength=2,
                                    minLength=2
                                )
                        if code != 4100:
                            raise Exception

                        code, message = Validate.i(
                                    bEndPoint.get('address'),
                                    'endPoint.address',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=120
                                )
                        if code != 4100:
                            raise Exception

                        code, message = Validate.i(
                                    bEndPoint.get('coordinates'),
                                    'endPoint.coordinates.',
                                    dataType=list,
                                    maxLength=2,
                                    minLength=2
                                )
                        if code != 4100:
                            raise Exception

                        code, message = Validate.i(
                                    bEndPoint.get('coordinates')[0],
                                    'endPoint.coordinates.0',
                                    dataType=float,
                                    exception=0.0,
                                    maxNumber=180,
                                    minNumber=-180
                                )
                        if code != 4100:
                            raise Exception

                        code, message = Validate.i(
                                    bEndPoint.get('coordinates')[1],
                                    'endPoint.coordinates.1',
                                    dataType=float,
                                    exception=0.0,
                                    maxNumber=90,
                                    minNumber=-90
                                )
                        if code != 4100:
                            raise Exception

                        bPayment = self.request.arguments.get('payment')
                        code, message = Validate.i(
                                    bPayment,
                                    'payment',
                                    dataType=dict,
                                    maxLength=3,
                                    minLength=2
                                )
                        if code != 4100:
                            raise Exception
                        '''
                            Payment Type
                            Supported Types:
                                 1. Hard Cash value 0
                        '''
                        code, message = Validate.i(
                                    bPayment.get('type'),
                                    'pament.type',
                                    dataType=int,
                                    maxNumber=0,
                                    minNumber=0
                                )
                        if code != 4100:
                            raise Exception
                        '''
                            Estimated Price of the Booking based on perKmRate
                            Max 100,000 Rupee 1 Lakh
                            Min 0
                        '''
                        code, message = Validate.i(
                                    bPayment.get('price'),
                                    'pament.price',
                                    dataType=float,
                                    maxNumber=1000000,
                                    minNumber=0
                                )
                        if code != 4100:
                            raise Exception


                        bElement = self.request.arguments.get('element')
                        code, message = Validate.i(
                                    bElement,
                                    'element',
                                    dataType=dict,
                                    maxLength=2,
                                    minLength=2
                                )
                        if code != 4100:
                            raise Exception
                        '''
                            Estimated Duration of the Booking
                            Max 30 Day in microsecond 2592000000000
                            Min 0
                        '''
                        code, message = Validate.i(
                                    bElement.get('duration'),
                                    'element.duration',
                                    dataType=int,
                                    maxNumber=2592000000000,
                                    minNumber=0
                                )
                        if code != 4100:
                            raise Exception

                        '''
                            Estimated Distance of the Booking
                            Max 20,000 KM in metre 20,000,000
                            Min 0
                        '''
                        code, message = Validate.i(
                                    bElement.get('distance'),
                                    'element.distance',
                                    dataType=float,
                                    maxNumber=20000000,
                                    exception=0
                                )
                        if code != 4100:
                            raise Exception

                        try:
                            vTypeId = ObjectId(self.request.arguments.get('vehicleTypeId'))
                            vType = yield self.vehicleType.find(
                                        {
                                            '_id': vTypeId,
                                            'disabled': False,
                                            'entityId': self.entityId,
                                        },
                                        {
                                            '_id': 1,
                                            'name': 1
                                        },
                                        limit=1
                                    )
                            if not len(vType):
                                raise Exception
                            else:
                                vType[0]['id'] = vType[0]['_id']
                                del vType[0]['_id']
                        except:
                            code = 4132
                            message = 'Invalid Argument - [ vehicleTypeId ].'
                            raise Exception

                        try:
                            vCatId = ObjectId(self.request.arguments.get('vehicleCategoryId'))
                            vCat = yield self.bookingCategory.find(
                                        {
                                            '_id': vCatId,
                                            'disabled': False,
                                            'entityId': self.entityId,
                                            'vehicleType.id': vTypeId
                                        },
                                        {
                                            '_id': 1,
                                            'name': 1,
                                            'onDemand': 1,
                                            'scheduleEndTime': 1,
                                            'vehicleType': 1
                                        },
                                        limit=1
                                    )
                            if not len(vCat):
                                raise Exception
                            else:
                                bFareCharge = [val for idx, val \
                                        in enumerate(vCat[0]['vehicleType'])\
                                            if val['id'] == vTypeId][0]
                                del bFareCharge['id']
                                vCat[0]['id'] = vCat[0]['_id']
                                del vCat[0]['_id']
                                del vCat[0]['vehicleType']
                        except:
                            code = 4133
                            message = 'Invalid Argument - [ vehicleCategoryId ].'
                            raise Exception

                        bSchedule = self.request.arguments.get('schedule')
                        code, message = Validate.i(
                                    bSchedule,
                                    'schedule',
                                    dataType=list,
                                    maxLength=2
                                )
                        if code != 4100:
                            raise Exception

                        if len(bSchedule):
                            for idx, val in enumerate(bSchedule):

                                if type(val) != int:
                                    code = 4190
                                    message = 'Invalid Argument - [ schedule.{0} ].'.format(idx)
                                    raise Exception
                                if val < self.time:
                                    code = 4191
                                    message = 'Invalid Argument - [ schedule.{0} ].'.format(idx)
                                    raise Exception

                                # Current Time + 6 months
                                if val > self.time + 15778476000000:
                                    code = 4192
                                    message = 'Invalid Argument - [ schedule.{0} ].'.format(idx)
                                    raise Exception
                            if bCategory['scheduleEndTime'] and len(bSchedule) < 2:
                                code = 4194
                                message = 'End time required in this Booking Category.'
                                raise Exception
                        try:
                            '''
                                Getting All the Details of the Requestor
                                Combines account, profile from BigBase
                                If serviceAccount available it will on priority
                            '''
                            rAccount = yield self.account.find(
                                                {
                                                    '_id': self.accountId
                                                },
                                                {
                                                    '_id': 1,
                                                    'firstName': 1,
                                                    'lastName': 1,
                                                    'contact': 1
                                                },
                                                limit=1
                                            )
                            if not len(rAccount):
                                code = 5150
                                message =  'Requestor Account Not Found.'
                                raise Exception
                            requestorAccount = {}
                            requestorAccount['id'] = self.profileId
                            requestorAccount['firstName'] = rAccount[0].get('firstName')
                            requestorAccount['lastName'] = rAccount[0].get('lastName')
                            requestorAccount['contact'] = rAccount[0].get('contact')
                            rServiceAccount = yield self.serviceAccount.find(
                                    {
                                        'profileId': self.profileId,
                                        'entityId': self.entityId
                                    },
                                    {
                                        'firstName': 1,
                                        'lastName': 1
                                    },
                                    limit=1
                            )
                            if len(rServiceAccount):
                                requestorAccount['firstName'] = rServiceAccount[0].get('firstName')
                                requestorAccount['lastName'] = rServiceAccount[0].get('lastName')
                            '''
                                On Demand ( Booking Now will directly go request to the drivers )
                            '''
                            if vCat[0]['onDemand']:
                                '''
                                    Finding vehicles rearby
                                    Filters:
                                        1. 5000 mitre Max distance from start Point
                                        2. Entity Id
                                        3. Disabled False ( Active Vehicle )
                                        4. Last Location Update time with in 2 hour
                                        5. Vehicle Type
                                        6. Max Vehicle ( Not Set)
                                '''
                                nearVehcle = yield self.vehicle.find(
                                        {
                                            'entityId': self.entityId,
                                            'disabled': False,
                                            'typeId': vTypeId,
                                            'location.1.time':
                                            {
                                                '$gte': self.time - 7200000000
                                            },
                                            'location.0' :
                                            { '$near' :
                                                {
                                                    '$geometry' :
                                                    {
                                                        'type' : "Point" ,
                                                        'coordinates' : bStartPoint['coordinates']
                                                    },
                                                    '$maxDistance' : 5000
                                                }
                                            }
                                        },
                                        {
                                            '_id': 1,
                                            'driverId': 1
                                        }
                                )
                                bRequested = []
                                if not len(nearVehcle):
                                    code = 4210
                                    message = 'No Vehicle is available at this moment.'
                                    raise Exception
                                '''
                                    Publishing Booking Request to the Drivers of those vehicles
                                    Filters:
                                     None
                                '''
                                # TODO: for now for the filtering
                                for idx, nv in enumerate(nearVehcle):
                                    driverProfile = yield self.profile.find(
                                                {
                                                    '_id': nv['driverId'],
                                                    'closed': False
                                                },
                                                {
                                                    '_id': 1
                                                },
                                                limit=1
                                            )
                                    if len(driverProfile):
                                        rd =    {
                                                    'vehicleId': nv['_id'],
                                                    'driverId': nv['driverId']
                                                }
                                        bRequested.append(rd)
                                '''
                                    All the Details of the Booking
                                    Set Activity:
                                     1. Requested.
                                '''
                                bookingId = yield self.booking.insert(
                                        {
                                            'entityId': self.entityId,
                                            'requestor': requestorAccount,
                                            'disabled': False,
                                            'startPoint': [
                                                {
                                                    'type': 'Point',
                                                    'coordinates': bStartPoint['coordinates']
                                                },
                                                {
                                                    'address': bStartPoint['address']
                                                }
                                            ],
                                            'endPoint': [
                                                {
                                                    'type': 'Point',
                                                    'coordinates': bStartPoint['coordinates']
                                                },
                                                {
                                                    'address': bStartPoint['address']
                                                }
                                            ],
                                            'schedule': bSchedule,
                                            'fareCharge': bFareCharge,
                                            'payment': [
                                                bPayment
                                            ],
                                            'element': [
                                                bElement
                                            ],
                                            'vehicleType': vType[0],
                                            'category': vCat[0],
                                            'activity': [
                                                {
                                                    'id': 1,
                                                    'time': self.time,
                                                    'requested': bRequested
                                                }
                                            ]
                                        }
                                    )
                                '''
                                    Converting ObjectId to string
                                '''
                                requestorAccount['id'] = str(requestorAccount['id'])
                                if len(requestorAccount['contact']) > 1:
                                    requestorAccount['contact'] = [requestorAccount['contact'][0]]
                                vType[0]['id'] = str(vType[0]['id'])
                                vCat[0]['id'] = str(vCat[0]['id'])
                                '''
                                    Booking Request for Publish
                                    Socket Code: 2507190750
                                    Element:
                                     1. Start Point of that Booking
                                     2. End Point of that Booking
                                '''
                                liveBookingRequest = {
                                            'code': 2507190750,
                                            'status': True,
                                            'message': 'New Booking Request.',
                                            'result': [
                                                {
                                                    'bookingId': str(bookingId),
                                                    'requestor': [requestorAccount],
                                                    'startPoint': [bStartPoint],
                                                    'endPoint': [bEndPoint],
                                                    'schedule': bSchedule,
                                                    'time': self.time,
                                                    'fareCharge': [bFareCharge],
                                                    'payment': [bPayment],
                                                    'element': [bElement],
                                                    'vehicleType': vType,
                                                    'category': vCat
                                                }
                                            ]
                                        }
                                for dnv in bRequested:
                                    channelId = '{0}_{1}'.format(
                                                'PROFILE',
                                                dnv['driverId']
                                            )
                                    yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingRequest))

                                '''
                                    Saving the Last Booking Reqested Time
                                '''
                                updateResult = yield self.profile.update(
                                            {
                                                '_id': self.profileId
                                            },
                                            {
                                                '$set':
                                                {
                                                    'lastBookingRequest': self.time
                                                }
                                            }
                                        )
                                if updateResult['n']:
                                    status = True
                                    code = 2000
                                    message = 'Booking Request has been Sent.'
                                    result.append(
                                                str(bookingId)
                                            )
                                else:
                                    code = 5180
                                    message = 'Internal Error Please Contact the Support Team.'
                            else:
                                status = False
                                code = 5080
                                message = 'This feature is Coming Soon.'
                        except Exception as e:
                            if code == 4100:
                                code = 5180
                                message = 'Internal Error Please Contact the Support Team.'
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = exc_tb.tb_frame.f_code.co_filename
                                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
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
                            vTypeId = ObjectId(self.request.arguments['id'])
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

                        vModel = self.request.arguments.get('make')
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
                                            '_id': vTypeId,
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

