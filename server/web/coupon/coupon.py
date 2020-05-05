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
class MmsCouponHandler(cyclone.web.RequestHandler, MongoMixin):

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
                            code == 4310
                            message = 'Invalid Argument - [ disabled ].'
                            raise Exception

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
                                        limit=1
                                    )
                            if len(vTypes):
                                for v in vTypes:
                                    v['id'] = str(v['_id'])
                                    del v['_id']
                                    del v['entityId']
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
                                    limit=limit,
                                    skip=skip
                                )
                            if len(vTypes):
                                for v in vTypes:
                                    v['id'] = str(v['_id'])
                                    del v['_id']
                                    del v['entityId']
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
                        if self.apiId == 20216: # TODO: till here
                            try:
                                code = str(self.request.arguments.get('code'))
                                description = str(self.request.arguments.get('description'))
                                usagePerUser = long(self.request.arguments.get('usagePerUser'))
                                totalUsers = long(self.request.arguments.get('totalUsers'))
	    	    	        percentageDiscount = long(self.request.arguments.get('percentageDiscount'))
                                absoluteDiscount = long(self.request.arguments.get('absoluteDiscount'))
                                datearray = list(self.request.arguments.get('dateArray'))
                                timearray = list(self.request.arguments.get('timeArray'))
                            except:
                                status = False
	    			code = 4220
                                message = 'Invalid Syntax.'

			    try:
                                couponData = {
                                        'disabled': False,
                                        'entityId': self.entityId,
                                        'code': code,
                                        'description': description,
                                        'usagePerUser': usagePerUser,
                                        'totalUsers': totalUsers,
                                        'percentageDiscount': percentageDiscount,
                                        'absoluteDiscount': absoluteDiscount,
                                        'dateArray': datearray,
                                        'timeArray': timearray
				}
                                yield self.coupons.insert(couponData)
                                status = True
                                code = 2000
                                message = 'Coupon added successfully'
                            except Exception:
                                status = False
	    			code = 4833
                                message = 'This Coupon is already exists.'
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
                        if self.apiId == 20216: # TODO: till here
                            try:
                                couponId = ObjectId(self.request.arguments.get('id'))
                                disabled = bool(self.request.arguments.get('disabled'))
                                code = str(self.request.arguments.get('code'))
                                description = str(self.request.arguments.get('description'))
                                usagePerUser = long(self.request.arguments.get('usagePerUser'))
                                totalUsers = long(self.request.arguments.get('totalUsers'))
		    	        percentageDiscount = long(self.request.arguments.get('percentageDiscount'))
                                absoluteDiscount = long(self.request.arguments.get('absoluteDiscount'))
                                datearray = list(self.request.arguments.get('dateArray'))
                                timearray = list(self.request.arguments.get('timeArray'))
                            except:
                                code = 4430
                                message = 'Invalid Syxtax.'
                                raise Exception
			    try:
                                couponData = {
                                        'disabled': disabled,
                                        'code': code,
                                        'description': description,
                                        'usagePerUser': usagePerUser,
                                        'totalUsers': totalUsers,
                                        'percentageDiscount': percentageDiscount,
                                        'absoluteDiscount': absoluteDiscount,
                                        'dateArray': datearray,
                                        'timeArray': timearray
				}
                                yield self.coupons.update(
                                        {
                                            '_id': ObjectId(couponId),
                                            'entityId': self.entityId
                                        },
                                        {
                                            '$set': couponData
                                        }
                                    )
                                status = True
                                code = 2000
                                message = 'Coupon updated successfully'
                            except Exception:
                                status = False
	    			code = 4833
                                message = 'This Coupon is already exists.'
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
    def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
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
                            vTypeId = ObjectId(self.get_arguments('id')[0])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception
                        updateResult = yield self.coupons.find_and_modify(
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
                            message = 'Coupon has been Disabled.'
                        else:
                            code = 4210
                            message = 'This Coupon does not exist.'
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
