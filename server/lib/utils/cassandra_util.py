#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement as CassandraQuery
from build_config import CASSANDRA_TTL

# Cassandra table description
CQL_TABLES = [ 'fcm_registrations', 'vehicle' ]

# Cassandra Prepared Statements
CQL_INSERT_VEHI_LOC = CassandraQuery(
        'INSERT INTO ' + CQL_TABLES[1] +'(id, time, distance, speed, ignition, location, source, orientation) VALUES(' + \
                '%s, %s, %s, %s, %s, %s, %s, %s) USING TTL ' + str(CASSANDRA_TTL))
CQL_GET_VEHI_LAST_LOC = CassandraQuery('SELECT * FROM ' + CQL_TABLES[1] + ' WHERE id=%s AND time < %s ORDER' + \
        ' BY time DESC LIMIT 1 ALLOW FILTERING')
CQL_DEL_VEHI_LOCS = CassandraQuery('DELETE FROM ' + CQL_TABLES[1] + ' WHERE id=%s')

CQL_GET_VEHI_LOCS_BY_INTERVAL = CassandraQuery(' SELECT * FROM ' + CQL_TABLES[1] + ' WHERE id=%s and time > %s and time < %s ALLOW FILTERING')

