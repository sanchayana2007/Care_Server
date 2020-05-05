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

@xenSecureV1
class MmsWebBookingHandler(cyclone.web.RequestHandler,
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

    fu = FileUtil()

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
                    if app[0]['apiId'] in [ 40216, 30216, 20216 ]: # TODO: till here

                        if self.apiId == 40216:
                            rQuery = {
                                        'entityId': self.entityId,
                                        '$where': 'this.activity[this.activity.length - 1].id != 1 || this.onDemand == false',
                                        'requestor.0.id': self.profileId
                                     }
                            rFields  = {
                                            '_id': 0,
                                            'activity': 1,
                                            'requestor': 1,
                                            'startPoint': 1,
                                            'endPoint': 1,
                                            'vehicleType': 1,
                                            'schedule': 1,
                                            'category': 1,
                                            'driver': 1,
                                            'vehicle': 1,
                                            'element': 1,
                                            'payment': 1,
                                            'feedback': 1,
                                            'route': 1
                                        }
                        elif self.apiId == 30216:
                            rQuery = {
                                        'entityId': self.entityId,
                                        '$where': 'this.activity[this.activity.length - 1].id != 1',
                                        'driver.0.id': self.profileId
                                     }
                            rFields  = {
                                            '_id': 0,
                                            'activity': 1,
                                            'requestor': 1,
                                            'startPoint': 1,
                                            'endPoint': 1,
                                            'vehicleType': 1,
                                            'schedule': 1,
                                            'category': 1,
                                            'driver': 1,
                                            'vehicle': 1,
                                            'element': 1,
                                            'payment': 1,
                                            'feedback': 1
                                        }
                        elif self.apiId == 20216:
                            rQuery = {
                                        'entityId': self.entityId,
                                     }
                            rFields  = {
                                            '_id': 0,
                                            'activity': 1,
                                            'requestor': 1,
                                            'startPoint': 1,
                                            'endPoint': 1,
                                            'vehicleType': 1,
                                            'schedule': 1,
                                            'category': 1,
                                            'driver': 1,
                                            'vehicle': 1,
                                            'element': 1,
                                            'payment': 1,
                                            'feedback': 1
                                        }
                        else:
                            code = 4003
                            message = 'You are not Authorized.'
                            self.set_status(401)
                            raise Exception

                        try:
                            rDisabled = bool(int(self.get_arguments('disabled')[0]))
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ disabled ].'
                            raise Exception

                        try:
                            rRowId = ObjectId(self.get_arguments('id')[0])
                        except:
                            rRowId = None

                        if rRowId:
                            rQuery['_id'] = rRowId
                            rQuery['disabled'] = rDisabled
                            rRows = yield self.booking.find(
                                        rQuery,
                                        rFields,
                                        limit=1
                                    )
                            if len(rRows):
                                for i1, v1 in enumerate(rRows):
                                    v1['id'] = str(rRowId)
                                    for i1, v2 in enumerate(v1['requestor']):
                                        v2['id'] = str(v2['id'])
                                    for i1, v2 in enumerate(v1['vehicleType']):
                                        v2['id'] = str(v2['id'])
                                    for i1, v2 in enumerate(v1['category']):
                                        v2['id'] = str(v2['id'])
                                    for i1, v2 in enumerate(v1['vehicle']):
                                        v2['id'] = str(v2['id'])
                                    for i1, v2 in enumerate(v1['driver']):
                                        v2['id'] = str(v2['id'])
                                    for i1, v2 in enumerate(v1['activity']):
                                        if v2['id'] == 9:
                                            v2['account'][0]['id'] = str(v2['account'][0]['id'])
                                    '''
                                        Deleting Driver Feedback
                                    '''
                                    if self.apiId == 40216:
                                        if len(v1['activity']) > 1:
                                            v1['oneTimePassword'] = v1['activity'][1]['code']
                                        if len(v1['feedback']) == 2:
                                            del v1['feedback'][1]
                                    '''
                                        Deleting User Feedback
                                    '''
                                    if self.apiId == 30216 and len(v1['feedback']):
                                        del v1['feedback'][0]
                                    for jx, f in enumerate(v1['feedback']):
                                        if not f:
                                            del v1['feedback'][jx]
                                    v1['time'] = v1['activity'][0]['time']
                                    if len(v1['driver']):
                                        fbx = self.fu.uploads + str(self.entityId) + '/booking/' + str(v1['id']) + '/' +\
                                                str(v1['driver'][0]['id'])
                                        fpu = fbx + '/profile.png'
                                        fpp = fpu.replace(self.fu.uploads, self.fu.uploadsPath)
                                        v1['driver'][0]['profilePicture'] = fpp
                                    del v1['activity'][0]['requested']
                                    result.append(v1)
                                result.reverse()
                                status = True
                                code = 2000
                            else:
                                code = 3001
                                message = 'No Booking Found.'
                        else:
                            try:
                                limit = int(self.get_arguments('limit')[0])
                            except:
                                limit = 0

                            try:
                                skip = int(self.get_arguments('skip')[0])
                            except:
                                skip = 0

                            rQuery['disabled'] = rDisabled
                            rRows = yield self.booking.find(
                                        rQuery,
                                        {
                                            '_id': 1,
                                            'activity': 1,
                                            'startPoint': 1,
                                            'endPoint': 1,
                                            'vehicleType': 1,
                                            'category': 1,
                                            'payment': 1,
                                            'feedback': 1,
                                            'onDemand': 1
                                        },
                                        limit=limit,
                                        skip=skip
                                    )
                            if len(rRows):
                                for i1, v1 in enumerate(rRows):
                                    v1['id'] = str(v1['_id'])
                                    del v1['_id']
                                    for i1, v2 in enumerate(v1['vehicleType']):
                                        v2['id'] = str(v2['id'])
                                    for i1, v2 in enumerate(v1['category']):
                                        v2['id'] = str(v2['id'])
                                    for i1, v2 in enumerate(v1['activity']):
                                        if v2['id'] == 9:
                                            v2['account'][0]['id'] = str(v2['account'][0]['id'])
                                    del v1['activity'][0]['requested']
                                    del v1['startPoint'][0]
                                    del v1['endPoint'][0]

                                    '''
                                        Deleting Driver Feedback
                                    '''
                                    if self.apiId == 40216:
                                        if len(v1['activity']) > 1 and v1['activity'][len(v1['activity']) - 1]['id'] != 9:
                                            v1['oneTimePassword'] = v1['activity'][1]['code']
                                        if len(v1['feedback']) == 2:
                                            del v1['feedback'][1]
                                    '''
                                        Deleting User Feedback
                                    '''
                                    if self.apiId == 30216 and len(v1['feedback']):
                                        del v1['feedback'][0]
                                    for jx, f in enumerate(v1['feedback']):
                                        if not f:
                                            del v1['feedback'][jx]
                                    # Giving the last Activity
                                    v1['time'] = v1['activity'][0]['time']
                                    v1['activity'] = [v1['activity'][len(v1['activity']) - 1]]
                                    result.append(v1)
                                result.reverse()
                                status = True
                                code = 2000
                            else:
                                code = 3001
                                message = 'No Booking Found.'
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
                                'closed': False,
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
                    if self.apiId == 40216: # TODO: till here

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
                                    dataType=int,
                                    maxNumber=1000000,
                                    minNumber=20
                                )
                        if code != 4100:
                            raise Exception
                        else:
                            bPayment['price'] = long(bPayment['price'])

                        bElement = self.request.arguments.get('element')
                        code, message = Validate.i(
                                    bElement,
                                    'element',
                                    dataType=dict,
                                    maxLength=3,
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
                                    dataType=int,
                                    maxNumber=20000000,
                                    exception=0
                                )
                        if code != 4100:
                            raise Exception

                        '''
                            Number of Passengers travelling
                            Data Type: int
                            Max: 10
                            Min: 1
                        '''
                        code, message = Validate.i(
                                    bElement.get('passenger'),
                                    'element.passenger',
                                    dataType=int,
                                    maxNumber=10,
                                    minNumber=1
                                )
                        if code != 4100:
                            raise Exception

                        '''
                            Coupon Code
                            Data Type: ObjectId ( Mongo Row Id )
                        '''
                        try:
                            couponId = self.request.arguments.get('coupon')
                            if couponId:
                                couponId = ObjectId(couponId)
                        except:
                            couponId = None
                            code = 4620
                            message = 'Invalid argument - [ coupon ].'
                            raise Exception

                        if couponId:
                            # TODO: for validation
                            bCoupon = yield self.coupon.find(
                                        {
                                            '_id': couponId,
                                            'entityId': self.entityId
                                        },
                                        {
                                            '_id': 1,
                                            'code': 1,
                                            'absoluteDiscount': 1,
                                            'percentageDiscount': 1,
                                            'discountUpto': 1
                                        },
                                        limit=1
                                    )
                            if not len(bCoupon):
                                code = 4205
                                message = 'Coupon not found.'
                                raise Exception
                        else:
                            bCoupon = []

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
                                            'differentDays': 1,
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

                        try:
                            code = 4000
                            bRoutePoints = self.request.arguments.get('routePoints')
                            if bRoutePoints:
                                bRoutePoints = list(bRoutePoints)
                            else:
                                bRoutePoints = []
                                code = 3003
                                raise Exception

                            #print bRoutePoints
                            #self.write({})
                            #self.finish()
                            #return

                            for idx, br in enumerate(bRoutePoints):
                                sLat = br['lat']
                                code, message = Validate.i(
                                    sLat,
                                    'Latitude {0} '.format(idx),
                                    dataType=float,
                                    maxNumber=90,
                                    minNumber=-90
                                )
                                if code != 4100:
                                    raise Exception

                                sLng = br['lng']
                                code, message = Validate.i(
                                    sLng,
                                    'Longitude {0} '.format(idx),
                                    dataType=float,
                                    maxNumber=180,
                                    minNumber=-180
                                )
                                if code != 4100:
                                    raise Exception

                            #print bRoutePoints
                            #self.write({})
                            #self.finish()
                            #return
                        except Exception as e:
                            #print e
                            if code == 4000:
                                code = 4244
                                message = 'Invalid Argument - [ routePoints ].'
                                raise Exception
                            elif code != 3003:
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
                                if val > self.time + 15552000000000:
                                    code = 4192
                                    message = 'Invalid Argument - [ schedule.{0} ].'.format(idx)
                                    raise Exception
                            if vCat[0]['scheduleEndTime'] and len(bSchedule) < 2:
                                code = 4194
                                message = 'End time required in this Booking Category.'
                                raise Exception
                        try:
                            '''
                                On Demand ( Booking Now will directly go request to the drivers )
                            '''
                            if not len(bSchedule) and vCat[0]['onDemand']:
                                '''
                                    Getting All the Details of the Requestor
                                    Combines account, profile from BigBase
                                    If serviceAccount available it will on priority
                                '''
                                requestorAccount = yield self.account.find(
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
                                if not len(requestorAccount):
                                    code = 5150
                                    message =  'Requestor Account Not Found.'
                                    raise Exception
                                requestorAccount[0]['id'] = self.profileId
                                requestorAccount[0]['firstName'] = requestorAccount[0].get('firstName')
                                requestorAccount[0]['lastName'] = requestorAccount[0].get('lastName')
                                requestorAccount[0]['contact'] = requestorAccount[0].get('contact')
                                del requestorAccount[0]['_id']
                                rServiceAccount = yield self.serviceAccount.find(
                                        {
                                            'profileId': self.profileId,
                                            'entityId': self.entityId,
                                            'closed': False
                                        },
                                        {
                                            'firstName': 1,
                                            'lastName': 1
                                        },
                                        limit=1
                                )
                                if len(rServiceAccount):
                                    requestorAccount[0]['firstName'] = rServiceAccount[0].get('firstName')
                                    requestorAccount[0]['lastName'] = rServiceAccount[0].get('lastName')
                                '''
                                    Finding vehicles rearby
                                    Filters:
                                        1. 5KM ( 5000 mitre ) Max distance from start Point
                                        2. Entity Id
                                        3. Disabled False ( Active Vehicle )
                                        4. Last Location Update time with in 20 minutes ( in microseconds )
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
                                                '$gte': self.time - 1200000000
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
                                if not len(bRequested):
                                    code = 4220
                                    message = 'No Vehicle is available at this moment.'
                                    raise Exception
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
                                            'onDemand': True,
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
                                                    'coordinates': bEndPoint['coordinates']
                                                },
                                                {
                                                    'address': bEndPoint['address']
                                                }
                                            ],
                                            'driver': [],
                                            'route': bRoutePoints,
                                            'vehicle': [],
                                            'schedule': bSchedule,
                                            'fareCharge': [bFareCharge],
                                            'feedback': [],
                                            'payment': [
                                                bPayment
                                            ],
                                            'element': [
                                                bElement
                                            ],
                                            'vehicleType': vType,
                                            'category': vCat,
                                            'activity': [
                                                {
                                                    'id': 1,
                                                    'time': self.time,
                                                    'requested': bRequested
                                                }
                                            ],
                                            'coupon': bCoupon
                                        }
                                    )
                                '''
                                    Copying User Profile Picture
                                '''
                                fpu = self.fu.uploads + str(self.entityId) + '/profile/' + str(requestorAccount[0]['id']) + '/profile.png'
                                if os.path.exists(fpu):
                                    fbx = self.fu.uploads + str(self.entityId) + '/booking/' + str(bookingId) + '/' +\
                                            str(requestorAccount[0]['id'])
                                    fbuc = fbx + '/profile.png'
                                    os.system('mkdir -p ' + fbx)
                                    os.system('cp ' + fpu + ' ' + fbuc)
                                '''
                                    Converting ObjectId to string
                                '''
                                requestorAccount[0]['id'] = str(requestorAccount[0]['id'])
                                if len(requestorAccount[0]['contact']) > 1:
                                    requestorAccount[0]['contact'] = [requestorAccount[0]['contact'][0]]
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
                                                    'requestor': requestorAccount,
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
                                    Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                            channelId,
                                            liveBookingRequest
                                        )
                                    )

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
                            elif len(bSchedule):
                                '''
                                    Getting All the Details of the Requestor
                                    Combines account, profile from BigBase
                                    If serviceAccount available it will on priority
                                '''
                                requestorAccount = yield self.account.find(
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
                                if not len(requestorAccount):
                                    code = 5150
                                    message =  'Requestor Account Not Found.'
                                    raise Exception
                                requestorAccount[0]['id'] = self.profileId
                                requestorAccount[0]['firstName'] = requestorAccount[0].get('firstName')
                                requestorAccount[0]['lastName'] = requestorAccount[0].get('lastName')
                                requestorAccount[0]['contact'] = requestorAccount[0].get('contact')
                                del requestorAccount[0]['_id']
                                rServiceAccount = yield self.serviceAccount.find(
                                        {
                                            'profileId': self.profileId,
                                            'entityId': self.entityId,
                                            'closed': False
                                        },
                                        {
                                            'firstName': 1,
                                            'lastName': 1
                                        },
                                        limit=1
                                )
                                if len(rServiceAccount):
                                    requestorAccount[0]['firstName'] = rServiceAccount[0].get('firstName')
                                    requestorAccount[0]['lastName'] = rServiceAccount[0].get('lastName')
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
                                            'onDemand': False,
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
                                                    'coordinates': bEndPoint['coordinates']
                                                },
                                                {
                                                    'address': bEndPoint['address']
                                                }
                                            ],
                                            'driver': [],
                                            'vehicle': [],
                                            'route': bRoutePoints,
                                            'schedule': bSchedule,
                                            'fareCharge': [
                                                bFareCharge
                                            ],
                                            'feedback': [],
                                            'payment': [
                                                bPayment
                                            ],
                                            'element': [
                                                bElement
                                            ],
                                            'vehicleType': vType,
                                            'category': vCat,
                                            'activity': [
                                                {
                                                    'id': 1,
                                                    'time': self.time,
                                                    'requested': []
                                                }
                                            ]
                                        }
                                    )
                                '''
                                    Booking Request Sent for Publish to User
                                    Socket Code: 508191014
                                    Element:
                                     1. Message
                                     2. Booking Id
                                '''
                                liveBookingRequest = {
                                            'code': 508191014,
                                            'status': True,
                                            'message': 'Booking Request has been sent.',
                                            'result': [
                                                {
                                                    'bookingId': str(bookingId)
                                                }
                                            ]
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            self.profileId
                                    )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingRequest))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingRequest
                                    )
                                )

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
                                    code = 5280
                                    message = 'Internal Error Please Contact the Support Team.'
                            else:
                                code = 4401
                                message = 'Invalid Option.'
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
                    if self.apiId in [ 20216, 30216, 40216 ]: # TODO: till here

                        rActivityId = self.request.arguments.get('activityId')
                        code, message = Validate.i(
                                    rActivityId,
                                    'activityId',
                                    dataType=int,
                                    maxNumber=10,
                                    minNumber=1
                                )
                        if code != 4100:
                            raise Exception

                        '''
                            From Admin
                            Setting Booking Activity Status Confirmed
                            Activity Id = 2 ( Confirmd ).
                            Assigning Vehicle with Driver in that Booking
                        '''
                        if rActivityId == 2 and self.apiId == 20216:
                            try:
                                driverProfileId = ObjectId(self.request.arguments.get('driverId'))
                            except:
                                code = 4232
                                message = 'Invalid Argument - [ driverId ].'
                                raise Exception
                            # TODO: need add more filtering
                            driverProfile = yield self.profile.find(
                                        {
                                            '_id': driverProfileId,
                                            'entityId': self.entityId
                                        },
                                        {
                                            'accountId': 1,
                                            '_id': 0
                                        },
                                        limit=1
                                    )
                            if not len(driverProfile):
                                code = 4232
                                message = 'Driver not found.'
                                raise Exception
                            '''
                                Getting All the Details of the Requestor
                                Combines account, profile from BigBase
                                If serviceAccount available it will on priority
                            '''
                            requestorAccount = yield self.account.find(
                                                {
                                                    '_id': driverProfile[0]['accountId']
                                                },
                                                {
                                                    '_id': 1,
                                                    'firstName': 1,
                                                    'lastName': 1,
                                                    'contact': 1
                                                },
                                                limit=1
                                            )
                            if not len(requestorAccount):
                                code = 5150
                                message =  'Requestor Driver Account Not Found.'
                                raise Exception
                            requestorAccount[0]['id'] = driverProfileId
                            requestorAccount[0]['firstName'] = requestorAccount[0].get('firstName')
                            requestorAccount[0]['lastName'] = requestorAccount[0].get('lastName')
                            requestorAccount[0]['contact'] = requestorAccount[0].get('contact')
                            del requestorAccount[0]['_id']
                            rServiceAccount = yield self.serviceAccount.find(
                                    {
                                        'profileId': driverProfileId,
                                        'entityId': self.entityId
                                    },
                                    {
                                        'firstName': 1,
                                        'lastName': 1
                                    },
                                    limit=1
                            )
                            if len(rServiceAccount):
                                requestorAccount[0]['firstName'] = rServiceAccount[0].get('firstName')
                                requestorAccount[0]['lastName'] = rServiceAccount[0].get('lastName')
                            '''
                                Searching for his assigned vehicle
                            '''
                            rVehicle = yield self.vehicle.find(
                                    {
                                        'disabled': False,
                                        'entityId': self.entityId,
                                        'driverId': driverProfileId
                                    },
                                    {
                                        '_id': 1,
                                        'registrationNumber': 1,
                                        'location': 1,
                                        'make': 1,
                                        'model': 1,
                                        'color': 1
                                    },
                                    limit=1
                                )
                            if not len(rVehicle):
                                code = 4233
                                message = 'You are assigned to this vehicle.'
                                raise Exception
                            else:
                                rVehicle[0]['id'] = rVehicle[0]['_id']
                                del rVehicle[0]['_id']

                            '''
                                Searching for Booking:
                                Filters:
                                 1. Row Id ( bookingId )
                                 2. Entity Id
                                 3. Activity length 1 ( State is Requested id = 1 ),
                                 4. Driver Id  should be there in requested.
                                 5. Reuested time should be with in 80 seconds ( in microseconds).
                                Updates:
                                 1. Driver .
                                 2. Vehicle .
                                 3. Activity State 1 -> 2 ( Confirm ) .
                                 5. Deleting the Driver and Vehicle from activity.0.requested .
                            '''
                            try:
                                rBookingId = ObjectId(self.request.arguments['bookingId'])
                            except:
                                code = 4132
                                message = 'Invalid Argument - [ bookingId ].'
                                raise Exception
                            '''
                                Copying Driver Profile Picture
                            '''
                            fpu = self.fu.uploads + str(self.entityId) + '/profile/' + str(requestorAccount[0]['id']) + '/profile.png'
                            if os.path.exists(fpu):
                                fbx = self.fu.uploads + str(self.entityId) + '/booking/' + str(rBookingId) + '/' +\
                                        str(requestorAccount[0]['id'])
                                fbuc = fbx + '/profile.png'
                                os.system('mkdir -p ' + fbx)
                                os.system('cp ' + fpu + ' ' + fbuc)
                                os.system('chmod 755 -R ' + self.fu.uploads + '*')
                            else:
                                fbuc = fpu

                            nConfirmCode = randint(1000, 9999)
                            rBookingConfirmResult = yield self.booking.find_and_modify(
                                        query=
                                        {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id == 1'
                                        },
                                        update=
                                        {
                                            '$set': {
                                                'driver': requestorAccount,
                                                'vehicle': rVehicle,
                                            },
                                            '$push':
                                            {
                                                'activity':
                                                {
                                                    'id': 2,
                                                    'time': self.time,
                                                    'coordinates': rVehicle[0]['location'][0]['coordinates'],
                                                    'code': nConfirmCode
                                                }
                                            }
                                        },
                                        fields=
                                        {
                                            '_id': 0,
                                            'requestor': 1
                                        },
                                        limit=1
                                    )
                            if not rBookingConfirmResult:
                                code = 4210
                                message = 'Request Booking is not available.'
                                raise Exception
                            else:
                                '''
                                    Converting ObjectId to string
                                '''
                                bookingRequestorId = rBookingConfirmResult['requestor'][0]['id']
                                '''
                                    Publishing to the Booking Requestor ( USER )
                                    Confirm Socket Id: 1408191152
                                '''
                                message = 'Your Booking bas been confirmed.'
                                liveBookingConfirm = {
                                            'code': 1408191152,
                                            'status': True,
                                            'message': message,
                                            'result': [
                                                str(rBookingId)
                                            ]
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            bookingRequestorId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingConfirm))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingConfirm
                                    )
                                )

                                '''
                                    Publishing to the Booking Requested ( DRIVER )
                                    Confirm Socket Id: 1408191154
                                '''
                                message = 'Your Booking bas been confirmed.'
                                liveBookingConfirm = {
                                            'code': 1408191154,
                                            'status': True,
                                            'message': message,
                                            'result': [
                                                str(rBookingId)
                                            ]
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            driverProfileId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingConfirm))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingConfirm
                                    )
                                )

                                status = True
                                code = 2000
                        elif rActivityId == 2 and self.apiId == 30216:
                            '''
                                From Driver
                                Setting Booking Activity Status Confirmed
                                Activity Id = 2 ( Confirmd ).
                                Assigning Vehicle with Driver in that Booking

                                Getting All the Details of the Requestor
                                Combines account, profile from BigBase
                                If serviceAccount available it will on priority
                            '''
                            requestorAccount = yield self.account.find(
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
                            if not len(requestorAccount):
                                code = 5150
                                message =  'Requestor Driver Account Not Found.'
                                raise Exception
                            requestorAccount[0]['id'] = self.profileId
                            requestorAccount[0]['firstName'] = requestorAccount[0].get('firstName')
                            requestorAccount[0]['lastName'] = requestorAccount[0].get('lastName')
                            requestorAccount[0]['contact'] = requestorAccount[0].get('contact')
                            del requestorAccount[0]['_id']
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
                                requestorAccount[0]['firstName'] = rServiceAccount[0].get('firstName')
                                requestorAccount[0]['lastName'] = rServiceAccount[0].get('lastName')
                            '''
                                Searching for his assigned vehicle
                            '''
                            rVehicle = yield self.vehicle.find(
                                    {
                                        'disabled': False,
                                        'entityId': self.entityId,
                                        'driverId': self.profileId
                                    },
                                    {
                                        '_id': 1,
                                        'registrationNumber': 1,
                                        'location': 1,
                                        'make': 1,
                                        'model': 1,
                                        'color': 1
                                    },
                                    limit=1
                                )
                            if not len(rVehicle):
                                code = 4233
                                message = 'You are assigned to this vehicle.'
                                raise Exception
                            else:
                                rVehicle[0]['id'] = rVehicle[0]['_id']
                                del rVehicle[0]['_id']

                            '''
                                Searching for Booking:
                                Filters:
                                 1. Row Id ( bookingId )
                                 2. Entity Id
                                 3. Activity length 1 ( State is Requested id = 1 ),
                                 4. Driver Id  should be there in requested.
                                 5. Reuested time should be with in 80 seconds ( in microseconds).
                                Updates:
                                 1. Driver .
                                 2. Vehicle .
                                 3. Activity State 1 -> 2 ( Confirm ) .
                                 5. Deleting the Driver and Vehicle from activity.0.requested .
                            '''
                            try:
                                rBookingId = ObjectId(self.request.arguments['bookingId'])
                            except:
                                code = 4132
                                message = 'Invalid Argument - [ bookingId ].'
                                raise Exception
                            '''
                                Copying Driver Profile Picture
                            '''
                            fpu = self.fu.uploads + str(self.entityId) + '/profile/' + str(requestorAccount[0]['id']) + '/profile.png'
                            if os.path.exists(fpu):
                                fbx = self.fu.uploads + str(self.entityId) + '/booking/' + str(rBookingId) + '/' +\
                                        str(requestorAccount[0]['id'])
                                fbuc = fbx + '/profile.png'
                                os.system('mkdir -p ' + fbx)
                                os.system('cp ' + fpu + ' ' + fbuc)
                                os.system('chmod 755 -R ' + self.fu.uploads + '*')
                            else:
                                fbuc = fpu

                            nConfirmCode = randint(1000, 9999)
                            rBookingConfirmResult = yield self.booking.find_and_modify(
                                        query=
                                        {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id == 1',
                                            'activity.0.time':
                                            {
                                                '$gt': self.time - 20000000
                                            },
                                            'activity.0.requested.driverId': self.profileId
                                        },
                                        update=
                                        {
                                            '$set': {
                                                'driver': requestorAccount,
                                                'vehicle': rVehicle,
                                            },
                                            '$push':
                                            {
                                                'activity':
                                                {
                                                    'id': 2,
                                                    'time': self.time,
                                                    'coordinates': rVehicle[0]['location'][0]['coordinates'],
                                                    'code': nConfirmCode
                                                }
                                            }
                                        },
                                        fields=
                                        {
                                            '_id': 0,
                                            'startPoint': 1,
                                            'endPoint': 1,
                                            'payment': 1,
                                            'element': 1,
                                            'vehicleType': 1,
                                            'category': 1,
                                            'requestor': 1,
                                            'route': 1
                                        }
                                    )
                            if not rBookingConfirmResult:
                                code = 4210
                                message = 'Request Booking is not available.'
                                raise Exception
                            rRemovedFromRequestedResult = yield self.booking.update(
                                        {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            'driver.0.id': self.profileId,
                                            'activity.1.time': self.time
                                        },
                                        {
                                            '$pull':
                                            {
                                                'activity.0.requested':
                                                {
                                                    'driverId': self.profileId
                                                }
                                            }
                                        }
                                    )
                            if rRemovedFromRequestedResult['n']:
                                '''
                                    Converting ObjectId to string
                                '''
                                requestorAccount[0]['id'] = str(requestorAccount[0]['id'])
                                if len(requestorAccount[0]['contact']) > 1:
                                    requestorAccount[0]['contact'] = [requestorAccount[0]['contact'][0]]
                                rVehicle[0]['id'] = str(rVehicle[0]['id'])
                                rBookingConfirmResult['category'][0]['id'] = \
                                        str(rBookingConfirmResult['category'][0]['id'])
                                rBookingConfirmResult['vehicleType'][0]['id'] = \
                                        str(rBookingConfirmResult['category'][0]['id'])
                                bookingRequestorId = rBookingConfirmResult['requestor'][0]['id']
                                del rBookingConfirmResult['requestor']
                                '''
                                    Publishing to the Booking Requestor
                                    COnfirm Socket Id: 2707190739
                                '''
                                message = 'Your Booking bas been confirmed.'
                                liveBookingConfirm = {
                                            'code': 2707190739,
                                            'status': True,
                                            'message': message,
                                            'result': [
                                                rBookingConfirmResult
                                            ]
                                        }
                                liveBookingConfirm['result'][0]['bookingId'] = str(rBookingId)
                                liveBookingConfirm['result'][0]['vehicle'] = rVehicle
                                liveBookingConfirm['result'][0]['time'] = self.time
                                liveBookingConfirm['result'][0]['confirmCode'] = nConfirmCode
                                # Adding driver profile picture
                                fpD = fbuc.replace(self.fu.uploads, self.fu.uploadsPath)
                                requestorAccount[0]['profilePicture'] = fpD

                                liveBookingConfirm['result'][0]['driver'] = requestorAccount

                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            bookingRequestorId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingConfirm))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingConfirm
                                    )
                                )

                                status = True
                                code = 2000
                        elif rActivityId == 3 and self.apiId == 30216:

                            '''
                                Searching for Booking:
                                Filters:
                                 1. Row Id ( bookingId )
                                 2. Entity Id
                                 3. Activity length 2 ( State is Confirmed id = 2 ),
                                 4. Driver Id  should be there in the Booking.
                                Updates:
                                 1. Latest Vehicle Location.
                                 2. Activity State 2 -> 3 ( Arrived ) .
                            '''

                            try:
                                rBookingId = ObjectId(self.request.arguments['bookingId'])
                            except:
                                code = 4132
                                message = 'Invalid Argument - [ bookingId ].'
                                raise Exception

                            '''
                                Searching for his assigned vehicle
                                Last update time with in 20 Minutes ( in microseconds )
                            '''

                            rVehicle = yield self.vehicle.find(
                                    {
                                        'disabled': False,
                                        'entityId': self.entityId,
                                        'driverId': self.profileId
                                    },
                                    {
                                        '_id': 1,
                                        'location': 1
                                    },
                                    limit=1
                                )
                            if not len(rVehicle):
                                code = 4233
                                message = 'You are assigned to this vehicle.'
                                raise Exception

                            rBooking = yield self.booking.find(
                                        {
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id > 2 && this.activity[this.activity.length - 1].id < 5',
                                            'driver.0.id': self.profileId
                                        },
                                        {
                                            '_id': 1
                                        },
                                        limit=1
                                    )
                            if len(rBooking):
                                code = 4610
                                message = 'You are already in another Booking.'
                                raise Exception
                            else:
                                rBooking = yield self.booking.find(
                                        {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            'driver.0.id': self.profileId
                                        },
                                        {
                                            '_id': 0,
                                            'startPoint': 1,
                                            'requestor': 1,
                                            'schedule': 1
                                        },
                                        limit=1
                                    )
                                if not len(rBooking):
                                    code = 4745
                                    message = 'This Booking is not available.'
                                    raise Exception
                            #elif len(rBooking[0]['schedule'])

                            '''
                                Last Location Update Time should be with in 20 minutes ( in microseconds )
                            '''
                            if rVehicle[0]['location'][1]['time'] < self.time - 1200000000:
                                code = 4140
                                message = 'Your Location is not updated.'
                                raise Exception

                            orgLatLng = (rVehicle[0]['location'][0]['coordinates'][1],
                                    rVehicle[0]['location'][0]['coordinates'][0])
                            destLatLng = (rBooking[0]['startPoint'][0]['coordinates'][1],
                                    rBooking[0]['startPoint'][0]['coordinates'][0])
                            '''
                                Distance Should be within 800 metres
                            '''
                            # TODO: for the distance
                            diffDistance = int(great_circle(orgLatLng, destLatLng).m)
                            if diffDistance > 800:
                                code = 4150
                                message = 'Please reach the Start Location First.'
                                raise Exception
                            rArrivedResult = yield self.booking.update(
                                    {
                                        '_id': rBookingId
                                    },
                                    {
                                        '$push':
                                        {
                                            'activity':
                                            {
                                                'id': 3,
                                                'time': self.time,
                                                'distance': diffDistance,
                                                'coordinates': rVehicle[0]['location'][0]['coordinates']
                                            }
                                        }
                                    }
                                )
                            if rArrivedResult['n']:
                                '''
                                    Publishing to the Booking Requestor
                                    Arrival alert Socket Id: 2907190703
                                '''
                                bookingRequestorId = rBooking[0]['requestor'][0]['id']
                                liveBookingConfirm = {
                                            'code': 2907190703,
                                            'status': True,
                                            'message': 'Your Vehicle has Arrived on your Location.',
                                            'result': []
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            bookingRequestorId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingConfirm))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingConfirm
                                    )
                                )

                                code = 2000
                                status = True
                                message = 'You have Arrived on the Start Location.'
                            else:
                                code = 4243
                                message = 'This Booking is not available.'

                        elif rActivityId == 4 and self.apiId == 30216:

                            '''
                                Searching for Booking:
                                Filters:
                                 1. Row Id ( bookingId )
                                 2. Entity Id
                                 3. Activity length 3 ( State is Arrived id = 3 ),
                                 4. Driver Id  should be there in the Booking.
                                 5. OTP should match.
                                Updates:
                                 1. Latest Vehicle Location.
                                 2. Activity State 3 -> 4 ( In Progress ) .
                            '''

                            try:
                                rBookingId = ObjectId(self.request.arguments['bookingId'])
                            except:
                                code = 4132
                                message = 'Invalid Argument - [ bookingId ].'
                                raise Exception

                            '''
                                OTP which send to the user
                            '''
                            cOtp = self.request.arguments.get('otp')
                            code, message = Validate.i(
                                    cOtp,
                                    'OTP',
                                    dataType=int,
                                    minLength=4,
                                    maxLength=4
                                )
                            if code != 4100:
                                raise Exception


                            '''
                                Searching for his assigned vehicle
                                Last update time with in 20 Minutes ( in microseconds )
                            '''

                            rVehicle = yield self.vehicle.find(
                                    {
                                        'disabled': False,
                                        'entityId': self.entityId,
                                        'driverId': self.profileId
                                    },
                                    {
                                        '_id': 1,
                                        'location': 1
                                    },
                                    limit=1
                                )
                            if not len(rVehicle):
                                code = 4233
                                message = 'You are assigned to this vehicle.'
                                raise Exception

                            rBooking = yield self.booking.find(
                                        {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id == 3',
                                            'activity.1.code': cOtp,
                                            'driver.0.id': self.profileId
                                        },
                                        {
                                            '_id': 0,
                                            'startPoint': 1,
                                            'requestor': 1
                                        },
                                        limit=1
                                    )
                            if not len(rBooking):
                                code = 4243
                                message = 'Booking is not available.'
                                raise Exception

                            '''
                                Last Location Update Time should be with in 20 minutes ( in microseconds )
                            '''
                            if rVehicle[0]['location'][1]['time'] < self.time - 1200000000:
                                code = 4140
                                message = 'Your Location is not updated.'
                                raise Exception

                            orgLatLng = (rVehicle[0]['location'][0]['coordinates'][1],
                                    rVehicle[0]['location'][0]['coordinates'][0])
                            destLatLng = (rBooking[0]['startPoint'][0]['coordinates'][1],
                                    rBooking[0]['startPoint'][0]['coordinates'][0])
                            '''
                                Distance from the start point
                            '''
                            diffDistance = int(great_circle(orgLatLng, destLatLng).m)
                            if diffDistance > 800:
                                code = 4150
                                message = 'Please reach the Start Location First.'
                                raise Exception
                            rStartedResult = yield self.booking.update(
                                    {
                                        '_id': rBookingId
                                    },
                                    {
                                        '$push':
                                        {
                                            'activity':
                                            {
                                                'id': 4,
                                                'time': self.time,
                                                'distance': diffDistance,
                                                'coordinates': rVehicle[0]['location'][0]['coordinates']
                                            }
                                        }
                                    }
                                )
                            if rStartedResult['n']:
                                '''
                                    Publishing to the Booking Requestor
                                    Trip Start alert Socket Id: 3007190148
                                '''
                                bookingRequestorId = rBooking[0]['requestor'][0]['id']
                                liveBookingStarted = {
                                            'code': 3007190148,
                                            'status': True,
                                            'message': 'Your Trip has started, Happy Journey.',
                                            'result': []
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            bookingRequestorId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingStarted))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingStarted
                                    )
                                )

                                code = 2000
                                status = True
                                message = 'Your Trip has started.'
                            else:
                                code = 5220
                                message = 'Internal Error Please Contact the Support Team.'

                        elif rActivityId == 5 and self.apiId == 30216:

                            '''
                                Searching for Booking:
                                Filters:
                                 1. Row Id ( bookingId )
                                 2. Entity Id
                                 3. Activity length 4 ( State is In Progress id = 4 ),
                                 4. Driver Id  should be there in the Booking.
                                Updates:
                                 1. Latest Vehicle Location.
                                 2. Activity State 4 -> 5 ( Reached ) .
                            '''

                            try:
                                rBookingId = ObjectId(self.request.arguments['bookingId'])
                            except:
                                code = 4132
                                message = 'Invalid Argument - [ bookingId ].'
                                raise Exception

                            '''
                                If true means Driver didn't reached the desinarion but
                                requesting to stop the trip
                            '''
                            try:
                                rForce = bool(self.request.arguments['force'])
                            except:
                                rForce = False

                            if rForce:
                                rForceData = self.request.arguments.get('data')
                                code, message = Validate.i(
                                        rForceData,
                                        'data',
                                        dataType=list,
                                        minLength=1,
                                        maxLength=1
                                    )
                                if code != 4100:
                                    raise Exception
                                code, message = Validate.i(
                                        rForceData[0],
                                        'data.0',
                                        dataType=dict,
                                        minLength=2,
                                        maxLength=2
                                    )
                                if code != 4100:
                                    raise Exception
                                '''
                                    Reason why he want to stop the trip
                                    Type: string
                                    Required: Yes
                                '''
                                code, message = Validate.i(
                                        rForceData[0].get('reason'),
                                        'data.0.reason',
                                        dataType=unicode,
                                        noSpecial=True,
                                        minLength=5,
                                        maxLength=180
                                    )
                                if code != 4100:
                                    raise Exception
                                '''
                                    Description why he want to stop the trip
                                    Type: string
                                    Required: no
                                '''
                                code, message = Validate.i(
                                        rForceData[0].get('description'),
                                        'data.0.description',
                                        dataType=unicode,
                                        maxLength=350
                                    )
                                if code != 4100:
                                    raise Exception
                            else:
                                rForceData = []

                            '''
                                Full Trip Distance from Start Point -> End Point
                                Distance taken from Driver Application
                                Data Type: long, int
                                Unit: metre
                                Max: 100,000,000
                                Min: 0
                            '''
                            cDistance = self.request.arguments.get('distance')
                            code, message = Validate.i(
                                    cDistance,
                                    'Distance',
                                    dataType=int,
                                    minNumber=0,
                                    maxNumber=100000000
                                )
                            if code != 4100:
                                raise Exception

                            '''
                                Searching for his assigned vehicle
                                Last update time with in 20 Minutes ( in microseconds )
                            '''

                            rVehicle = yield self.vehicle.find(
                                    {
                                        'disabled': False,
                                        'entityId': self.entityId,
                                        'driverId': self.profileId
                                    },
                                    {
                                        '_id': 1,
                                        'location': 1
                                    },
                                    limit=1
                                )
                            if not len(rVehicle):
                                code = 4233
                                message = 'You are assigned to this vehicle.'
                                raise Exception

                            rBooking = yield self.booking.find(
                                        {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id == 4',
                                            'driver.0.id': self.profileId
                                        },
                                        {
                                            '_id': 0,
                                            'endPoint': 1,
                                            'requestor': 1,
                                            'element': 1,
                                            'category': 1,
                                            'fareCharge': 1,
                                            'activity': 1,
                                            'coupon': 1
                                        },
                                        limit=1
                                    )
                            if not len(rBooking):
                                code = 4243
                                message = 'Booking is not available.'
                                raise Exception
                            '''
                                All the Payment and Distance Calculation should be here
                            '''
                            cCategory = rBooking[0]['category']
                            cDifferentDays = rBooking[0]['category'][0]['differentDays']

                            cFareCharge = rBooking[0]['fareCharge'][0]
                            cTotalPrice = 0L

                            cBaseKm = rBooking[0]['fareCharge'][0]['baseKm']
                            if cBaseKm == 0:
                                del cFareCharge['baseKm']
                            cPerKmRate = rBooking[0]['fareCharge'][0]['perKmRate']
                            if cPerKmRate == 0:
                                del cFareCharge['perKmRate']
                            cCancellationCharge = rBooking[0]['fareCharge'][0]['cancellationCharge']
                            if cCancellationCharge == 0:
                                del cFareCharge['cancellationCharge']
                            cWaitingCharge = rBooking[0]['fareCharge'][0]['waitingCharge']
                            if cWaitingCharge == 0:
                                del cFareCharge['waitingCharge']
                            cBaseHour = rBooking[0]['fareCharge'][0]['baseHour']
                            if cBaseHour == 0:
                                del cFareCharge['baseHour']
                            cNightHoldCharge = rBooking[0]['fareCharge'][0]['nightHoldCharge']
                            if cNightHoldCharge == 0:
                                del cFareCharge['nightHoldCharge']
                            cBasePrice = rBooking[0]['fareCharge'][0]['basePrice']
                            if cBasePrice == 0:
                                del cFareCharge['basePrice']
                            cPerHourRate = rBooking[0]['fareCharge'][0]['perHourRate']
                            if cPerHourRate == 0:
                                del cFareCharge['perHourRate']
                            cMaxPassenger = rBooking[0]['fareCharge'][0]['maxPassenger']
                            if cMaxPassenger == 0:
                                del cFareCharge['maxPassenger']

                            cPassenger = rBooking[0]['element'][0]['passenger']
                            cDuration = self.time - rBooking[0]['activity'][3]['time']


                            cBaseAdded = False
                            '''
                                Calculated from Start -> End Distance
                                Per KM Cost
                                Algo: distance x rate
                            '''
                            if cBaseKm > 0:
                                distInKm = (cDistance / 1000)
                                distInKmInt = int(distInKm)
                                distInKmEx = distInKm - distInKmInt
                                if distInKmEx > 0.4:
                                    distInKmInt = distInKmInt + 1
                                if distInKmInt > cBaseKm:
                                    value = (distInKmInt - cBaseKm) * cPerKmRate
                                    if value > 0:
                                        cTotalPrice = cTotalPrice + value + cBasePrice
                                        cBaseAdded = True
                            '''
                                Calculated from Arival Time -> Start Time
                                Per Min Cost
                                Algo: min x rate
                            '''
                            if cWaitingCharge > 0:
                                aTime = rBooking[0]['activity'][2]['time']
                                sTime = rBooking[0]['activity'][3]['time']
                                # Microseconds to Minute
                                tDiffInMin = int((sTime - aTime) / 1000 / 1000 / 60)
                                if tDiffInMin:
                                    value = tDiffInMin * cWaitingCharge
                                    if value:
                                        cTotalPrice = cTotalPrice + value

                            '''
                                Calculated from Start Time -> End Time
                                Per Hour Cost
                                Algo: hour x rate
                            '''
                            if cBaseHour > 0:
                                # Microseconds to Hour
                                tDiffInHour = ((cDuration) / 1000 / 1000 / 60 / 60)
                                tDiffInHourInt = int(tDiffInHour)
                                tDiffInHourEx = tDiffInHour - tDiffInHourInt
                                if tDiffInHourEx > 0.4:
                                    tDiffInHourInt = tDiffInHourInt + 1

                                if tDiffInHourInt > cBaseHour:
                                    value = (tDiffInHourInt - cBaseHour) * cPerHourRate
                                    if value:
                                        cTotalPrice = cTotalPrice + value
                                        if not cBaseAdded:
                                            cTotalPrice = cTotalPrice + cBasePrice
                                            cBaseAdded = True

                            '''
                                Calculated from Start Time -> End Time
                                Per day Cost
                                Algo: date x rate
                            '''
                            if cDifferentDays:
                                # Microseconds to Hour
                                tDiffInDay = ((cDuration) / 1000 / 1000 / 60 / 60 / 24)
                                tDiffInDayInt = int(tDiffInDay)
                                tDiffInDayEx = round(tDiffInDay - tDiffInDayInt, 1)
                                if tDiffInDayEx > 0.1:
                                    tDiffInDayInt = tDiffInDayInt + 1
                                if tDiffInDayInt > 0:
                                    if cBaseAdded:
                                        value = (tDiffInDayInt - 1) * cBasePrice
                                    else:
                                        value = tDiffInDayInt * cBasePrice
                                    cTotalPrice = cTotalPrice + value

                                    value = tDiffInDayInt * nightHoldCharge
                                    cTotalPrice = cTotalPrice + value

                            # TODO: for now
                            #if key == 'cancellationCharge' and value:
                            #    Log.i('TODO', 'For Cancellation Charge')

                            # TODO: foe now
                            #if key == 'maxPassenger' and value:
                            #    Log.i('TODO', 'For Max Passenger')

                            if cTotalPrice < cBasePrice:
                                cTotalPrice = cBasePrice

                            '''
                                Calculating Coupon Discounts
                            '''
                            cCoupon = rBooking[0]['coupon']
                            cTotalDiscount = 0L
                            if len(cCoupon):
                                for idx, val in enumerate(cCoupon):
                                    if val['percentageDiscount'] > 0:
                                        pds = (cTotalPrice / 100) * val['percentageDiscount']
                                        cTotalDiscount = cTotalDiscount + pds
                                    elif val['absoluteDiscount'] > 0:
                                        ads = val['absoluteDiscount']
                                        cTotalDiscount = cTotalDiscount + ads

                                    # Set to max discount
                                    if cTotalDiscount > val['discountUpto']:
                                        cTotalDiscount = val['discountUpto']

                            # Round Up Discount
                            if cTotalDiscount > 0:
                                cTotal = long(cTotalDiscount)
                                if (cTotalDiscount - cTotal) > 0.5:
                                    cTotalDiscount = long(cTotalDiscount + 1)

                            # Round up Total price
                            rTotal = long(cTotalPrice)
                            if (cTotalPrice - rTotal) > 0.5:
                                cTotalPrice = long(cTotalPrice + 1)
                            else:
                                cTotalPrice = long(cTotalPrice)

                            '''
                                Last Location Update Time should be with in 20 minutes ( in microseconds )
                            '''
                            if rVehicle[0]['location'][1]['time'] < self.time - 1200000000:
                                code = 4140
                                message = 'Your Location is not updated.'
                                raise Exception

                            orgLatLng = (rVehicle[0]['location'][0]['coordinates'][1],
                                    rVehicle[0]['location'][0]['coordinates'][0])
                            destLatLng = (rBooking[0]['endPoint'][0]['coordinates'][1],
                                    rBooking[0]['endPoint'][0]['coordinates'][0])
                            '''
                                Distance from the End point
                            '''
                            # TODO: for now
                            diffDistance = int(great_circle(orgLatLng, destLatLng).m)
                            if diffDistance > 800 and not rForce:
                                code = 4150
                                message = 'Please reach the End Location First.'
                                raise Exception
                            rStartedResult = yield self.booking.update(
                                    {
                                        '_id': rBookingId
                                    },
                                    {
                                        '$push':
                                        {
                                            'activity':
                                            {
                                                'id': 5,
                                                'time': self.time,
                                                'force': rForce,
                                                'data': rForceData,
                                                'distance': diffDistance,
                                                'coordinates': rVehicle[0]['location'][0]['coordinates']
                                            },
                                            'fareCharge': cFareCharge,
                                            'payment':
                                            {
                                                '$each':
                                                [
                                                    {
                                                        'price': cTotalPrice,
                                                        'type': 0,
                                                        'variation': 0
                                                    },
                                                    {
                                                        'price': (cTotalPrice - cTotalDiscount),
                                                        'type': 0,
                                                        'variation': cTotalDiscount
                                                    }
                                                ]

                                            },
                                            'element':
                                            {
                                                'duration': cDuration,
                                                'distance': cDistance,
                                                'passenger': cPassenger
                                            }
                                        }
                                    }
                                )
                            if rStartedResult['n']:
                                '''
                                    Publishing to the Booking Requestor
                                    Trip Start alert Socket Id: 3007190323
                                '''
                                message =  'You have reached your destination.'
                                bookingRequestorId = rBooking[0]['requestor'][0]['id']
                                liveBookingStarted = {
                                            'code': 3007190323,
                                            'status': True,
                                            'message': message,
                                            'result': [str(rBookingId)]
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            bookingRequestorId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingStarted))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingStarted
                                    )
                                )
                                code = 2000
                                status = True
                            else:
                                code = 5220
                                message = 'Internal Error Please Contact the Support Team.'
                        elif rActivityId == 6 and self.apiId == 30216:

                            '''
                                Searching for Booking:
                                Filters:
                                 1. Row Id ( bookingId )
                                 2. Entity Id
                                 3. Activity length 5 ( State is Reached id = 5 ),
                                 4. Driver Id  should be there in the Booking.
                                Updates:
                                 1. Latest Vehicle Location.
                                 2. Activity State 5 -> 6 ( Paid ) .
                            '''

                            try:
                                rBookingId = ObjectId(self.request.arguments['bookingId'])
                            except:
                                code = 4132
                                message = 'Invalid Argument - [ bookingId ].'
                                raise Exception

                            '''
                                Searching for his assigned vehicle
                                Last update time with in 20 Minutes ( in microseconds )
                            '''

                            rVehicle = yield self.vehicle.find(
                                    {
                                        'disabled': False,
                                        'entityId': self.entityId,
                                        'driverId': self.profileId
                                    },
                                    {
                                        '_id': 1,
                                        'location': 1
                                    },
                                    limit=1
                                )
                            if not len(rVehicle):
                                code = 4233
                                message = 'You are assigned to this vehicle.'
                                raise Exception

                            rBooking = yield self.booking.find(
                                        {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id == 5',
                                            'driver.0.id': self.profileId
                                        },
                                        {
                                            '_id': 0,
                                            'requestor': 1
                                        },
                                        limit=1
                                    )
                            if not len(rBooking):
                                code = 4243
                                message = 'Booking is not available.'
                                raise Exception

                            '''
                                Last Location Update Time should be with in 20 minutes ( in microseconds )
                            '''
                            if rVehicle[0]['location'][1]['time'] < self.time - 1200000000:
                                code = 4140
                                message = 'Your Location is not updated.'
                                raise Exception

                            rPaidResult = yield self.booking.update(
                                    {
                                        '_id': rBookingId
                                    },
                                    {
                                        '$push':
                                        {
                                            'activity':
                                            {
                                                'id': 6,
                                                'time': self.time
                                            }
                                        }
                                    }
                                )
                            if rPaidResult['n']:
                                '''
                                    Publishing to the Booking Requestor
                                    Payment alert Socket Id: 3007190334
                                '''
                                message =  'Your Booking Payment is Complete.'
                                bookingRequestorId = rBooking[0]['requestor'][0]['id']
                                liveBookingPaid = {
                                            'code': 3007190334,
                                            'status': True,
                                            'message': message,
                                            'result': []
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            bookingRequestorId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingPaid))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingPaid
                                    )
                                )
                                code = 2000
                                status = True
                            else:
                                code = 5220
                                message = 'Internal Error Please Contact the Support Team.'

                        elif rActivityId == 7 and self.apiId == 40216:

                            '''
                                Searching for Booking:
                                Filters:
                                 1. Row Id ( bookingId )
                                 2. Entity Id
                                 3. Activity 7 ( State is Paid id = 6 ),
                                 4. Driver Id  should be there in the Booking.
                                Updates:
                                 1. Feedback index 0.
                            '''

                            try:
                                rBookingId = ObjectId(self.request.arguments['bookingId'])
                            except:
                                code = 4132
                                message = 'Invalid Argument - [ bookingId ].'
                                raise Exception

                            '''
                                Rating of the Feedback from User
                            '''
                            fRating = self.request.arguments.get('rating')
                            code, message = Validate.i(
                                    fRating,
                                    'Rating',
                                    dataType=int,
                                    minNumber=1,
                                    maxLength=4
                                )
                            if code != 4100:
                                raise Exception

                            '''
                                Description of the Feedback from User
                            '''
                            fDescription = self.request.arguments.get('description')
                            code, message = Validate.i(
                                    fDescription,
                                    'Description',
                                    dataType=unicode,
                                    minLength=0,
                                    maxLength=120
                                )
                            if code != 4100:
                                raise Exception

                            rFeedbackResult = yield self.booking.find_and_modify(
                                        query =
                                        {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id == 6',
                                            '$where': 'this.feedback[0] == null',
                                            'requestor.0.id': self.profileId
                                        },
                                        update =
                                        {
                                            '$set':
                                            {
                                                'feedback.0':
                                                {
                                                    'rating': fRating,
                                                    'description': fDescription
                                                }
                                            }
                                        },
                                        fields =
                                        {
                                            '_id': 0,
                                            'requestor': 1
                                        }
                                )
                            if rFeedbackResult:
                                '''
                                    Publishing to the Booking Requestor
                                    Payment alert Socket Id: 3007190624
                                '''
                                message =  'Thank you for using Our Service.'
                                bookingRequestorId = rFeedbackResult['requestor'][0]['id']
                                liveBookingPaid = {
                                            'code': 3007190624,
                                            'status': True,
                                            'message': message,
                                            'result': []
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            bookingRequestorId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingPaid))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingPaid
                                    )
                                )

                                code = 2000
                                status = True
                            else:
                                code = 5220
                                message = 'Booking is not available.'
                        elif rActivityId == 8 and self.apiId == 30216:

                            '''
                                Searching for Booking:
                                Filters:
                                 1. Row Id ( bookingId )
                                 2. Entity Id
                                 3. Activity 8 ( State is Paid id = 6 ),
                                 4. Driver Id  should be there in the Booking.
                                Updates:
                                 1. Feedback index 0.
                            '''

                            try:
                                rBookingId = ObjectId(self.request.arguments['bookingId'])
                            except:
                                code = 4132
                                message = 'Invalid Argument - [ bookingId ].'
                                raise Exception

                            '''
                                Rating of the Feedback from Driver
                            '''
                            fRating = self.request.arguments.get('rating')
                            code, message = Validate.i(
                                    fRating,
                                    'Rating',
                                    dataType=int,
                                    minNumber=1,
                                    maxNumber=5
                                )
                            if code != 4100:
                                raise Exception

                            '''
                                Description of the Feedback from User
                            '''
                            fDescription = self.request.arguments.get('description')
                            code, message = Validate.i(
                                    fDescription,
                                    'Description',
                                    dataType=unicode,
                                    minLength=0,
                                    maxLength=120
                                )
                            if code != 4100:
                                raise Exception

                            rFeedbackResult = yield self.booking.find_and_modify(
                                        query =
                                        {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id == 6',
                                            '$where': 'this.feedback[1] == null',
                                            'driver.0.id': self.profileId
                                        },
                                        update =
                                        {
                                            '$set':
                                            {
                                                'feedback.1':
                                                {
                                                    'rating': fRating,
                                                    'description': fDescription
                                                }
                                            }
                                        },
                                        fields =
                                        {
                                            '_id': 0,
                                            'requestor': 1
                                        }
                                )
                            if rFeedbackResult:
                                '''
                                    Publishing to the Booking Requestor
                                    Payment alert Socket Id: 3007190624
                                '''
                                message =  'Thank you for using Our Service.'
                                bookingRequestorId = rFeedbackResult['requestor'][0]['id']
                                liveBookingPaid = {
                                            'code': 3007190624,
                                            'status': True,
                                            'message': message,
                                            'result': []
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            bookingRequestorId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingPaid))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingPaid
                                    )
                                )

                                code = 2000
                                status = True
                            else:
                                code = 5220
                                message = 'Booking is not available.'
                        elif rActivityId == 9:

                            ''' Booking Cancel API activity
                                Searching for Booking:
                                Filters:
                                 1. Row Id ( bookingId )
                                 2. Entity Id
                                 3. Activity 2, 3, 4 -> 9 ( State is Cancel = 9 ),
                                 4. if Driver Id should be there in the Booking.
                                 5. if user Id should be there in the Booking.
                                 6. No restriction for Admin.
                            '''

                            try:
                                rBookingId = ObjectId(self.request.arguments['bookingId'])
                            except:
                                code = 4132
                                message = 'Invalid Argument - [ bookingId ].'
                                raise Exception

                            rForceData = self.request.arguments.get('data')
                            code, message = Validate.i(
                                    rForceData,
                                    'data',
                                    dataType=list,
                                    minLength=1,
                                    maxLength=1
                                )
                            if code != 4100:
                                raise Exception
                            code, message = Validate.i(
                                    rForceData[0],
                                    'data.0',
                                    dataType=dict,
                                    minLength=2,
                                    maxLength=2
                                )
                            if code != 4100:
                                raise Exception
                            '''
                                Reason why he want to stop the trip
                                Type: string
                                Required: Yes
                            '''
                            code, message = Validate.i(
                                    rForceData[0].get('reason'),
                                    'data.0.reason',
                                    dataType=unicode,
                                    minLength=5,
                                    maxLength=120
                                )
                            if code != 4100:
                                raise Exception
                            '''
                                Description why he want to stop the trip
                                Type: string
                                Required: no
                            '''
                            code, message = Validate.i(
                                    rForceData[0].get('description'),
                                    'data.0.description',
                                    dataType=unicode,
                                    maxLength=350
                                )
                            if code != 4100:
                                raise Exception

                            if self.apiId == 40216:
                                query = {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id == 2 |' + \
                                                    '| this.activity[this.activity.length - 1].id == 3 |' + \
                                                    '| this.onDemand == false',
                                            'requestor.0.id': self.profileId
                                        }
                            elif self.apiId == 30216:
                                query = {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id == 2 |' + \
                                                    '| this.activity[this.activity.length - 1].id == 3',
                                            'driver.0.id': self.profileId
                                        }
                            elif self.apiId == 20216:
                                query = {
                                            '_id': rBookingId,
                                            'entityId': self.entityId,
                                            '$where': 'this.activity[this.activity.length - 1].id < 9'
                                        }
                            else:
                                code = 5610
                                message = 'Internal Error, Please contact the support team.'
                                raise Exception

                            rBooking = yield self.booking.find(
                                        query,
                                        {
                                            '_id': 0,
                                            'startPoint': 1,
                                            'vehicle': 1,
                                            'requestor': 1,
                                            'driver': 1
                                        },
                                        limit=1
                                    )
                            if not len(rBooking):
                                code = 4243
                                message = 'Booking is not available.'
                                raise Exception
                            '''
                                Getting All the Details of the Requestor
                                Combines account, profile from BigBase
                                If serviceAccount available it will on priority
                            '''
                            requestorAccount = yield self.account.find(
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
                            if not len(requestorAccount):
                                code = 5150
                                message =  'Requestor Account Not Found.'
                                raise Exception
                            requestorAccount[0]['id'] = self.profileId
                            requestorAccount[0]['firstName'] = requestorAccount[0].get('firstName')
                            requestorAccount[0]['lastName'] = requestorAccount[0].get('lastName')
                            requestorAccount[0]['contact'] = requestorAccount[0].get('contact')
                            del requestorAccount[0]['_id']
                            rServiceAccount = yield self.serviceAccount.find(
                                    {
                                        'profileId': self.profileId,
                                        'entityId': self.entityId,
                                        'closed': False
                                    },
                                    {
                                        'firstName': 1,
                                        'lastName': 1
                                    },
                                    limit=1
                            )
                            if len(rServiceAccount):
                                requestorAccount[0]['firstName'] = rServiceAccount[0].get('firstName')
                                requestorAccount[0]['lastName'] = rServiceAccount[0].get('lastName')

                            '''
                                Searching for his assigned vehicle
                            '''
                            if len(rBooking[0]['vehicle']):
                                rVehicle = yield self.vehicle.find(
                                        {
                                            '_id': rBooking[0]['vehicle'][0]['id'],
                                            'disabled': False,
                                            'entityId': self.entityId,
                                        },
                                        {
                                            '_id': 1,
                                            'location': 1
                                        },
                                        limit=1
                                    )
                                if not len(rVehicle):
                                    code = 4233
                                    message = 'Assigned vehicle not found, Please contact the support team.'
                                    raise Exception
                            else:
                                rVehicle = []
                            '''
                                Last Location Update Time should be with in 20 minutes ( in microseconds )
                            '''
                            if len(rVehicle):

                                orgLatLng = (rVehicle[0]['location'][0]['coordinates'][1],
                                        rVehicle[0]['location'][0]['coordinates'][0])
                                destLatLng = (rBooking[0]['startPoint'][0]['coordinates'][1],
                                        rBooking[0]['startPoint'][0]['coordinates'][0])
                                '''
                                    Distance from the start point
                                '''
                                diffDistance = int(great_circle(orgLatLng, destLatLng).m)
                                rVcoordinates = rVehicle[0]['location'][0]['coordinates']
                            else:
                                diffDistance = 0.0
                                rVcoordinates = []

                            rStartedResult = yield self.booking.update(
                                    {
                                        '_id': rBookingId
                                    },
                                    {
                                        '$push':
                                        {
                                            'activity':
                                            {
                                                'id': 9,
                                                'time': self.time,
                                                'data': rForceData,
                                                'account': requestorAccount,
                                                'distance': diffDistance,
                                                'coordinates': rVcoordinates
                                            }
                                        }
                                    }
                                )
                            if rStartedResult['n']:
                                '''
                                    Publishing to the Booking Requestor
                                    Booking Cancel alert Socket Id: 608190527
                                '''
                                bookingRequestorId = rBooking[0]['requestor'][0]['id']
                                liveBookingStarted = {
                                            'code': 608190527,
                                            'status': True,
                                            'message': 'Your Booking has been cancelled.',
                                            'result': [
                                                    str(rBookingId)
                                                ]
                                        }
                                channelId = '{0}_{1}'.format(
                                            'PROFILE',
                                            bookingRequestorId
                                        )
                                yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingStarted))
                                Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                        channelId,
                                        liveBookingStarted
                                    )
                                )
                                if not len(rBooking[0]['driver']):
                                    code = 2000
                                    status = True
                                    message = 'Booking has been cancelled.'
                                else:
                                    bookingDriverId = rBooking[0]['driver'][0]['id']
                                    '''
                                        Publishing to the Booking Driver
                                        Booking Cancel alert Socket Id: 608190725
                                    '''
                                    liveBookingStarted = {
                                                'code': 608190725,
                                                'status': True,
                                                'message': 'Your Booking has been cancelled.',
                                                'result': [
                                                    str(rBookingId)
                                                    ]
                                            }
                                    channelId = '{0}_{1}'.format(
                                                'PROFILE',
                                                bookingDriverId
                                            )
                                    yield RedisMixin.stream.publish(channelId, json.dumps(liveBookingStarted))
                                    Log.i('[ BOOKING ] REDISH', 'PUBLISH ChannelID: {0} Payload: {1}'.format(
                                            channelId,
                                            liveBookingStarted
                                        )
                                    )
                                    code = 2000
                                    status = True
                                    message = 'Booking has been cancelled.'
                            else:
                                code = 5220
                                message = 'Internal Error Please Contact the Support Team.'
                        else:
                            code = 4003
                            message = 'Invalid Option Selected.'
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

