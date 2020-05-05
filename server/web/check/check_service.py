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
class CheckServiceHandler(cyclone.web.RequestHandler, MongoMixin):

    SUPPORTED_METHODS = ('GET', 'POST', 'DELETE','PUT')

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    entity = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][5]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]

    serviceArea = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][5]['name']
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
                    if app[0]['apiId'] == 40216: # TODO: till here
                        try:
                            startPoint = [
                                            float(self.get_arguments('startLng')[0]),
                                            float(self.get_arguments('startLat')[0])
                                         ]
                        except:
                            code = 4120
                            message = 'Invalid Argument - [ Start Point ].'
                            raise Exception

                        try:
                            endPoint =  Point(
                                                float(self.get_arguments('endLng')[0]),
                                                float(self.get_arguments('endLat')[0])
                                            )
                        except:
                            code = 4120
                            message = 'Invalid Argument - [ End Point ].'
                            raise Exception

                        serviceArea = yield self.serviceArea.find(
                            {
                                'entityId': self.entityId,
                                'area':
                                {
                                    '$geoIntersects':
                                    {
                                        '$geometry':
                                        {
                                            'type' :
                                                'Point',
                                                'coordinates' : startPoint
                                        }
                                    }
                                }
                            },
                            limit=1
                        )
                        if len(serviceArea):
                            status = True
                            comVect = []
                            for idx in serviceArea[0]['area']['coordinates'][0]:
                                comVect.append(
                                        (
                                            idx[0],
                                            idx[1]
                                        )
                                    )
                            servicPolygon = Polygon(comVect)
                            withIn = servicPolygon.contains(endPoint)
                            if withIn:
                                code = 30
                            else:
                                code = 40
                        else:
                            code = 4100
                            message = 'Service is not available on that Area.'
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

