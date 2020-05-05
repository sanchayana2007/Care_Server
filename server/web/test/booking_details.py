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
class MtimeWebTestBookingDetailsHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

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
                    if self.apiId in [ 402020, 402021, 402022 ]: # TODO: till here


                        '''
                            From Accomodation Provider / Tourist
                            Setting Booking Activity Status to Requested
                            Activity Id = 1 ( Requested ).
                            Entering Customer and Room Details, etc.
                        '''
                        if self.apiId in [402020, 402021]:
                            try:
                                bookingId = self.request.arguments.get('bookingId')
                                if not bookingId:
                                    raise Exception
                                else:
                                    bookingId = ObjectId(bookingId)
                            except:
                                code = 4050
                                status = False
                                message = "Invalid Booking Id"
                                raise Exception
                            cFirstName = self.request.arguments.get('firstName')
                            code,message = Validate.i(
                                            cFirstName,
                                            'First Name',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 50,
                                            noSpecial = True,
                                            noNumber = True
                                        )

                            if code != 4100:
                                raise Exception



                            cLastName = self.request.arguments.get('lastName')
                            code,message = Validate.i(
                                            cLastName,
                                            'Last Name',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 50,
                                            noSpecial = True,
                                            noNumber = True
                                        )

                            if code != 4100:
                                raise Exception

                            cPhoneNumber = self.request.arguments.get('phoneNumber')
                            Log.i(type(cPhoneNumber))
                            if cPhoneNumber:
                                code,message = Validate.i(
                                            cPhoneNumber,
                                            'Phone Number',
                                            notEmpty = True,
                                            dataType = int,
                                            minNumber=1000000000,
                                            maxNumber=9999999999
                                        )

                                if code != 4100:
                                    raise Exception

                            cEmailAddress = self.request.arguments.get('email')
                            if cEmailAddress:
                                code,message = Validate.i(
                                            cEmailAddress,
                                            'Email',
                                            inputType='email',
                                            dataType=unicode,
                                            maxLength=50
                                        )

                                if code != 4100:
                                    raise Exception

                            cRoomNum = self.request.arguments.get('roomNumber')
                            code,message = Validate.i(
                                            cRoomNum,
                                            'Room Number',
                                            notEmpty = True,
                                            dataType = unicode,
                                            maxLength = 20,
                                            noSpecial = True
                                        )

                            if code != 4100:
                                raise Exception

                            custDetailsUpdate = yield self.testBooking.update(
                                                                {
                                                                    '_id':ObjectId(bookingId),
                                                                    '$where': 'this.activity[this.activity.length - 1].id == 1',
                                                                    'providerDetails.0.id': self.profileId
                                                                },
                                                                {
                                                                '$set': {
                                                                    'customerDetails':[
                                                                                        {
                                                                                            'verified': False,
                                                                                            'firstName':cFirstName,
                                                                                            'lastName':cLastName,
                                                                                            'phoneNumber':cPhoneNumber,
                                                                                            'email':cEmailAddress,
                                                                                            'roomNumber':cRoomNum
                                                                                        }
                                                                                    ]
                                                                    }
                                                            }
                                                    )
                            if custDetailsUpdate['n']:
                                code = 2000
                                status = True
                                message = "Tourist contact information has been updated"
                            else:
                                code = 2002
                                status = False
                                message = "Invalid Booking."

                        #TODO::Customer will receive notification from here and activityID will be updated accordingly.

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
                    if app[0]['apiId'] == 402020: # TODO: till here
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

