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


from lib import *

@xenSecureV1
class DeviceHandler(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('GET', 'POST', 'DELETE','PUT')

    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][6]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]

    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    deviceModel = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][8]['name']
                ]

    device = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][9]['name']
                ]

    vehicle = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][4]['name']
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
                                'entityId': self.entityId,
                                'accountId': self.accountId,
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
                            vTypes = yield self.device.find(
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
                                    del v['entityId']
                                    dModel = yield self.deviceModel.find(
                                        {
                                            '_id': v['modelId']
                                        }
                                    )
                                    if not len(dModel):
                                        raise Exception
                                    else:
                                        v['modelId'] = str(v['modelId'])
                                        v['model'] = dModel[0]['model']
                                        v['make'] = dModel[0]['make']
                                    dVehicle = yield self.vehicle.find(
                                                {
                                                    'deviceId': v['_id']
                                                },
                                                limit=1
                                            )
                                    if len(dVehicle):
                                        v['assigned'] = True
                                    else:
                                        v['assigned'] = False
                                    del v['_id']
                                    result.append(v)
                                status = True
                                code = 2000
                            else:
                                code = 3001
                                message = 'No Device Found.'
                        else:
                            try:
                                limit = int(self.get_arguments('limit')[0])
                            except:
                                limit = None

                            try:
                                skip = int(self.get_arguments('skip')[0])
                            except:
                                skip = 0

                            try:
                                assigned = bool(int(self.get_arguments('assigned')[0]))
                            except:
                                assigned = None

                            if limit != None:
                                vTypes = yield self.device.find(
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
                                        del v['entityId']
                                        dModel = yield self.deviceModel.find(
                                            {
                                                '_id': v['modelId']
                                            }
                                        )
                                        if not len(dModel):
                                            raise Exception
                                        else:
                                            v['modelId'] = str(v['modelId'])
                                            v['model'] = dModel[0]['model']
                                            v['make'] = dModel[0]['make']

                                        dVehicle = yield self.vehicle.find(
                                                    {
                                                        'deviceId': v['_id']
                                                    },
                                                    limit=1
                                                )
                                        if len(dVehicle):
                                            v['assigned'] = True
                                        else:
                                            v['assigned'] = False

                                        if assigned != None:
                                            if assigned and v['assigned']:
                                                result.append(v)
                                            elif not assigned and not v['assigned']:
                                                result.append(v)
                                        else:
                                            result.append(v)
                                        del v['_id']
                                    if len(result):
                                        status = True
                                        code = 2000
                                    else:
                                        code = 3001
                                        message = 'No Device Found.'
                                else:
                                    code = 3001
                                    message = 'No Device Found.'
                            else:
                                vTypes = yield self.device.find(
                                        {
                                            'entityId': self.entityId,
                                            'disabled': tDisabled
                                        }
                                    )
                                if len(vTypes):
                                    for v in vTypes:
                                        v['id'] = str(v['_id'])
                                        del v['entityId']
                                        dModel = yield self.deviceModel.find(
                                            {
                                                '_id': v['modelId']
                                            }
                                        )
                                        if not len(dModel):
                                            raise Exception
                                        else:
                                            v['modelId'] = str(v['modelId'])
                                            v['model'] = dModel[0]['model']
                                            v['make'] = dModel[0]['make']

                                        dVehicle = yield self.vehicle.find(
                                                    {
                                                        'deviceId': v['_id']
                                                    },
                                                    limit=1
                                                )
                                        if len(dVehicle):
                                            v['assigned'] = True
                                        else:
                                            v['assigned'] = False

                                        if assigned != None:
                                            if assigned and v['assigned']:
                                                result.append(v)
                                            elif not assigned and not v['assigned']:
                                                result.append(v)
                                        else:
                                            result.append(v)
                                        del v['_id']
                                    if len(result):
                                        status = True
                                        code = 2000
                                    else:
                                        code = 3001
                                        message = 'No Device Found.'
                                else:
                                    code = 3001
                                    message = 'No Device Found.'
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
                                'entityId': self.entityId,
                                'accountId': self.accountId,
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

                        dSerialNumber = self.request.arguments.get('serialNumber')
                        code, message = Validate.i(
                                    dSerialNumber,
                                    'Serial Number',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=60
                                )
                        if code != 4100:
                            raise Exception

                        dIMEI = self.request.arguments.get('imei')
                        code, message = Validate.i(
                                    dIMEI,
                                    'IMEI',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=90
                                )
                        if code != 4100:
                            raise Exception

                        try:
                            dModelId = ObjectId(self.request.arguments.get('modelId'))
                            dModel = yield self.deviceModel.find(
                                        {
                                            '_id': dModelId
                                        }
                                    )
                            if not len(dModel):
                                raise Exception
                        except:
                            code = 4130
                            message = 'Invalid Argument - [ Model Id ].'
                            raise Exception


                        simNumber = self.request.arguments.get('simNumber')
                        code, message = Validate.i(
                                    simNumber,
                                    'SIM Number',
                                    dataType=int
                                )
                        if code != 4100:
                            raise Exception

                        simCountryCode = self.request.arguments.get('simCountryCode')
                        code, message = Validate.i(
                                    simCountryCode,
                                    'SIM Country Code',
                                    dataType=int
                                )
                        if code != 4100:
                            raise Exception

                        country = yield self.phoneCountry.find(
                                    {
                                        'code': simCountryCode
                                    },
                                    limit=1
                                )
                        if not len(country):
                            code = 4242
                            message = 'Invalid SIM Country Code.'
                            raise Exception
                        if len(str(simNumber)) != country[0]['telMaxLength']:
                            code = 4252
                            message = 'Invalid SIM Number.'
                            raise Exception
                        else:
                            simNumber = long(str(simCountryCode) + str(simNumber))

                        try:
                            yield self.device.insert(
                                    {
                                        'disabled': False,
                                        'serialNumber': dSerialNumber,
                                        'imei': dIMEI,
                                        'simNumber': simNumber,
                                        'modelId': dModelId,
                                        'entityId': self.entityId
                                    }
                                )
                            status = True
                            code = 2000
                            message = 'New Device has been created.'
                        except Exception as e:
                            exe = str(e).split(':')
                            if len(exe) < 2:
                                status = False
                                code = 4280
                                message = 'This Device is already exists.'
                            elif 'imei_1' in exe[2]:
                                status = False
                                code = 4281
                                message = 'This IMEI is already exists.'
                            elif 'serialNumber_1' in exe[2]:
                                status = False
                                code = 4282
                                message = 'This Serial Number is already exists.'
                            elif 'simNumber_1' in exe[2]:
                                status = False
                                code = 4283
                                message = 'This Sim Number is already exists.'
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
                                'entityId': self.entityId,
                                'accountId': self.accountId,
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

                        tDisabled = self.request.arguments.get('disabled')
                        code, message = Validate.i(
                                    tDisabled,
                                    'Disabled',
                                    dataType=bool
                                )
                        if code != 4100:
                            raise Exception

                        dSerialNumber = self.request.arguments.get('serialNumber')
                        code, message = Validate.i(
                                    dSerialNumber,
                                    'Serial Number',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=60
                                )
                        if code != 4100:
                            raise Exception

                        dIMEI = self.request.arguments.get('imei')
                        code, message = Validate.i(
                                    dIMEI,
                                    'IMEI',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=90
                                )
                        if code != 4100:
                            raise Exception

                        try:
                            dModelId = ObjectId(self.request.arguments.get('modelId'))
                            dModel = yield self.deviceModel.find(
                                        {
                                            '_id': dModelId
                                        }
                                    )
                            if not len(dModel):
                                raise Exception
                        except:
                            code = 4130
                            message = 'Invalid Argument - [ modelId ].'
                            raise Exception

                        simNumber = self.request.arguments.get('simNumber')
                        code, message = Validate.i(
                                    simNumber,
                                    'SIM Number',
                                    dataType=int
                                )
                        if code != 4100:
                            raise Exception

                        simCountryCode = self.request.arguments.get('simCountryCode')
                        code, message = Validate.i(
                                    simCountryCode,
                                    'SIM Country Code',
                                    dataType=int
                                )
                        if code != 4100:
                            raise Exception

                        country = yield self.phoneCountry.find(
                                    {
                                        'code': simCountryCode
                                    },
                                    limit=1
                                )
                        if not len(country):
                            code = 4242
                            message = 'Invalid SIM Country Code.'
                            raise Exception
                        if len(str(simNumber)) != country[0]['telMaxLength']:
                            code = 4252
                            message = 'Invalid SIM Number.'
                            raise Exception
                        else:
                            simNumber = long(str(simCountryCode) + str(simNumber))

                        try:
                            vTypeId = ObjectId(self.request.arguments['id'])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception

                        try:
                            updateResult = yield self.device.find_and_modify(
                                    query = {
                                            '_id': vTypeId,
                                            'entityId': self.entityId
                                        },
                                    update = {
                                        '$set': {
                                            'disabled': tDisabled,
                                            'serialNumber': dSerialNumber,
                                            'imei': dIMEI,
                                            'simNumber': simNumber,
                                            'modelId': dModelId
                                        }
                                    }
                            )
                            if updateResult:
                                status = True
                                code = 2000
                                message = 'Device details has been updated.'
                            else:
                                code = 4210
                                message = 'This Device does not exist.'
                        except Exception as e:
                            print e
                            exe = str(e).split(':')
                            if len(exe) < 2:
                                status = False
                                code = 4280
                                message = 'This Device is already exists.'
                            elif 'imei_1' in exe[2]:
                                status = False
                                code = 4281
                                message = 'This IMEI is already exists.'
                            elif 'serialNumber_1' in exe[2]:
                                status = False
                                code = 4282
                                message = 'This Serial Number is already exists.'
                            elif 'simNumber_1' in exe[2]:
                                status = False
                                code = 4283
                                message = 'This Sim Number is already exists.'
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
            # TODO: this need to be moved in a global class, from here
            profile = yield self.profile.find(
                            {
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
                        updateResult = yield self.device.find_and_modify(
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
                            message = 'Device has been Disabled.'
                        else:
                            code = 4210
                            message = 'This Device does not exist.'
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

