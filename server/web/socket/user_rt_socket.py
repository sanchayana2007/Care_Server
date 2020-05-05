#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Real Time WebSocket Handler
'''

from lib import *

USER_RT_WS_CONNECTIONS = {
            'totalSocket': 0
        }

class MmsWebUserRealtimeWebSocketHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]

    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]

    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]

    vehicle = MongoMixin.serviceDb[
                    CONFIG['database'][1]['table'][4]['name']
                ]


    def __init__(self, application, request, **kwargs):
        cyclone.web.RequestHandler.__init__(self, application, request,
                                            **kwargs)
        self.application = application
        self.request = request
        self.transport = request.connection.transport
        self.ws_protocol = WebSocketProtocol(self)
        self.notifyFinish().addCallback(self.connectionLost)

    def initialize(self):
        self.key = None
        self.accountId = None
        self.entityId = None
        self.applicationId = None
        self.profileId = None
        self.time = timeNow()
        Log.i('[ US-SOC ]', 'Connection Request.')

    @defer.inlineCallbacks
    def _execute(self, transforms, *args, **kwargs):
        try:
            self.key = self.request.headers['Sec-Websocket-Key']
            Log.i('[ US-SOC ] Key', self.key)

            bearerToken = str(self.get_arguments('Authorization')[0])
            accountId = JWT_DECODE(bearerToken)
            if not accountId:
                raise Exception('Authorization')
            else:
                self.accountId = ObjectId(accountId)
                Log.i('[ US-SOC ] Authorization', self.accountId)

            xOriginKey = str(self.get_arguments('x-Origin-Key')[0])
            entityId = FN_DECRYPT(xOriginKey)
            if not entityId:
                raise Exception('x-Origin-Key')
            else:
                self.entityId = ObjectId(entityId)
                Log.i('[ US-SOC ] x-Origin-Key', self.entityId)

            xApiKey = str(self.get_arguments('x-Api-Key')[0])
            applicationId = FN_DECRYPT(xApiKey)
            if not applicationId:
                raise Exception('x-Api-Key')
            else:
                self.applicationId = ObjectId(applicationId)
                Log.i('[ US-SOC ] x-Api-Key', self.applicationId)

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
                        self.profileId = profile[0]['_id']
                        Log.i('[ US-SOC ]', 'Initialized, Profile: ' + str(self.profileId))
                    else:
                        raise Exception('Not Authorized.')
                else:
                    raise Exception('Not Authorized.')
            else:
                raise Exception('Not Authorized.')
        except Exception as e:
            template = 'Exception: {0}. Argument: {1!r}'
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error, Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            self.closeConnection(401)
            return
        try:
            self._transforms = transforms or list()
            self.request.connection.setRawMode()
            self.request.connection.rawDataReceived = \
                self.ws_protocol.rawDataReceived
            self.ws_protocol.acceptConnection()
        except Exception as e:
            template = 'Exception: {0}. Argument: {1!r}'
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error, Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))

    @defer.inlineCallbacks
    def connectionMade(self, *args, **kwargs):
        try:
            self.key = yield self.key
            '''
                Connecting To Redis
            '''
            self.setupRedis()

            Log.i('[ US-SOC ]', 'Connected.')
            '''
                Saving in a global Array
            '''
            '''
            oldConn = USER_RT_WS_CONNECTIONS.get(self.profileId)
            if oldConn == None:
                oldConn =   {
                                'connection': [self]
                            }
            else:
                oldConn['connection'].append(self)
            USER_RT_WS_CONNECTIONS[self.profileId] = oldConn
            '''
            USER_RT_WS_CONNECTIONS['totalSocket'] = USER_RT_WS_CONNECTIONS['totalSocket'] + 1
            Log.i('[ US-SOC ]', 'Total Connection : ' + str(USER_RT_WS_CONNECTIONS['totalSocket']))
        except Exception as e:
            self.closeConnection(500)
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5010
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error, Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        return

    @defer.inlineCallbacks
    def messageReceived(self, body=str):

        code = 4000
        status = False
        result = []
        message = ''

        self.cTime = timeNow()

        try:
            Log.d('[ US-SOC ] PID', self.profileId)
            try:
                # CONVERTS BODY INTO JSON
                args = yield json.loads(body)
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            # This Code defines the socket communication
            sCode = args.get('code')
            if type(sCode) != int:
                code = 4100
                message = 'Invalid Argument - [ code ].'
                raise Exception
            Log.d('[ US-SOC ] SCODE', sCode)
            if sCode == 2607191245:
                channelId = '{0}_{1}'.format(
                        'PROFILE',
                        self.profileId
                    )
                self.redis.subscribe(channelId)
                Log.i('[ US-SOC ] REDISH', 'SUBSCRIBE ChannelIDs: {0}'.format(
                        channelId
                    )
                )
                code = sCode
                status = True
                message = 'Self Profile is Connected.'
            elif sCode == 2407190836:
                subVehicle = []
                try:
                    '''
                        Subcribing All the Vehicle on that Type
                        Filters:
                         1. Entity Id
                         2. Type Id
                         3. Distance ( not set )
                         4. Limit ( not set )
                    '''
                    subVehicle = yield self.vehicle.find(
                            {
                                'entityId': self.entityId,
                                'disabled': False,
                                'typeId': ObjectId(args['result'][0]['vehicleTypeId']),
                                'location.1.time':
                                {
                                    '$gte': self.cTime - 1200000000
                                },
                                'location.0' :
                                { '$near' :
                                    {
                                        '$geometry' :
                                        {
                                            'type' : "Point" ,
                                            'coordinates' : args['result'][0]['coordinates']
                                        },
                                        '$maxDistance' : 5000
                                    }
                                }
                            },
                            {
                                '_id': 1
                            }
                    )
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = exc_tb.tb_frame.f_code.co_filename
                    Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                    code = 4030
                    message = 'Syntax Error.'
                    raise Exception
                if not len(subVehicle):
                    status = False
                    code = sCode
                    message = 'No Vehicle is available.'
                    raise Exception
                for val in subVehicle:
                    result.append(str(val['_id']))
                code = sCode
                status = True
            #
            #    Subscribe to specific Vehicles
            #
            elif sCode == 2507190836:
                for idx,val in enumerate(args['result']):
                    try:
                        v = yield self.vehicle.find(
                                {
                                    '_id': ObjectId(val)
                                },
                                {
                                    '_id': 1,
                                    'location': 1
                                },
                                limit=1
                            )
                        if not len(v):
                            raise Exception
                        else:
                            v = v[0]
                            r =     {
                                'id': str(v['_id']),
                                'latitude': v['location'][0]['coordinates'][1],
                                'longitude': v['location'][0]['coordinates'][0],
                                'orientation': v['location'][1]['orientation'],
                                'distance': v['location'][1]['distance'],
                                'ignition': v['location'][1]['ignition'],
                                'time': v['location'][1]['time'],
                                'speed': v['location'][1]['speed']
                            }
                            result.append(r)
                    except:
                        code = sCode
                        status = False
                        message = 'Invalid Vehicle Id Index: {0}'.format(idx)
                        raise Exception
                if len(result):
                    redishSubcribeId = []
                    for idx, val in enumerate(result):
                        channelId = '{0}_{1}'.format(
                                    'VLC',
                                    val['id']
                                )
                        self.redis.subscribe(channelId)
                        redishSubcribeId.append(channelId)
                    Log.i('[ US-SOC ] REDISH', 'SUBSCRIBE ChannelIDs: {0}'.format(
                            redishSubcribeId
                        )
                    )
                    status = True
                else:
                    code = sCode
                    status = False
                    message = 'No Vehicle Found.'
                code = sCode
            # Unsubcribe all vehicles
            elif sCode == 2607190836:
                for idx, val in enumerate(args['result']):
                    try:
                        v = ObjectId(val)
                    except:
                        code = sCode
                        status = False
                        message = 'Invalid Vehicle Id.'
                        raise Exception
                    channelId = '{0}_{1}'.format(
                            'VLC',
                            val
                        )
                    args['result'][idx] = channelId
                    self.redis.unsubscribe(channelId)
                Log.i('[ US-SOC ] REDISH', 'UNSUBSCRIBE ChannelIDs: {0}'.format(
                        args['result']
                    )
                )
                code = sCode
                status = True
            else:
                status = False
                code = sCode
                message = 'Unsupported Argument - [ code ].'
        except Exception as e:
            status = False
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error, Please Contact the Support Team.'
                Log.w('EXC', iMessage)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
                return
        if code == 4000:
            return
        response =  {
                        'code': code,
                        'status': status,
                        'message': message
                    }
        Log.d('[ US-SOC ] RESPONSE', response)
        try:
            response['result'] = result
            self.sendMessage(json.dumps(response))
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error, Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.sendMessage(json.dumps(response))
            return

    def sendMessage(self, data):
        self.ws_protocol.sendMessage(data)

    def _rawDataReceived(self, data):
        self.ws_protocol.handleRawData(data)


    def forbidConnection(self, message):
        self.transport.write(
            "HTTP/1.1 403 Forbidden\r\nContent-Length: %s\r\n\r\n%s" %
            (str(len(message)), message))
        return self.transport.loseConnection()

    def closeConnection(self, code):
        self.transport.write(
            "HTTP/1.1 %s Forbidden\r\nContent-Length: 5\r\n\r\n" %
            (str(code)))
        return self.transport.loseConnection()

    @defer.inlineCallbacks
    def connectionLost(self, reason):

        self.key = yield self.key
        '''
            Deleting the Old Socket Connection from Global
        '''
        '''
        oldConn = yield USER_RT_WS_CONNECTIONS.get(self.profileId)
        if oldConn != None:
            for idx, val in enumerate(oldConn['connection']):
                if val.key == self.key:
                    del oldConn['connection'][idx]
        '''
        '''
            Reducing Total Socket Number
        '''
        if self.profileId:
            USER_RT_WS_CONNECTIONS['totalSocket'] = \
                USER_RT_WS_CONNECTIONS['totalSocket'] - 1
            self.redis.punsubscribe('*')
            self.redis.quit()

        Log.i('[ US-SOC ] LOST-Key', self.key)
        Log.i('[ US-SOC ] LOST-Authorization', self.accountId)
        Log.i('[ US-SOC ] LOST-x-Origin-Key', self.entityId)
        Log.i('[ US-SOC ] LOST-x-Api-Key', self.applicationId)
        Log.i('[ US-SOC ] LOST-Profile', self.profileId)
        Log.i('[ US-SOC ] LOST', 'Total Connection : ' + str(USER_RT_WS_CONNECTIONS['totalSocket']))
        return

