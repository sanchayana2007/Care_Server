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
class MtimeWebTestBookingPaidHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('POST')

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
    def post(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # GET JSON FROM REQUEST BODY
                self.request.arguments = json.loads(self.request.body)

            except Exception as e:
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                code = 4100
                message = 'Expected Request Type FormData.'
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
		    if self.apiId in [ 402021, 30216, 20216, 402020, 402022 ]:
                        if self.apiId in [ 402021, 30216, 20216, 402020, 402022 ]: #TODO: till here
                            try:
                                bookingId  = ObjectId(self.request.arguments.get('bookingId'))
                            except:
                                code = 4013
                                status = False
                                message = "Invalid Booking"
                                raise Exception

                            #TODO:: Customer verification remaining
                            bookingUpdate = yield self.testBooking.update(
                                            {
                                                '_id':bookingId,
                                                'entityId': self.entityId,
                                                'providerDetails.0.id': self.profileId,
                                                '$where': 'this.activity[this.activity.length - 1].id > 0 && this.activity[this.activity.length - 1].id < 3'
                                            },
                                            {
                                                "$push":{
                                                            'activity':
                                                                        {
                                                                            'id':3,
                                                                            'time':timeNow()
                                                                        }
                                                        }
                                            }
                                        )
                            #TODO::Customer notification not yet done
                            if bookingUpdate.get('n'):
                                status = True
                                code = 2000
                                message = "Booking Payment is Complete.."
                            else:
                                status = False
                                code = 4104
                                message = "Invalid Booking"
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

