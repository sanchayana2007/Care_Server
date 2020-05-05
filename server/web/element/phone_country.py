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
class PhoneCountryHandler(cyclone.web.RequestHandler, MongoMixin):

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

    phoneCountry = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][6]['name']
                ]

    @defer.inlineCallbacks
    def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            # TODO: this need to be moved in a global class
            entity = yield self.entity.find(
                                {
                                    '_id': self.entityId
                                },
                                limit=1
                            )
            if not len(entity):
                code = 4003
                message = 'You are not Authorized.'
                self.set_status(401)
                raise Exception

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
                vTypes = yield self.phoneCountry.find(
                                {
                                    '_id': vTypeId,
                                    'disabled': tDisabled
                                },
                                limit=1
                            )
                if len(vTypes):
                    for v in vTypes:
                        del v['_id']
                        result.append(v)
                    status = True
                    code = 2000
                else:
                    code = 3001
                    message = 'No Phone Country Found.'
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
                    vTypes = yield self.phoneCountry.find(
                                {
                                    'disabled': tDisabled
                                },
                                limit=limit,
                                skip=skip
                            )
                    if len(vTypes):
                        for v in vTypes:
                            del v['_id']
                        result.append(v)
                        status = True
                        code = 2000
                    else:
                        code = 3001
                        message = 'No Phone Country Found.'
                else:
                    vTypes = yield self.phoneCountry.find(
                                {
                                    'disabled': tDisabled
                                }
                            )
                    if len(vTypes):
                        for v in vTypes:
                            del v['_id']
                            result.append(v)
                        status = True
                        code = 2000
                    else:
                        code = 3001
                        message = 'No Phone Country Found.'

        except Exception as e:
            status = False
            result = []

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

