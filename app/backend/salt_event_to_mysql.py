#!/bin/env python
#coding=utf8

# Import python libs
import json

# Import salt modules
import salt.config
import salt.utils.event

# Import third party libs
import MySQLdb
__opts__ = salt.config.client_config('/etc/salt/master')

# Create MySQL connect
conn = MySQLdb.connect(host="127.0.0.1",user="test",passwd="test_1234",db="cmdb",charset="utf8")
cursor = conn.cursor()

# Listen Salt Master Event System
event = salt.utils.event.MasterEvent(__opts__['sock_dir'])
for eachevent in event.iter_events(full=True):
    ret = eachevent['data']
    print ret
    if "salt/job/" in eachevent['tag']:
        # Return Event
        if ret.has_key('id') and ret.has_key('return'):
            # Igonre saltutil.find_job event
            if ret['fun'] == "saltutil.find_job":
                continue
	    if ret['return'] == "True":
		continue
	    if ret['fun'] == "mine.update":
		continue
	    try:
		ret['success']
	    except:
		ret['success'] = "True"
            sql = '''INSERT INTO `app_salt_return`
                (`fun`, `jid`, `result`, `host`, `success`, `full_ret` )
                VALUES ( %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (ret['fun'], ret['jid'],
                                 json.dumps(ret['return']), ret['id'],
                                 ret['success'], json.dumps(ret)))
            cursor.execute("COMMIT")
    # Other Event
    else:
        pass
