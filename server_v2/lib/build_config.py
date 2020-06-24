#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SERVER BUILD LIBS

from __future__ import division

import sys
import json
import random
import asyncio
import requests
import tornado.gen as gen
import tornado.httpserver as httpserver
import tornado.platform.asyncio as tornado_asyncio
import tornado.web
#import uvloop
import time
import re
#import txmongo
import motor.motor_asyncio
import os
from bson.objectid import ObjectId

from datetime import datetime as dtime

from .log_util import Log

# SERVER CONFIGURATION FILE
CONFIG_FILE_PATH = '../configuration.json'

try:
    CONFIG_FILE = open(CONFIG_FILE_PATH)
    CONFIG = json.loads(CONFIG_FILE.read())
    CONFIG_FILE.close()

    # Project Code
    PROJECT_NAME = CONFIG['name']

    # Project Code
    PROJECT_CODE = CONFIG['projectCode']

    # WEB SERVER CONFIGURATION
    WEB_SERVER_PORT = CONFIG["instance"][2]['port']
    WEB_SERVER_INTERFACE = CONFIG["instance"][2]['host']

    # USER DB CONFIGURATION

    #USER_DBPOOL = txmongo.MongoConnection(
    #        CONFIG['database'][0]['host'],
    #        CONFIG['database'][0]['port'],
    #    )
    #USER_DATABASE = getattr(USER_DBPOOL, CONFIG['database'][0]['key'])

    # USER DB CONFIGURATION
    #SERVICE_DBPOOL = txmongo.MongoConnection(
    #        CONFIG['database'][1]['host'],
    #        CONFIG['database'][1]['port'],
    #    )
    #SERVICE_DATABASE = getattr(SERVICE_DBPOOL, CONFIG['database'][1]['key'])

    '''

    # Cassandra Configuration
    CASSANDRA_HOST = CONFIG['database'][2]['host']
    CASSANDRA_PORT = CONFIG['database'][2]['port']
    CASSANDRA_KEYSPACE = CONFIG['database'][2]['key']
    CASSANDRA_UNAME = CONFIG['database'][2]['username']
    CASSANDRA_PASS = CONFIG['database'][2]['password']
    CASSANDRA_TTL = CONFIG['database'][2]['ttl']

    CASSANDRA_DATABASE = cql_session.CassandraSession(
            [CASSANDRA_HOST],
            port=CASSANDRA_PORT,
            keyspace=CASSANDRA_KEYSPACE,
            username=CASSANDRA_UNAME,
            password=CASSANDRA_PASS
    )

    # Redis Configuration
    REDIS_SERVER_HOST = CONFIG['database'][3]['host']
    REDIS_SERVER_PORT = CONFIG['database'][3]['port']
    REDIS_SERVER_KEY = CONFIG['database'][3]['key']
    REDIS_SERVER_DB_ID = CONFIG['database'][3]['dbId']

    MAPS_GOOGLE_KEY = CONFIG['maps'][0]['key']
    '''

except Exception as e:
    status = False
    template = 'Exception: {0}. Argument: {1!r}'
    code = 5011
    iMessage = template.format(type(e).__name__, e.args)
    message = 'Internal Error Please Contact the Support Team.'
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = exc_tb.tb_frame.f_code.co_filename
    Log.c('BUILD-EXC', iMessage)
    Log.c('BUILD-EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))

# SMS GW configuration
# import sendotp
# # Msg 91 Gateway
# MSG91_GW = sendotp.sendotp(MSG91_GW_ID, SMS_GW_MESSAGE + ' ' + '{{otp}}.')
#
from sendotp import sendotp

MSG91_GW_ID = CONFIG['sms_gw'][0]['key']
SMS_GW_MESSAGE = CONFIG['name'] + ' verification code(OTP) is'
#otpobj =  sendotp.sendotp('190375ALnQVrF2Z5a46383e','my message is {{otp}} keep otp with you.')
MSG91_GW = sendotp.sendotp(MSG91_GW_ID, SMS_GW_MESSAGE + ' ' + '{{otp}}.')

# 3245 is the otp to send
#print(otpobj.send(919981534313,'msgind',3245))



