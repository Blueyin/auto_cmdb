#!/usr/bin/python
#encoding:utf-8
import json
import MySQLdb
def __virtual__():
    return 'mysql_return'
def returner(ret):
    conn=MySQLdb.connect(host='127.0.0.1',user='test',passwd='test_1234',db='cmdb',port=3306)
    cursor=conn.cursor()
    sql = 'INSERT INTO app_salt_return(`fun`,`jid`,`result`,`host`,`success`,`full_ret`)VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql % (str(json.dumps(ret['fun'])),str(json.dumps(ret['jid'])),str(json.dumps(ret['return'])),str(json.dumps(ret['id'])),'"'+str(ret['success'])+'"',"'"+json.dumps(ret)+"'"))
    conn.commit()
    cursor.close()
    conn.close()
