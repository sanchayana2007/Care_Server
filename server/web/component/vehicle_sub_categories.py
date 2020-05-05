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
class VehicleCategoryFieldHandler(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('GET', 'POST', 'DELETE','PUT')

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

    vehicleCategoryField = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][3]['name']
                ]

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            '''
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body)
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            '''
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
                        # TODO: need  to add pagination
                        vCat = yield self.vehicleCategoryField.find(
                                    {
                                        'entityId': self.entityId,
                                        'active': True
                                    }
                                )
                        if len(vCat):
                            for v in vCat:
                                v['id'] = str(v['_id'])
                                del v['_id']
                                del v['active']
                                del v['entityId']
                                result.append(v)
                            status = True
                            code = 2000
                        else:
                            code = 3001
                            message = 'No Vehicle Category Fields Found.'
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

                        fName = self.request.arguments.get('name')
                        code, message = Validate.i(
                                    fName,
                                    'Name',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=60
                                )
                        if code != 4100:
                            raise Exception

                        fPlaceHolder = self.request.arguments.get('placeHolder')
                        code, message = Validate.i(
                                    fPlaceHolder,
                                    'Place Holder',
                                    dataType=unicode,
                                    notEmpty=True,
                                    noSpecial=True,
                                    noNumber=True,
                                    maxLength=80
                                )
                        if code != 4100:
                            raise Exception

                        fMinValue = self.request.arguments.get('minNumber')
                        code, message = Validate.i(
                                    fMinValue,
                                    'Min Value',
                                    dataType=int,
                                    notEmpty=True,
                                    maxNumber=100000,
                                    minNumber=0,
                                )
                        if code != 4100:
                            raise Exception

                        fMaxValue = self.request.arguments.get('maxNumber')
                        code, message = Validate.i(
                                    fMaxValue,
                                    'Max Value',
                                    dataType=int,
                                    maxNumber=100000,
                                    minNumber=0
                                )
                        if code != 4100:
                            raise Exception

                        try:
                            yield self.vehicleCategoryField.insert(
                                    {
                                        'active': True,
                                        'name': fName,
                                        'placeHolder': fPlaceHolder,
                                        'minValue': fMinValue,
                                        'maxValue': fMaxValue,
                                        'entityId': self.entityId
                                    }
                                )
                            status = True
                            code = 2000
                            message = 'New Vehicle Category has been created.'
                        except:
                            status = False
                            code = 4280
                            message = 'This Categories Field is already exists.'
                    else:
                        code = 4003
                        message = 'You are not authorized.'
                else:
                    code = 4003
                    message = 'You are not authorized.'
            else:
                code = 4003
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
            try:
                pId = ObjectId(self.uid)
            except:
                code = 4003
                message = 'You are not authorized.'
                raise Exception
            profile = yield self.profile.find(
                            {
                                '_id': pId
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

                        # TODO: need to create a global class for validation
                        regexSp = re.compile('[@_`+!#$%^&*()<>?/\-|}{~:,.]')
                        regexEm = re.compile('[@`+!#$%^&*()<>?/\|}{~:],')
                        regexNp = re.compile('[1234567890]')

                        cName = self.request.arguments.get('name')
                        if cName == None:
                            code = 4510
                            message = 'Missing Argument - [ name ].'
                            raise Exception
                        elif type(cName) != unicode:
                            code = 4511
                            message = 'Invalid Argument - [ name ].'
                            raise Exception
                        elif not len(str(cName)):
                            code = 4512
                            message = 'Please enter the Name.'
                            raise Exception
                        elif regexSp.search(cName) != None:
                            code = 4513
                            message = 'Name should not contain any special character.'
                            raise Exception
                        elif regexNp.search(cName) != None:
                            code = 4514
                            message = 'Name should not contain any number.'
                            raise Exception
                        elif len(cName) > 30:
                            code = 4515
                            message = 'Name should be less than 30 characters.'
                            raise Exception
                        elif ' ' in cName:
                            code = 4516
                            message = 'Name should not contain any white space.'
                            raise Exception
                        else:
                            cName = str(cName)

                        cDescription = self.request.arguments.get('description')
                        if cDescription == None:
                            code = 4520
                            message = 'Missing Argument - [ description ].'
                            raise Exception
                        elif type(cDescription) != unicode:
                            code = 4521
                            message = 'Invalid Argument - [ description ].'
                            raise Exception
                        elif not len(str(cDescription)):
                            code = 4522
                            message = 'Please enter the Description Name.'
                            raise Exception
                        elif len(cDescription) > 120:
                            code = 4525
                            message = 'Description name should be less than 120 characters.'
                            raise Exception
                        else:
                            cDescription = str(cDescription)

                        try:
                            vCatId = ObjectId(self.request.arguments['id'])
                        except:
                            code == 4310
                            message = 'Invalid Argument - [ id ].'
                            raise Exception

                        oCat = yield self.vehicleCategory.find(
                                {
                                    'name': cName,
                                    'entityId': profile[0]['entityId'],
                                    'active': True
                                },
                                limit=1
                            )
                        if len(oCat) and vCatId != oCat[0]['_id']:
                            status = False
                            code = 4280
                            message = 'This Vehicle Categories is already exists.'
                        else:
                            updateResult = yield self.vehicleCategory.find_and_modify(
                                    query = {
                                            '_id': vCatId
                                        },
                                    update = {
                                        '$set': {
                                            'name': cName,
                                            'description': cDescription,
                                        }
                                    }
                                )
                            if updateResult:
                                status = True
                                code = 2000
                                message = 'Vehicle Category details has been Updated.'
                            else:
                                code = 4210
                                message = 'This Vehicle Category does not exist.'
                    else:
                        code = 4003
                        message = 'You are not authorized.'
                else:
                    code = 4003
                    message = 'You are not authorized.'
            else:
                code = 4003
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
            try:
                pId = ObjectId(self.uid)
            except:
                code = 4003
                message = 'You are not authorized.'
                raise Exception
            profile = yield self.profile.find(
                            {
                                '_id': pId
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
                        updateResult = yield self.vehicleCategory.find_and_modify(
                                    query = {
                                            '_id': vCatId,
                                            'active': True
                                        },
                                    update = {
                                        '$set': {
                                            'active': False,
                                        }
                                    }
                            )
                        if updateResult:
                            status = True
                            code = 2000
                            message = 'Vehicle Category has been Removed.'
                        else:
                            code = 4210
                            message = 'This Vehicle Category does not exist.'
                    else:
                        code = 4003
                        message = 'You are not authorized.'
                else:
                    code = 4003
                    message = 'You are not authorized.'
            else:
                code = 4003
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

