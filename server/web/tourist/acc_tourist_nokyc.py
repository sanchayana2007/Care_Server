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
class MtimeWebNoKycTouristHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('GET','POST','PUT')

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

    fu = FileUtil()


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
                    if self.apiId in [ 402021, 402022]:
                        if self.apiId == 402021:
                            try:
                                subtouristId = ObjectId(self.request.arguments.get('subtouristId'))
                            except:
                                code = 4000
                                status = True
                                message = "Invalid Tourist Id"
                                raise Exception
                            try:
                                bookingId = ObjectId(self.request.arguments.get('bookingId'))
                            except:
                                code = 4000
                                status = True
                                message = "Invalid Booking Id"
                                raise Exception
                            title = self.request.arguments.get('title')
                            code,message = Validate.i(
                                        title,
                                        'Title',
                                        notEmpty = True,
                                        inputType='unicode',
                                        maxLength = 100
                                )
                            if code != 4100:
                                raise Exception
                            description = self.request.arguments.get('description')
                            code,message = Validate.i(
                                        description,
                                        'Description',
                                        notEmpty = True,
                                        inputType='unicode',
                                        maxLength = 100
                                )
                            if code != 4100:
                                raise Exception
                            subUpdate = yield self.touristBook.update(
                                            {
                                                '_id':bookingId,
                                                'touristDetails.id': str(subtouristId)
                                            },
                                            {
                                            '$set':{
                                                    'touristDetails.$.note': [
                                                                                    {
                                                                                        'title':title,
                                                                                        'description':description
                                                                                    }
                                                                                ]
                                                    }
                                            }
                                        )
                            if subUpdate['n']:
                                code = 2000
                                status = True
                                message = "Note has been added"
                            else:
                                code = 4050
                                status = False
                                message = "Invalid account"
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

