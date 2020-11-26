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
class MedServiceProductHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    SUPPORTED_METHODS = ('GET','POST','PUT','DELETE')

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
    serviceBook = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][0]['name']
                ]
    serviceList = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][1]['name']
                ]
    cancelFee = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][2]['name']
                ]
    serviceProduct = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][4]['name']
                ]

    fu = FileUtil()

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''
        try:
            productId = self.request.arguments['id'][0]
        except:
            productId = None
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
                    Log.i(self.apiId)
                    if app[0]['apiId'] in [ 502020, 502022, 502021]: # TODO: till here
                        if productId == None:
                            res = yield self.serviceProduct.find(
                                        {
                                            'entityId':self.entityId,
                                            'disabled':False
                                        }
                                    )
                        else:
                            try:
                                productId = ObjectId(productId)
                            except:
                                code = 4050
                                status = False
                                message = "Invalid Product Id"
                            res = yield self.serviceProduct.find(
                                        {
                                            'entityId':self.entityId,
                                            '_id':productId,
                                            'disabled':False
                                        }
                                    )
                        if len(res):
                            for proInfo in res:
                                v = {
                                        'id':str(proInfo['_id']),
                                        'serviceId':str(proInfo['serviceId']),
                                        'serviceName':proInfo['serviceName'],
                                        'productName':proInfo['productName'],
                                        'productPrice':proInfo['productPrice'],
                                    }
                                result.append(v)
                            result.reverse()
                            code = 2000
                            status = True
                            message = 'List of products'
                        else:
                            code = 4080
                            status = False
                            message = "No data found"
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
                    if self.apiId in [ 502020, 502022]:
                        if self.apiId == 502022:
                            serviceId = self.request.arguments.get('serviceId')
                            if serviceId == None:
                                code = 4830
                                status = False
                                message = "Service name is missing"
                                raise Exception
                            code, message = Validate.i(
                                    serviceId,
                                    'serviceId',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=40
                                )
                            if code != 4100:
                                raise Exception

                            try:
                                serviceId = ObjectId(serviceId)
                            except:
                                code = 4555
                                status = False
                                message = "Invalid Service Id"
                                raise Exception

                            serFind = yield self.serviceList.find(
                                        {
                                            '_id':serviceId,
                                            'disabled':False
                                        }
                                    )
                            if not len(serFind):
                                code = 4560
                                status = False
                                message = "Service is not valid"
                                raise Exception

                            serviceName = serFind[0]['serNameEnglish']

                            productName = self.request.arguments.get('productName')
                            if productName == None or productName == '':
                                code = 4830
                                status = False
                                message = "Product name is missing"
                                raise Exception
                            code, message = Validate.i(
                                    productName,
                                    'Product Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=40
                                )
                            if code != 4100:
                                raise Exception

                            productPrice = self.request.arguments.get('productPrice')
                            if productPrice == None or productPrice == '':
                                code = 4830
                                status = False
                                message = "Product price is missing"
                                raise Exception
                            code,message = Validate.i(
                                            productPrice,
                                            'Product Price',
                                            dataType = int,
                                            minNumber= 0,
                                            maxNumber= 100000,
                                        )
                            if code != 4100:
                                raise Exception


                            proData = {
                                        'disabled': False,
                                        'entityId':self.entityId,
                                        'serviceId':serviceId,
                                        'serviceName':serviceName,
                                        'productName':productName,
                                        'productPrice':productPrice
                                      }
                            productId = yield self.serviceProduct.insert(proData)
                            code = 2000
                            message = "Product has been added"
                            status = True
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
                    if self.apiId in [ 502020, 502022]:
                        if self.apiId == 502022:
                            try:
                                productId = ObjectId(self.request.arguments.get('productId'))
                            except:
                                code = 4050
                                message = "Invalid Product Id"
                                raise Exception
                            proFind = yield self.serviceProduct.find(
                                        {
                                            '_id':productId
                                        }
                                    )
                            if not len(proFind):
                                code = 4060
                                status = False
                                message = "Invalid Product"
                                raise Exception
                            serviceId = self.request.arguments.get('serviceId')
                            if serviceId == None:
                                code = 4830
                                status = False
                                message = "Service name is missing"
                                raise Exception
                            code, message = Validate.i(
                                    serviceId,
                                    'serviceId',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=40
                                )
                            if code != 4100:
                                raise Exception

                            try:
                                serviceId = ObjectId(serviceId)
                            except:
                                code = 4555
                                status = False
                                message = "Invalid Service Id"
                                raise Exception

                            serFind = yield self.serviceList.find(
                                        {
                                            '_id':serviceId,
                                        }
                                    )
                            if not len(serFind):
                                code = 4560
                                status = False
                                message = "Service is not valid"
                                raise Exception

                            serviceName = serFind[0]['serNameEnglish']

                            productName = self.request.arguments.get('productName')
                            if productName == None or productName == '':
                                code = 4830
                                status = False
                                message = "Product name is missing"
                                raise Exception
                            code, message = Validate.i(
                                    productName,
                                    'Product Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=40
                                )
                            if code != 4100:
                                raise Exception

                            productPrice = self.request.arguments.get('productPrice')
                            if productPrice == None or productPrice == '':
                                code = 4830
                                status = False
                                message = "Product price is missing"
                                raise Exception
                            code, message = Validate.i(
                                    productPrice,
                                    'Product Price',
                                    dataType=int,
                                    notEmpty=True,
                                )
                            if code != 4100:
                                raise Exception
                            proUpdate = yield self.serviceProduct.update(
                                                {
                                                    '_id':productId,
                                                },
                                                {
                                                '$set':{
                                                            'serviceId':serviceId,
                                                            'serviceName':serviceName,
                                                            'productName':productName,
                                                            'productPrice':productPrice
                                                        }
                                                }
                                            )
                            if proUpdate['n']:
                                code = 2000
                                message = "Product information updated"
                                status = True
                            else:
                                code = 4060
                                message = "Invalid Product"
                                status = False
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

    @defer.inlineCallbacks
    def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                productId = ObjectId(self.request.arguments['id'][0])
            except Exception as e:
                code = 4100
                message = 'Invalid Product ID'
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
                    if app[0]['apiId'] == 502022:# TODO: till here
                        serDel = yield self.serviceProduct.update(
                                    {
                                        '_id':productId
                                    },
                                    {
                                    '$set':{
                                                'disabled':True
                                           }
                                    }
                                )
                        if serDel['n']:
                            code = 2000
                            status = True
                            message = "Product has been removed from active list"
                        else:
                            code = 4210
                            status = False
                            message = 'This entry does not exist.'
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
