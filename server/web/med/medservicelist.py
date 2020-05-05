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
class MedServiceListHandler(cyclone.web.RequestHandler,
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

    fu = FileUtil()

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''
        try:
            serviceId = self.request.arguments['id'][0]
        except:
            serviceId = None
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
                    if app[0]['apiId'] in [ 502020, 502022]: # TODO: till here
                        if serviceId == None:
                            res = yield self.serviceList.find(
                                        {
                                            'entityId':self.entityId,
                                            'disabled':False
                                        }
                                    )
                        else:
                            try:
                                serviceId = ObjectId(serviceId)
                            except:
                                code = 4050
                                status = False
                                message = "Invalid Service Id"
                            res = yield self.serviceList.find(
                                        {
                                            'entityId':self.entityId,
                                            '_id':serviceId,
                                            'disabled':False
                                        }
                                    )
                        if len(res):
                            for serInfo in res:
                                v = {
                                        '_id':str(serInfo['_id']),
                                        'serNameEnglish':serInfo['serNameEnglish'],
                                        'serNameHindi':serInfo['serNameHindi'],
                                        'serCharges':serInfo['serCharges'],
                                        'serTA':serInfo['serTA'],
                                        'serDA':serInfo['serDA'],
                                        'serTATotal':serInfo['serTATotal'],
                                        'serDATotal':serInfo['serDATotal'],
                                        'media':serInfo['media']
                                    }
                                if len(v['media']):
                                    for docx in v['media']:
                                        docx['link'] = self.fu.serverUrl + '/uploads/' \
                                                + str(self.entityId)\
                                                + '/service_media/' + str(serInfo['_id'])\
                                                + '/' + str(docx['time']) + docx['mimeType']
                                else:
                                    img = {
                                            'link':"https://medix.xlayer.in/uploads/default/serviceList.png"
                                        }
                                    v['media'].append(img)
                                result.append(v)
                            result.reverse()
                            code = 2000
                            status = True
                            message = 'List of services'
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
                            serNameEnglish = self.request.arguments.get('serNameEnglish')
                            code, message = Validate.i(
                                    serNameEnglish,
                                    'serNameEnglish',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=40
                                )
                            if code != 4100:
                                raise Exception

                            serNameHindi = self.request.arguments.get('serNameHindi')
                            if serNameHindi == None:
                                code = 4830
                                status = False
                                message = "Service Name in Hindi missing."
                                raise Exception
                            if not len(serNameHindi):
                                code = 4840
                                status = False
                                message = "Service Name in Hindi missing."
                                raise Exception

                            serCharges = self.request.arguments.get('serCharges')
                            code, message = Validate.i(
                                    serCharges,
                                    'serCharges',
                                    dataType=int,
                                    notEmpty=True,
                                )
                            if code != 4100:
                                raise Exception

                            serTA = self.request.arguments.get('serTA')
                            code, message = Validate.i(
                                    serTA,
                                    'service TA',
                                    dataType=int,
                                    notEmpty=True,
                                )
                            if code != 4100:
                                raise Exception

                            serDA = self.request.arguments.get('serDA')
                            code, message = Validate.i(
                                    serDA,
                                    'service DA',
                                    dataType=int,
                                    notEmpty=True,
                                )
                            if code != 4100:
                                raise Exception
                            serTATotal = serCharges + serTA
                            serDATotal = serCharges + serDA

                            serData = {
                                        'disabled': False,
                                        'serNameEnglish':serNameEnglish,
                                        'serNameHindi':serNameHindi,
                                        'serCharges':serCharges,
                                        'serTA':serTA,
                                        'serTATotal':serTATotal,
                                        'serDA':serDA,
                                        'serDATotal':serDATotal,
                                        'media':[],
                                        'entityId':self.entityId
                                      }
                            serviceId = yield self.serviceList.insert(serData)
                            code = 2000
                            message = "Service has been added"
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
                                serviceId = ObjectId(self.request.arguments.get('serviceId'))
                            except:
                                code = 4050
                                message = "Invalid service Id"
                                raise Exception
                            serBook = yield self.serviceList.find(
                                        {
                                            '_id':serviceId
                                        }
                                    )
                            if not len(serBook):
                                code = 4060
                                message = "Invalid Booking"
                                raise Exception
                            serNameEnglish = self.request.arguments.get('serNameEnglish')
                            code, message = Validate.i(
                                    serNameEnglish,
                                    'serNameEnglish',
                                    dataType=unicode,
                                    notEmpty=True,
                                    maxLength=40
                                )
                            if code != 4100:
                                raise Exception

                            serNameHindi = self.request.arguments.get('serNameHindi')
                            if serNameHindi == None:
                                code = 4830
                                status = False
                                message = "Service Name in Hindi missing."
                                raise Exception
                            if not len(serNameHindi):
                                code = 4840
                                status = False
                                message = "Service Name in Hindi missing."
                                raise Exception

                            serCharges = self.request.arguments.get('serCharges')
                            code, message = Validate.i(
                                    serCharges,
                                    'serCharges',
                                    dataType=int,
                                    notEmpty=True,
                                )
                            if code != 4100:
                                raise Exception

                            serTA = self.request.arguments.get('serTA')
                            code, message = Validate.i(
                                    serTA,
                                    'service TA',
                                    dataType=int,
                                    notEmpty=True,
                                )
                            if code != 4100:
                                raise Exception
                            serDA = self.request.arguments.get('serDA')
                            code, message = Validate.i(
                                    serDA,
                                    'service DA',
                                    dataType=int,
                                    notEmpty=True,
                                )
                            if code != 4100:
                                raise Exception

                            serTATotal = serCharges + serTA
                            serDATotal = serCharges + serDA
                            serUpdate = yield self.serviceList.update(
                                                {
                                                    '_id':serviceId,
                                                },
                                                {
                                                '$set':{
                                                            'serNameEnglish':serNameEnglish,
                                                            'serNameHindi':serNameHindi,
                                                            'serCharges':serCharges,
                                                            'serTA':serTA,
                                                            'serTATotal':serTATotal,
                                                            'serDA':serDA,
                                                            'serDATotal':serDATotal,
                                                        }
                                                }
                                            )
                            if serUpdate['n']:
                                code = 2000
                                message = "Service information updated"
                                status = True
                            else:
                                code = 4060
                                message = "Invalid Service"
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
                serviceId = ObjectId(self.request.arguments['id'][0])
            except Exception as e:
                code = 4100
                message = 'Invalid ID'
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
                        serDel = yield self.serviceList.update(
                                    {
                                        '_id':serviceId
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
                            message = "Service has been removed from active list"
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

