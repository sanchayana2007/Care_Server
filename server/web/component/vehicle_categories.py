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
class VehicleCategoryHandler(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('GET')
    #SUPPORTED_METHODS = ('GET', 'POST', 'DELETE', 'OPTIONS', 'PUT')

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

    vehicleCategory = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][1]['name']
                ]

    vehicleType = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][2]['name']
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
                    accessId = app[0]['apiId']
                    if accessId == 20216 or accessId == 40216: # TODO: till here
                        try:
                            tDisabled = bool(int(self.get_arguments('disabled')[0]))
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ disabled ].'
                            raise Exception

                        try:
                            shrink = bool(int(self.get_arguments('shrink')[0]))
                        except:
                            shrink = True

                        try:
                            vCatId = ObjectId(self.get_arguments('id')[0])
                        except:
                            vCatId = None
                        if vCatId != None:
                            vCats = yield self.vehicleCategory.find(
                                        {
                                            '_id': vCatId,
                                            'entityId': self.entityId,
                                            'disabled': tDisabled
                                        },
                                        limit=1
                                    )
                            if len(vCats):
                                for v in vCats:
                                    v['id'] = str(v['_id'])
                                    del v['_id']
                                    del v['entityId']
                                    for idx, val in enumerate(v['vehicleType']):
                                        vType = yield self.vehicleType.find(
                                                {
                                                    '_id': ObjectId(val['id']),
                                                    'disabled': False,
                                                    'entityId': self.entityId
                                                },
                                                limit=1
                                            )
                                        if len(vType):
                                            val['name'] = vType[0]['name']
                                            val['id'] = str(val['id'])
                                    result.append(v)
                                status = True
                                code = 2000
                            else:
                                code = 3001
                                message = 'No Vehicle Categories Found.'
                        else:
                            try:
                                limit = int(self.get_arguments('limit')[0])
                            except:
                                limit = None

                            try:
                                skip = int(self.get_arguments('skip')[0])
                            except:
                                skip = 0

                            if limit != None:
                                vCats = yield self.vehicleCategory.find(
                                        {
                                            'entityId': self.entityId,
                                            'disabled': tDisabled
                                        },
                                        limit=limit,
                                        skip=skip
                                    )
                                if len(vCats):
                                    for v in vCats:
                                        v['id'] = str(v['_id'])
                                        del v['_id']
                                        del v['entityId']
                                        del v['vehicleType']
                                        result.append(v)
                                    status = True
                                    code = 2000
                                else:
                                    code = 3001
                                    message = 'No Vehicle Categories Found.'
                            else:
                                vCats = yield self.vehicleCategory.find(
                                        {
                                            'entityId': self.entityId,
                                            'disabled': tDisabled
                                        }
                                    )
                                if len(vCats):
                                    for v in vCats:
                                        v['id'] = str(v['_id'])
                                        del v['_id']
                                        del v['entityId']
                                        if shrink:
                                            del v['vehicleType']
                                        else:
                                            for idx, val in enumerate(v['vehicleType']):
                                                vType = yield self.vehicleType.find(
                                                    {
                                                        '_id': ObjectId(val['id']),
                                                        'disabled': False,
                                                        'entityId': self.entityId
                                                    },
                                                    limit=1
                                                )
                                                if len(vType):
                                                    val['name'] = vType[0]['name']
                                                    val['id'] = str(val['id'])
                                                    urlPath = '{0}/{1}/{2}/{3}/{4}/{5}'
                                                    urlPath = urlPath.format(
                                                            FileUtil.serverUrl,
                                                            'uploads',
                                                            str(self.entityId),
                                                            'vehicle/category',
                                                            v['id'],
                                                            val['id']
                                                        )
                                                    val['icon'] = urlPath + '/icon.svg'
                                                    val['marker'] = urlPath + '/marker.png'
                                        result.append(v)
                                    status = True
                                    code = 2000
                                else:
                                    code = 3001
                                    message = 'No Vehicle Categories Found.'
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

                        cName = self.request.arguments.get('name')
                        code, message = Validate.i(
                                    cName,
                                    'Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=40
                                )
                        if code != 4100:
                            raise Exception

                        cDescription = self.request.arguments.get('description')
                        code, message = Validate.i(
                                    cDescription,
                                    'Description',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=80
                                )
                        if code != 4100:
                            raise Exception
                        cVehicleTypes = self.request.arguments.get('vehicleType')
                        code, message = Validate.i(
                                    cVehicleTypes,
                                    'Vehicle Types',
                                    dataType=list,
                                    maxNumber=3,
                                    minNumber=1
                                )
                        if code != 4100:
                            raise Exception

                        cOnDemand = self.request.arguments.get('onDemand')
                        code, message = Validate.i(
                                    cOnDemand,
                                    'On Demand',
                                    dataType=bool
                                )
                        if code != 4100:
                            raise Exception

                        cScheduleEndTime = self.request.arguments.get('scheduleEndTime')
                        code, message = Validate.i(
                                    cScheduleEndTime,
                                    'Schedule End Time.',
                                    dataType=bool
                                )
                        if code != 4100:
                            raise Exception

                        for i, val in enumerate(cVehicleTypes):
                            try:
                                vType = yield self.vehicleType.find(
                                            {
                                                '_id': ObjectId(val['id'])
                                            },
                                            limit=1
                                        )
                                if len(vType):
                                    idx = {}
                                    idx['id'] = ObjectId(val['id'])
                                    cBasePrice = val.get('basePrice')
                                    code, message = Validate.i(
                                                cBasePrice,
                                                'Base Price',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['basePrice'] = cBasePrice
                                    cBaseHour = val.get('baseHour')
                                    code, message = Validate.i(
                                                cBaseHour,
                                                'Base Hour',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['baseHour'] = cBaseHour

                                    cBaseKm = val.get('baseKm')
                                    code, message = Validate.i(
                                                cBaseKm,
                                                'Base Km',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['baseKm'] = cBaseKm

                                    cPerKmRate = val.get('perKmRate')
                                    code, message = Validate.i(
                                                cPerKmRate,
                                                'Per KM Rate',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['perKmRate'] = cPerKmRate

                                    cPerHourRate = val.get('perHourRate')
                                    code, message = Validate.i(
                                                cPerHourRate,
                                                'Per Hour Rate',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['perHourRate'] = cPerHourRate

                                    cWaitingCharge = val.get('waitingCharge')
                                    code, message = Validate.i(
                                            cWaitingCharge,
                                            'Waiting Charge',
                                            dataType=float,
                                            minNumber=0,
                                            maxNumber=10000
                                        )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['waitingCharge'] = cWaitingCharge

                                    cNightHoldCharge = val.get('nightHoldCharge')
                                    code, message = Validate.i(
                                            cNightHoldCharge,
                                            'Night Hold Charge',
                                            dataType=float,
                                            minNumber=0,
                                            maxNumber=10000
                                        )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['nightHoldCharge'] = cNightHoldCharge

                                    cExtraPerKm = val.get('extraPerKm')
                                    code, message = Validate.i(
                                            cExtraPerKm,
                                            'Extra Per KM',
                                            dataType=float,
                                            minNumber=0,
                                            maxNumber=10000
                                        )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['extraPerKm'] = cExtraPerKm
                                    cCancellationCharge = val.get('cancellationCharge')
                                    code, message = Validate.i(
                                            cCancellationCharge,
                                            'Cancellation Charge',
                                            dataType=float,
                                            minNumber=0,
                                            maxNumber=10000
                                        )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['cancellationCharge'] = cCancellationCharge

                                    '''
                                        Number Passenger Category can aford
                                        Maximum no 5
                                        Minimum no 1
                                    '''
                                    cMaxPassenger = val.get('maxPassenger')
                                    code, message = Validate.i(
                                            cMaxPassenger,
                                            'Max Passenger',
                                            dataType=int,
                                            maxNumber=5,
                                            minNumber=1
                                    )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['maxPassenger'] = cMaxPassenger

                                    cVehicleTypes[i] = idx
                                else:
                                    raise Exception
                            except Exception as e:
                                Log.d('VTYPE-ARR', e)
                                if code == 4100:
                                    code = 4260
                                    message = 'Invalid Vehicle Type Id on Index {0}.'
                                    message = message.format(i + 1)
                                else:
                                    message = message + ' Index ' + str(i + 1)
                                raise Exception
                        try:
                            yield self.vehicleCategory.insert(
                                    {
                                        'disabled': False,
                                        'state': 30,
                                        'name': cName,
                                        'onDemand': cOnDemand,
                                        'scheduleEndTime': cScheduleEndTime,
                                        'description': cDescription,
                                        'vehicleType': cVehicleTypes,
                                        'entityId': self.entityId
                                    }
                                )
                            status = True
                            code = 2000
                            message = 'New Vehicle Category has been created.'
                        except:
                            status = False
                            code = 4280
                            message = 'This Vehicle Category is already exists.'
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

                        try:
                            vCatId = ObjectId(self.request.arguments['id'])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception

                        cDisabled = self.request.arguments.get('disabled')
                        code, message = Validate.i(
                                    cDisabled,
                                    'Disabled',
                                    dataType=bool
                                )
                        if code != 4100:
                            raise Exception

                        cName = self.request.arguments.get('name')
                        code, message = Validate.i(
                                    cName,
                                    'Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=40
                                )
                        if code != 4100:
                            raise Exception

                        cDescription = self.request.arguments.get('description')
                        code, message = Validate.i(
                                    cDescription,
                                    'Description',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    maxLength=80
                                )
                        if code != 4100:
                            raise Exception
                        cVehicleTypes = self.request.arguments.get('vehicleType')
                        code, message = Validate.i(
                                    cVehicleTypes,
                                    'Vehicle Types',
                                    dataType=list,
                                    maxNumber=3,
                                    minNumber=1
                                )
                        if code != 4100:
                            raise Exception

                        cOnDemand = self.request.arguments.get('onDemand')
                        code, message = Validate.i(
                                    cOnDemand,
                                    'On Demand',
                                    dataType=bool
                                )
                        if code != 4100:
                            raise Exception

                        cScheduleEndTime = self.request.arguments.get('scheduleEndTime')
                        code, message = Validate.i(
                                    cScheduleEndTime,
                                    'Schedule End Time.',
                                    dataType=bool
                                )
                        if code != 4100:
                            raise Exception

                        for i, val in enumerate(cVehicleTypes):
                            try:
                                vType = yield self.vehicleType.find(
                                            {
                                                '_id': ObjectId(val['id'])
                                            },
                                            limit=1
                                        )
                                if len(vType):
                                    idx = {}
                                    idx['id'] = ObjectId(val['id'])
                                    cBasePrice = val.get('basePrice')
                                    code, message = Validate.i(
                                                cBasePrice,
                                                'Base Price',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['basePrice'] = cBasePrice
                                    cBaseHour = val.get('baseHour')
                                    code, message = Validate.i(
                                                cBaseHour,
                                                'Base Hour',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['baseHour'] = cBaseHour

                                    cBaseKm = val.get('baseKm')
                                    code, message = Validate.i(
                                                cBaseKm,
                                                'Base Km',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['baseKm'] = cBaseKm

                                    cPerKmRate = val.get('perKmRate')
                                    code, message = Validate.i(
                                                cPerKmRate,
                                                'Per KM Rate',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['perKmRate'] = cPerKmRate

                                    cPerHourRate = val.get('perHourRate')
                                    code, message = Validate.i(
                                                cPerHourRate,
                                                'Per Hour Rate',
                                                dataType=float,
                                                minNumber=0,
                                                maxNumber=10000
                                            )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['perHourRate'] = cPerHourRate

                                    cWaitingCharge = val.get('waitingCharge')
                                    code, message = Validate.i(
                                            cWaitingCharge,
                                            'Waiting Charge',
                                            dataType=float,
                                            minNumber=0,
                                            maxNumber=10000
                                        )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['waitingCharge'] = cWaitingCharge

                                    cNightHoldCharge = val.get('nightHoldCharge')
                                    code, message = Validate.i(
                                            cNightHoldCharge,
                                            'Night Hold Charge',
                                            dataType=float,
                                            minNumber=0,
                                            maxNumber=10000
                                        )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['nightHoldCharge'] = cNightHoldCharge

                                    cExtraPerKm = val.get('extraPerKm')
                                    code, message = Validate.i(
                                            cExtraPerKm,
                                            'Extra Per KM',
                                            dataType=float,
                                            minNumber=0,
                                            maxNumber=10000
                                        )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['extraPerKm'] = cExtraPerKm

                                    cCancellationCharge = val.get('cancellationCharge')
                                    code, message = Validate.i(
                                            cCancellationCharge,
                                            'Cancellation Charge',
                                            dataType=float,
                                            minNumber=0,
                                            maxNumber=10000
                                        )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['cancellationCharge'] = cCancellationCharge

                                    '''
                                        Number Passenger Category can aford
                                        Maximum no 5
                                        Minimum no 1
                                    '''
                                    cMaxPassenger = val.get('maxPassenger')
                                    code, message = Validate.i(
                                            cMaxPassenger,
                                            'Max Passenger',
                                            dataType=int,
                                            maxNumber=5,
                                            minNumber=1
                                    )
                                    if code != 4100:
                                        raise Exception
                                    else:
                                        idx['maxPassenger'] = cMaxPassenger

                                    cVehicleTypes[i] = idx
                                else:
                                    raise Exception
                            except Exception as e:
                                Log.d('VTYPE-ARR', e)
                                if code == 4100:
                                    code = 4260
                                    message = 'Invalid Vehicle Type Id on Index {0}.'
                                    message = message.format(i + 1)
                                else:
                                    message = message + ' Index ' + str(i + 1)
                                raise Exception
                        try:
                            updateResult = yield self.vehicleCategory.find_and_modify(
                                    query = {
                                            '_id': vCatId,
                                            'entityId': self.entityId
                                        },
                                    update = {
                                        '$set': {
                                            'disabled': cDisabled,
                                            'name': cName,
                                            'onDemand': cOnDemand,
                                            'scheduleEndTime': cScheduleEndTime,
                                            'description': cDescription,
                                            'vehicleType': cVehicleTypes,
                                        }
                                    }
                            )
                            if updateResult:
                                status = True
                                code = 2000
                                message = 'Vehicle Category has been updated.'
                            else:
                                code = 4230
                                message = 'This Vehicle Category does not exist.'
                        except:
                            status = False
                            code = 4280
                            message = 'This Vehicle Category is already exists.'
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
                                'accountId': self.accountId,
                                'entityId': entityId,
                                'applicationId': applicationId
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
                            vTypeId = ObjectId(self.request.arguments['id'])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception
                        updateResult = yield self.vehicleCategory.find_and_modify(
                                    query = {
                                            '_id': vTypeId,
                                            'disabled': False
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
                            message = 'Vehicle Category has been Disabled.'
                        else:
                            code = 4210
                            message = 'This Vehicle Category does not exist.'
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

