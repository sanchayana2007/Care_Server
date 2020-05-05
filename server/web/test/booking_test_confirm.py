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

@noXenSecureV1
class MtimeWebTestBookingConfirmHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('POST','GET')

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
            key = str(self.request.arguments.get('key'))
            acceptStatus = self.request.arguments.get('acceptStatus')
            bId = FN_DECRYPT(key)
            if not bId:
                code = 5090
                status = False
                message = "Internal Error Please Contact the Support Team."
                raise Exception
            else:
                bookingId = ObjectId(bId)
            #TODO:: Customer verification remaining
            if acceptStatus:
                bookingUpdate = yield self.testBooking.update(
                                    {
                                        '_id':bookingId,
                                        '$where': 'this.activity[this.activity.length - 1].id == 1'
                                    },
                                    {
                                    "$push":{
                                        'activity':
                                                {
                                                    'id':2,
                                                    'time':timeNow()
                                                }
                                        },
                                    }
                                )
                if bookingUpdate.get('n'):
                    status = True
                    code = 2000
                    message = "Booking has been confirmed."
                else:
                    status = False
                    code = 4104
                    message = "Invalid Booking"
            else:
                bookingUpdate = yield self.testBooking.update(
                                    {
                                        '_id':bookingId,
                                        '$where': 'this.activity[this.activity.length - 1].id == 1'
                                    },
                                    {
                                    "$inc":{
                                                'activity.1.declineCounter':1
                                            },
                                    }
                                )
                if bookingUpdate.get('n'):
                    status = True
                    code = 4104
                    message = "Booking has been declined"
                else:
                    status = False
                    code = 4104
                    message = "Invalid Booking"
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

    fu = FileUtil()
    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''
        try:
            key = str(self.request.arguments['key'][0])
            bId = FN_DECRYPT(key)
            if not bId:
                code = 5090
                status = False
                message = "Invalid Booking Confirmation"
                raise Exception
            else:
                bookingId = ObjectId(bId)
            serProf = {}
            bookInfo = yield self.testBooking.find(
                                    {
                                        '_id':bookingId,
                                        '$where': 'this.activity[this.activity.length - 1].id == 1'
                                    },
                                    {
                                        '_id':0,
                                        'customerDetails.firstName':1,
                                        'customerDetails.lastName':1,
                                        'customerDetails.roomNumber':1,
                                        'customerDetails.phoneNumber':1,
                                        'providerDetails.accountId':1,
                                        'documents':1,
                                        'faceProof':1,
                                        'entityId':1
                                    },
                                    limit=1
                                )
            if not len(bookInfo):
                code = 5210
                status = False
                message = "Invalid Booking"
                raise Exception
            accProv = bookInfo[0]['providerDetails'][0]['accountId']
            del bookInfo[0]['providerDetails']
            serProf = bookInfo[0]['customerDetails'][0]

            serProf['documents'] = []
            serProf['faceProof'] = []
            for media in bookInfo[0]['documents']:
                media['link'] = self.fu.serverUrl + '/uploads/' \
                            + str(bookInfo[0]['entityId']) + '/test_booking/' \
                            + str(bookingId) + '/' + str(media['time']) + media['mimeType']
                serProf['documents'].append(
                        media)
            for media in bookInfo[0]['faceProof']:
                media['link'] = self.fu.serverUrl + '/uploads/' \
                            + str(bookInfo[0]['entityId']) + '/test_booking/' \
                            + str(bookingId) + '/' + str(media['time']) + media['mimeType']
                serProf['faceProof'].append(
                        media)

            orgAcc = yield self.account.find(
                                            {
                                                '_id':accProv
                                            },
                                            {
                                                '_id': 0,
                                                'firstName': 1,
                                                'lastName': 1,
                                                'contact': 1
                                            }
                                        )
            if len(orgAcc):
                serProf['providerDetails'] = orgAcc
            else:
                code = 4000
                message = "Provider list is empty"
                raise Exception
            result.append(serProf)
            if len(result):
                code = 2000
                status = True
            else:
                code = 4040
                status = False
                message = "No Data Found"
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
