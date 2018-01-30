#/usr/bin/python2.7
#encoding:utf-8

import urllib
import jenkins  
import time  
from datetime import datetime
import sys  
import MySQLdb  
  
jenkins_server_url="http://192.168.0.4:8080"
host="192.168.0.4"
user_id = "test"
api_token = "**********************"
#server=jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)  
server=jenkins.Jenkins(jenkins_server_url, username=user_id, password="test1234")  
joblist=[]

def get_job_info(jobName):
    joblist=server.get_job_info(jobName)  
    print joblist

def get_jobs_name():
    list=[]
    jobname=[]
    joburl=[]
    jobdate=[]
    jobn=[]
    list= server.get_info()['jobs']
    #print list
    for i in list:
	#print i['url']
        joba,jobb=get_job_time(i['name'])
        jobname.append(i['name'])
        joburl.append(i['url'])
        jobn.append(joba)
        jobdate.append(jobb)
    return jobname,joburl

def get_all_jobs_name():
    lists=[]
    job_name=[]
    job_url=[]
    job_date=[]
    job_id=[]
    full_name=[]
    ret = list()
    lists= server.get_all_jobs()
    for i in lists:
	full_name = i['fullname'].decode("utf-8")
        job_id,job_date=get_job_time(i['fullname'])
	job_name = i['name']
	job_url = str(i['url'])
	job_url = str(urllib.unquote(job_url))
 	job_status = server.get_job_config(str(full_name)).split('disabled>')[1].split('<')[0]
	if job_status == 'false':
	    job_status = "可用"
	else:
	    job_status = "不可用"
	#print i['name'],jobb,i['url'],joba
	value = (job_name,job_date,job_id,job_url,job_status,full_name)
	ret.append(value) 
    import_sql(ret)
    return ret	

def get_job_time(jobName):
    try:
    	last = server.get_job_info(str(jobName))['lastBuild']['number']
    except TypeError:
	last="未执行"
	last_date=""
	return last,last_date 
    else:	
    #print last
    	build_info = server.get_build_info(str(jobName), last)
    	#print build_info
    	timeStamp = str(build_info['timestamp'])[:-3]
    	tim = time.localtime(int(timeStamp))
    	last_date = time.strftime("%Y-%m-%d %H:%M:%S",tim)
    	return last,last_date

def import_sql(ret):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    sql_del = '''DELETE FROM `app_jenkins_return`'''
    set_names = '''set names utf8'''
    sql = '''INSERT INTO `app_jenkins_return`
                (`job_name`, `job_date`, `job_id`, `job_url`, `job_status`, `full_name`)
                VALUES ( %s, %s, %s, %s, %s, %s)'''
    try:
	print ret
    	cursor.execute(set_names)
    	cursor.execute(sql_del)
    	cursor.executemany(sql, ret)
    	cursor.execute("COMMIT") 
    except:
        conn.rollback()
    else:
	conn.close()

def import_history_sql(ret):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    sql_del = '''DELETE FROM `app_job_history_return`'''
    set_names = '''set names utf8'''
    sql = '''INSERT INTO `app_job_history_return`
                (`job_name`, `job_host`, `job_work`, `job_bigtime`, `job_endtime`, `job_index`, `pc_index`, `job_history`)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)'''
    try:
        cursor.execute(set_names)
        cursor.execute(sql_del)
        cursor.execute(sql, ret)
        cursor.execute("COMMIT")
    except:
        conn.rollback()
    else:
        conn.close()

def import_release_sql(ret):
    conn = MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
    cursor = conn.cursor()
    sql_del = '''DELETE FROM `app_job_release_return`'''
    set_names = '''set names utf8'''
    sql = '''INSERT INTO `app_job_release_return`
                (`job_name`, `job_host`, `job_work`, `job_starttime`, `job_endtime`, `job_index`, `pc_index`, `job_status`,`job_history`,`result_log`)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    try:
        cursor.execute(set_names)
        cursor.execute(sql_del)
        cursor.execute(sql, ret)
        cursor.execute("COMMIT")
    except:
        conn.rollback()
    else:
        conn.close()

def create_job(jobName):
    server.create_job(jobName,jenkins.EMPTY_CONFIG_XML)

def create_view(jobName):
    server.create_view(jobName, jenkins.EMPTY_VIEW_CONFIG_XML)

def delete_job(jobName):
    server.delete_job(jobName)

def build_job_info(jobName,parameters):
    print server.build_job(joName,parameters)
  
def get_job_output(jobName):
    last = server.get_job_info(jobName)['lastBuild']['number']
    return server.get_build_console_output(jobName,last)

def get_user():
    user = server.get_whoami()['fullName']  
    return user

def get_running(full_name,jobName):
    result = get_job_output(full_name)
    workspace = result.split('Building in workspace')[1].strip().split('\n')[0]
    next_build_number = server.get_job_info(full_name)['nextBuildNumber']
    parameters = {}
    parameters['project0001'] = 'test001'
    server.build_job(full_name,parameters)
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_log = " {0} {1} 程序开始构建".format(start_time,full_name)
    try:
	results = []
	results.extend([jobName,host,workspace,start_time,"end_time",next_build_number,next_build_number,"执行开始","result",result_log])
	import_release_sql(results)
	return results
    finally:
        for i in range(50):
	    builds = server.get_running_builds()
	    if len(builds)!=0:break
	    time.sleep(1)
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result_log += "\n {0} {1} 程序构建中".format(time_now,full_name)
	results = []
	results.extend([jobName,host,workspace,start_time,"end_time",next_build_number,next_build_number,"执行中","result",result_log])
	import_release_sql(results)
	#return results
        while True:
            builds = server.get_running_builds()
	    try:
	        naer = builds[0]['name']
	    except:		
	        break
	    else:
	        if full_name == naer:
		    continue
		#print full_name + "程序构建中"
	    time.sleep(1)
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	results = []
        result = get_job_output(full_name)
        result_log += "\n {0} {1} 程序构建完成".format(end_time,full_name)
	#print result_log
        results.extend([jobName,host,workspace,start_time,end_time,next_build_number,next_build_number,"执行成功",result,result_log])
        import_release_sql(results)
        return results
    

def get_one_result(full_name,jobName):
    results = []
    result = get_job_output(full_name)
    try:
	workspace = result.split('Building in workspace')[1].strip().split('\n')[0]
	last = server.get_job_info(full_name)['lastBuild']['number']
    except:
	print "返回格式错误，请查看返回信息"
    else:	
        try:
    	    lines = result.split('Finished at:')[1].strip()
	except:
	    big_verify_time = "time error"
	else:
	    big_verify_time =  lines.split('\n')[0]
	try: 
    	    lines = result.split('Finished at:')[2].strip()
    	    big_end_time = lines.split('\n')[0]
    	except:
	    print "返回格式错误，请查看返回信息"
	    big_end_time = big_verify_time
            results.append(jobName)
            results.append(host)
            results.append(workspace)
            results.append(big_verify_time)
            results.append(big_end_time)
            results.append(last)
            results.append(last)
            results.append(result)
	    #print results
            import_history_sql(results)
        else:
	    results.append(jobName)
    	    results.append(host)
    	    results.append(workspace)
    	    results.append(big_verify_time)
    	    results.append(big_end_time)
    	    results.append(last)
    	    results.append(last)
	    results.append(result)
	    import_history_sql(results)
        return results

if __name__ == '__main__':  
    jobName='运维测试2'
    full_name='运维测试2'

    get_running(full_name,jobName)

