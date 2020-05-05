#!/usr/bin/env python
# -*- coding: utf-8 -*-

from build_config import *
#from build_config import CASSANDRA_DATABASE

#from cassandra_util import *
from log_util import *
from redis_util import (
        RedisSubscriberProtocol, RedisSubscriberFactory, \
                RedisConnectionPool )
#from file_util import FileUtil

# Mongo Database Connection Class
class MongoMixin(object):

    userDb = USER_DATABASE
    serviceDb = SERVICE_DATABASE
    medicineDb = MEDICINE_DATABASE
    Log.i('MONGO', 'Service has been Initialized!')

# Redis Connection Class
class RedisMixin(object):

    qf = None
    ws = None
    stream = None

    # Redis Server Connection
    @classmethod
    @defer.inlineCallbacks
    def setup(self, host, port, dbid, poolsize):
        Log.i('REDISH', 'Stream Connected!')
        RedisMixin.qf = RedisSubscriberFactory()
        RedisMixin.qf.maxDelay = 20
        RedisMixin.qf.protocol = RedisPublisherProtocol

        # Normal client connection
        RedisMixin.stream = yield RedisConnectionPool(host, port,
                            dbid, poolsize)
    # Redis client connection Method
    def setupRedis(self):
        RedisMixin.ws = self
        self.rds = reactor.connectTCP(
                REDIS_SERVER_HOST,
                REDIS_SERVER_PORT,
                RedisMixin.qf
        )
        self.qf = RedisMixin.qf
        Log.i('REDISH', 'Client Setup Success!')

# Cassandra Database Connection Class
#class CassandraMixin(object):
#    session = CASSANDRA_DATABASE
#    Log.i('CASSANDRA', 'Session is Active!')

# Redis Protocol for handlling Websocket Group Publish
class RedisPublisherProtocol(RedisSubscriberProtocol):

    def messageReceived(self, status, channel, message):
        if status == None:
            self.ws.sendMessage(message)

    @defer.inlineCallbacks
    def connectionMade(self):
        try:
            self.redis = yield self
            self.ws = RedisMixin.ws
	    self.ws.redis = self
            RedisMixin.ws = None
            Log.i('REDIS', 'Connection Opened! S.KEY: ' + str(self.ws.key))
        except Exception as e:
            try:
                self.ws.closeConnection(401)
            except Exception as e1:
                e = e1
            template = 'Exception: {0}. Argument: {1!r}'
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error, Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            return



    def connectionLost(self, status):
        try:
            stat = str(status).replace(']', '')
            stats = stat.split('\'>:')
            Log.i('REDIS', 'Connection Lost! Status:' + stats[1])
        except:
            Log.i('REDIS', 'Connection Lost! Status: Unknown')

