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
class MtimeWebTestBookingCoutHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ( 'POST')

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
    def post(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:

            try:
                videoProof = self.request.files['faceProof'][0]
            except Exception as e:
                code = 4102
                message = 'Need a Face Proof.'
                raise Exception

            try:
                bookingId = ObjectId(self.request.arguments['bookingId'][0])
            except Exception as e:
                code = 4103
                message = 'Invalid Argument [ bookingId ].'
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

                            filepath = []

                            videoProofType = videoProof['content_type']
                            videoProofType = yield mimetypes.guess_extension(
                                            videoProofType,
                                            strict=True
                                )
                            videoTime = timeNow()
                            # TODO: need to confirm it will be video or not
                            if str(videoProofType) in ['.mp4']:
                                fName = videoTime
                                fRaw = videoProof['body']
                                fp = self.fu.uploads + '/' + str(self.entityId) \
                                        + '/test_booking/' + str(bookingId) + '/'
                                if not os.path.exists(fp):
                                     Log.i('DRV-Profile', 'Creating Directories')
                                     os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + videoProofType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()
                                os.system('chmod 755 -R ' + fpm)
                                filepath.append(fpm)

                            else:
                                message = 'Invalid File Type for Video Proof.'
                                code = 4010
                                raise Exception

                                #TODO::Need to give expired time.

                            '''
                            idProofType = idProof['content_type']
                            idProofType = yield mimetypes.guess_extension(
                                            idProofType,
                                            strict=True
                                )


                            idTime = timeNow()
                            if str(idProofType) in ['.jpeg', '.jpg', '.png', '.jpe']:
                                fName = idTime
                                fRaw = idProof['body']
                                fp = self.fu.tmpPath
                                if not os.path.exists(fp):
                                    Log.i('Booking', 'Creating Directories')
                                    os.system('mkdir -p ' + fp)
                                fpm = fp + '/' + str(fName) + idProofType
                                fh = open(fpm, 'w')
                                fh.write(fRaw)
                                fh.close()

                                # Converting to PNG
                                idProofType = '.png'
                                fpx = fp + '/' + str(fName) + idProofType
                                filepath.append(fpx)
                                im = Image.open(fpm)
                                im.save(fpx, 'PNG')
                                os.system('rm ' + fpm)
                                os.system('chmod 755 -R ' + fp + '*')

                            else:
                                message = 'Invalid File Type for Face Proof.'
                                code = 4011
                                raise Exception
                            '''

                            checkOutUpdate = yield self.testBooking.update(
                                                {
                                                    '_id':ObjectId(bookingId),
                                                    'entityId':self.entityId,
                                                    '$where':'this.activity[this.activity.length-1].id == 3'
                                                },
                                                {
                                                '$push': {
                                                            'faceProof': {
                                                                                'time': videoTime,
                                                                                'mimeType': videoProofType
                                                                         },
                                                            'activity': {
                                                                                'id': 4,
                                                                                'time': timeNow(),
                                                                        }
                                                        }
                                                    }
                                                )


                            if checkOutUpdate['n']:
                                code = 2000
                                status = True
                                message = "Checkout Document has been successfully uploaded."
                            else:
                                code = 4302
                                status = False
                                message = 'Invalid Booking'

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

