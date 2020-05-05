#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Real Time WebSocket Handler
'''

from utils import *
#from conn_config import WEB_SERVER_RT_WS_CONNECTIONS, WEB_SERVER_RT_WS_T_CONNECTION

class VtsRealtimeWebSocketHandler(cyclone.web.RequestHandler,
        MongoMixin, RedisMixin):

    #admin_profiles = MongoMixin.db.admin_profiles
    #users = MongoMixin.db.users
    #parent_profiles = MongoMixin.db.parent_profiles
    #apps = MongoMixin.db.applications
    #vehicles = MongoMixin.db.vehicles

    def __init__(self, application, request, **kwargs):
        cyclone.web.RequestHandler.__init__(self, application, request,
                                            **kwargs)
        self.application = application
        self.request = request
        self.transport = request.connection.transport
        self.ws_protocol = WebSocketProtocol(self)
        self.notifyFinish().addCallback(self.connectionLost)

    def initialize(self):
        #self.stats = stats
        Log.i('Connect', '')

    @defer.inlineCallbacks
    def _execute(self, transforms, *args, **kwargs):
        self.uid = None
        self.key = None
        try:
            uid = ObjectId(
                        JWT_DECODE(
                                self.get_arguments('wskey')[0]
                            )
                    )
            aid = str(self.get_arguments('application_id')[0])
            app = yield self.apps.find(
                        {
                            'application_id': aid
                        }
                    )
            if len(app):
                # For Admin Portal / Admin App
                if (app[0]['service_code'] == 'ADMIN'):
                    admin = yield self.admin_profiles.find(
                                {
                                    'user_id': uid
                                }
                            )
                    if len(admin):
                        self.uid = uid
                        self.aid = aid
                        self.key = self.request.headers['Sec-Websocket-Key']
                    else:
                        self.closeConnection(401)
                        return
                else:
                    self.closeConnection(401)
                    return
            else:
                self.closeConnection(401)
                return
        except Exception as e:
            print e, 'error'
            self.closeConnection(401)
            return
        self.time = timeNow()
        self._transforms = transforms or list()
        self.request.connection.setRawMode()
        self.request.connection.rawDataReceived = \
            self.ws_protocol.rawDataReceived
        self.ws_protocol.acceptConnection()

    @defer.inlineCallbacks
    def connectionMade(self, *args, **kwargs):
        self.uid = yield self.uid
        try:
            # Redis Client Setup
            self.setupRedis()
            if len(WEB_SERVER_RT_WS_CONNECTIONS):
                for i in range(len(WEB_SERVER_RT_WS_CONNECTIONS)):
                    state = WEB_SERVER_RT_WS_CONNECTIONS[i]
                    for s in range(len(state)):
                        ws = state[s]
                        if (ws.uid == self.uid):
                            if (len(state) == 3):
                                WEB_SERVER_RT_WS_T_CONNECTION.append(0)
                                state[0].forbidConnection('Maximum limit excceded')
                                state.append(self)
                                WEB_SERVER_RT_WS_CONNECTIONS[i] = state
                                Log.d('WS.OCONN', str(self.uid) + ' KEY: ' + str(self.key))
                                return
                            else:
                                state.append(self)
                                WEB_SERVER_RT_WS_CONNECTIONS[i] = state
                                WEB_SERVER_RT_WS_T_CONNECTION.append(0)
                                Log.d('WS-OCONN', str(self.uid) + ' KEY: ' + str(self.key))
                                Log.d('WS-TOTAL-SOC', len(WEB_SERVER_RT_WS_T_CONNECTION))
                                Log.d('WS-PER-CONN-SOC', len(state))
                                return
                        else:
                            WEB_SERVER_RT_WS_CONNECTIONS.append([self])
                            WEB_SERVER_RT_WS_T_CONNECTION.append(0)
                            Log.d('WS-NCONN', str(self.uid) + ' KEY: ' + str(self.key))
                            Log.d('WS-TOTAL-SOC', len(WEB_SERVER_RT_WS_T_CONNECTION))
                            Log.d('WS-PER-CONN-SOC', 1)
                            return
            else:
                WEB_SERVER_RT_WS_CONNECTIONS.append([self])
                WEB_SERVER_RT_WS_T_CONNECTION.append(0)
                Log.d('WS-NCONN', str(self.uid) + ' KEY: ' + str(self.key))
                Log.d('WS-TOTAL-SOC', len(WEB_SERVER_RT_WS_T_CONNECTION))
                Log.d('WS-PER-CONN-SOC', 1)
            # print WEB_SERVER_RT_WS_CONNECTIONS
        except:
            Log.i('WS-SOC', 'CODE 3, Format Error!')
        return

    @defer.inlineCallbacks
    def messageReceived(self, jmsg=str):
        self.uid = yield self.uid
        mtype = ''
        rmsg = ''
        scode = 2000
        data = []
        try:
            Log.i('WS-SOC', 'MSG: ' + jmsg)
            jmsg = json.loads(jmsg)
            mtype = str(jmsg['msg_type'])
            if (mtype == 'SUB_VEHICLE_STATUS'):
                vid = ObjectId(jmsg['data'][0]['id'])
                vh = yield self.vehicles.find(
                        {
                            '_id': ObjectId(vid)
                        }
                     )
                if len(vh):
                    self.redis.subscribe(str(vid))
                    rmsg = 'Vehicle has been Subscribed'
                else:
                    mtype = 'ERROR'
                    scode = 4111
                    rmsg = 'Invalid Vehicle Id'
            elif (mtype == 'UNSUB_VEHICLE_STATUS'):
                vid = ObjectId(jmsg['data'][0]['id'])
                vh = yield self.vehicles.find(
                        {
                            '_id': ObjectId(vid)
                        }
                     )
                if len(vh):
                    self.redis.unsubscribe(str(vid))
                    rmsg = 'Vehicle has been Unsubscribed'
                else:
                    mtype = 'ERROR'
                    scode = 4112
                    rmsg = 'Invalid Vehicle Id'
            else:
                scode = 4003
                rmsg = 'Unknown MSG TYPE'
        except:
            mtype = 'ERROR'
            scode = 4002
            rmsg = 'Invalid Syntax'
            data  = []
        resp =  {
                    'msg_type': mtype,
                    'status_code': scode,
                    'response': rmsg,
                    'data': data
                }
        self.sendMessage(resp)

    @defer.inlineCallbacks
    def sendMessage(self, data):
        self.uid = yield self.uid
        self.ws_protocol.sendMessage(data)

    def _rawDataReceived(self, data):
        self.ws_protocol.handleRawData(data)


    def forbidConnection(self, message):
        self.transport.write(
            "HTTP/1.1 403 Forbidden\r\nContent-Length: %s\r\n\r\n%s" %
            (str(len(message)), message))
        return self.transport.loseConnection()

    def closeConnection(self, ecode):
        self.transport.write(
            "HTTP/1.1 %s Forbidden\r\nContent-Length: 5\r\n\r\n" %
            (str(ecode)))
        return self.transport.loseConnection()

    @defer.inlineCallbacks
    def connectionLost(self, reason):
        self.uid = yield self.uid
        try:
            if (self.uid != None):
                for i in range(len(WEB_SERVER_RT_WS_CONNECTIONS)):
                    state = WEB_SERVER_RT_WS_CONNECTIONS[i]
                    for s in range(len(state)):
                        ws = state[s]
                        if (ws.key == self.key):
                            del state[s]
                            if len(state):
                                WEB_SERVER_RT_WS_CONNECTIONS[i] = state
                            else:
                                del WEB_SERVER_RT_WS_CONNECTIONS[i]
                            if len(WEB_SERVER_RT_WS_T_CONNECTION):
                                del WEB_SERVER_RT_WS_T_CONNECTION[0]
                            self.redis.quit()
                            Log.d('WS-LCONN', str(self.uid) + ' KEY: ' + str(self.key))
                            Log.d('WS-TOTAL-SOC', len(WEB_SERVER_RT_WS_T_CONNECTION))
                            Log.d('WS-PER-CONN-SOC', len(state))
                            return
            Log.d('WS-LCONN', str(self.uid) + ' KEY: ' + str(self.key))
            Log.d('WS-TOTAL-SOC', len(WEB_SERVER_RT_WS_T_CONNECTION))
        except:
            Log.e('WS-SOC', 'CODE 10, Format Error!')
        return

