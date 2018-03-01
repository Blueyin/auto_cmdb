#/usr/bin/python2.7
#encoding:utf-8

import urllib
import jenkins  
import time  
from datetime import datetime
import sys  
import MySQLdb  
conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")

def import_release_sql(ret,jid):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    #if jid !='':
	#print ret
        #sql_del = '''DELETE FROM `app_running_list` WHERE jid = %s and name = %s'''
    set_names = '''set names utf8'''
    sql = '''INSERT INTO `app_running_list`
                (`name`, `user`, `fun`, `start_time`, `end_time`, `sum_time`, `status`,`jid`,`action`,`result`,`command`)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    #print sql,ret
    try:
        cursor.execute(set_names)
        #cursor.execute(sql_del,jid)
        cursor.execute(sql, ret)
        cursor.execute("COMMIT")
    except:
        conn.rollback()
    else:
        conn.close()
    return True

def update_release_sql(name,jid,status):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    set_names = '''set names utf8'''
    sql = "UPDATE app_running_list SET  jid='%s',status='%s' WHERE name='%s'" % (jid,status,name)
    cursor.execute(set_names)
    try:
        cursor.execute(sql)
        cursor.execute("COMMIT")
    except:
        conn.rollback()
    else:
        conn.close()
    return True

def update_operate_sql(jid,ret):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    set_names = '''set names utf8'''
    sql = "UPDATE app_schedule_running_list SET  status='%s',end_time='%s',sum_time='%s',result='%s',command='%s' WHERE jid='%s'" % (ret[0],ret[1],ret[2],ret[3],ret[4],jid)
    cursor.execute(set_names)
    try:
        cursor.execute(sql)
        cursor.execute("COMMIT")
    except:
        conn.rollback()
    else:
        conn.close()
    return True


def insert_operate_sql(jid,ret):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    set_names = '''set names utf8'''
    sql = "UPDATE app_running_list SET  status='%s',end_time='%s',sum_time='%s',result='%s',command='%s' WHERE jid='%s'" % (ret[0],ret[1],ret[2],ret[3],ret[4],jid)
    cursor.execute(set_names)
    try:
        cursor.execute(sql)
        cursor.execute("COMMIT")
    except:
        conn.rollback()
    else:
        conn.close()
    return True


def select_salt_return(jid):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    set_names = '''set names utf8'''
    sql = "select * from app_salt_return where jid='%s'" % (jid)
    n = 1
    while True:
        cursor.execute(set_names)
        cursor.execute(sql)
        sel = cursor.fetchall()
        if sel:
            conn.close()
            break
        else:
            n += 1
            time.sleep(1)
        if n >= 10:
            return False
    if sel[0][5] == '1' or sel[0][5] == 'success' or sel[0][5] == 'True':
        return True
    else:
        return False

def select_schedule_sql(jid,time_now,action):
    import datetime
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    set_names = '''set names utf8'''
    sql = "select * from app_salt_return where jid='%s'" % (jid)
    #sql = "select * from app_salt_return where jid='20171228143649111939'"
    cursor.execute(set_names)
    results = []
    result = ""
    while True:
        cursor.execute(sql)
        sel = cursor.fetchall()
	if sel:
	    break
	else:
	   time.sleep(1)
    conn.close()
    ret = sel[0][6]
    if sel[0][5] == '1' or sel[0][5] == 'success' or sel[0][5] == 'True':
        end_time = ret.split('_stamp": "')[1].split('"')[0]
        end_time = utc2local(end_time)
        sum_time = end_time - datetime.datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
	numb = 0
	command = str(ret.split('fun_args": ["')[1].split('"')[0])
	status = "执行成功"
        for rets in sel:
	    ret = rets[6]
	    if result == "":
    		id = str(ret.split('"id": "')[1].split('"')[0])
            	result = id + '\n' + str(ret.split('return": "')[1].split('"')[0]) + '\n'
	    else:
		id = str(ret.split('"id": "')[1].split('"')[0])
		result = result + id + '\n' + str(ret.split('return": "')[1].split('"')[0]) 
	    numb += 1
	if numb == 1:
	    result = str(ret.split('return": "')[1].split('"')[0])
        result = result.replace("'","\\\'")
        result = result.replace('"','\\\"')
        results = ["执行成功",end_time,sum_time,result,command]
    else:
        end_time = ret.split('_stamp": "')[1].split('"')[0]
        end_time = utc2local(end_time)
        sum_time = end_time - datetime.datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
        result = str(ret.split('return": "')[1].split('"')[0])
        command = str(ret.split('fun_args": ["')[1].split('"')[0])
	status = "执行失败" 
        for rets in sel:
            ret = rets[6]
            if result == "":
                id = str(ret.split('"id": "')[1].split('"')[0])
                result = id + '\n' + str(ret.split('return": "')[1].split('"')[0]) + '\n'
            else:
                id = str(ret.split('"id": "')[1].split('"')[0])
                result = result + id + '\n' + str(ret.split('return": "')[1].split('"')[0])
            numb += 1
        if numb == 1:
            result = str(ret.split('return": "')[1].split('"')[0])
        result = result.replace("'","\\\'") 
        result = result.replace('"','\\\"')
        results = ["执行失败",end_time,sum_time,result,command]
    if action == 'operate':
        insert_operate_sql(jid,results)
    elif action == 'schedule':
        update_operate_sql(jid,results)
    return results,status


def import_schedule_sql(ret,jid):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    set_names = '''set names utf8'''
    sql = '''INSERT INTO `app_schedule_running_list`
                (`name`, `user`, `fun`, `start_time`, `end_time`, `sum_time`, `status`,`jid`,`action`,`result`,`command`,`scheduleName`,`list_id`)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    #print sql,ret
    try:
        cursor.execute(set_names)
        #cursor.execute(sql_del,jid)
        cursor.execute(sql, ret)
        cursor.execute("COMMIT")
    except:
        conn.rollback()
    else:
        conn.close()
    return True


def utc2local(utc_st):
    import datetime
    utc_st = utc_st[:-7]
    utc_st = datetime.datetime.strptime(utc_st, '%Y-%m-%dT%H:%M:%S')
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st



def insert_schedule_sql(scheduleName,results,time_now):
    import datetime
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    sum_time = results[1] - datetime.datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
    set_names = '''set names utf8'''
    sql = "UPDATE app_running_list SET  end_time='%s',sum_time='%s',status='%s' WHERE name='%s'" % (results[1],sum_time,results[0],scheduleName)
    cursor.execute(set_names)
    try:
        cursor.execute(sql)
        cursor.execute("COMMIT")
    except:
        conn.rollback()
    else:
        conn.close()
    return True


def update_schedule_sql(name,jid,status):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    set_names = '''set names utf8'''
    sql = "UPDATE app_schedule_running_list SET  jid='%s',status='%s' WHERE name='%s'" % (jid,status,name)
    cursor.execute(set_names)
    try:
        cursor.execute(sql)
        cursor.execute("COMMIT")
    except:
        conn.rollback()
    else:
        conn.close()
    return True
if __name__ == '__main__':  
    jobName='运维测试2'
    full_name='运维测试2'

