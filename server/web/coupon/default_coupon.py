#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	1.  CouponHandler
		Type: Class
		Methods:
			A.GET:
				Get all coupon  details
			B.POST:
				Will create new coupon
			C.PUT:
				Update coupon details
			D:DELETE:
				Delete coupon
'''
import traceback
from lib import *

@xenSecureV1
class MmsDefaultCouponHandler(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ("GET", "POST", "DELETE","PUT")

    account = MongoMixin.userDb[
                CONFIG['database'][0]['table'][0]['name']
            ]

    applications = MongoMixin.userDb[
                CONFIG['database'][0]['table'][1]['name']
            ]

    profile = MongoMixin.userDb[
                CONFIG['database'][0]['table'][2]['name']
            ]

    coupons = MongoMixin.serviceDb[
                CONFIG['database'][1]['table'][11]['name']
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
                            'closed': False,
                            'accountId': self.accountId,
                            'applicationId': self.applicationId,
                            'entityId': self.entityId
                        },
                        limit=1
                    )
                if len(profile):
                    app = yield self.applications.find(
                            {
                                '_id': self.applicationId
                            },
                            limit=1
                        )
                    if len(app):
                        try:
                            tDisabled = bool(int(self.get_arguments('disabled')[0]))
                        except:
                            tDisabled = False
                        # Set default to False
                        tDisabled = False

                        try:
                            vTypeId = ObjectId(self.get_arguments('id')[0])
                        except:
                            vTypeId = None

                        if vTypeId != None:
                            vTypes = yield self.coupons.find(
                                        {
                                            '_id': vTypeId,
                                            'entityId': self.entityId,
                                            'disabled': tDisabled
                                        },
                                        {
                                            '_id': 1,
                                            'code': 1,
                                            'discountUpto': 1,
                                            'percentageDiscount': 1,
                                            'absoluteDiscount': 1,
                                            'description': 1
                                        },
                                        limit=1
                                    )
                            if len(vTypes):
                                for v in vTypes:
                                    v['id'] = str(v['_id'])
                                    del v['_id']
                                    result.append(v)
                                status = True
                                code = 2000
                            else:
                                code = 3001
                                message = 'No Coupons Found.'
                        else:
                            try:
                                limit = int(self.get_arguments('limit')[0])
                            except:
                                limit = 0

                            try:
                                skip = int(self.get_arguments('skip')[0])
                            except:
                                skip = 0

                            vTypes = yield self.coupons.find(
                                    {
                                        'entityId': self.entityId,
                                        'disabled': tDisabled
                                    },
                                    {
                                        '_id': 1,
                                        'code': 1,
                                        'discountUpto': 1,
                                        'percentageDiscount': 1,
                                        'absoluteDiscount': 1,
                                        'description': 1
                                    },
                                    limit=limit,
                                    skip=skip
                                )
                            if len(vTypes):
                                for v in vTypes:
                                    v['id'] = str(v['_id'])
                                    del v['_id']
                                    result.append(v)
                                status = True
                                code = 2000
                            else:
                                code = 3001
                                message = 'No Coupons Found.'
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

