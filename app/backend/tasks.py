#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
from celery import task
from app.backend.fb_jenkins import *
from app.backend.zbx_tool import *
import urllib
import jenkins
import salt.client, commands

local = salt.client.LocalClient()
import time
from datetime import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

jenkins_server_url = "http://127.0.0.1:8080"
host = "127.0.0.1"
user_id = "jenkins"
server = jenkins.Jenkins(jenkins_server_url, username=user_id, password="jenkins1234")
joblist = []


@task
def get_job_output(jobName):
    last = server.get_job_info(jobName)['lastBuild']['number']
    return server.get_build_console_output(jobName, last)


@task
def goto_html(full_name, jobName):
    result = get_job_output(full_name)
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_log = " {0} {1} 程序开始构建".format(start_time, full_name)
    parameters = {}
    project = 'erp-facade-achievement'
    parameters['project'] = project
    server.build_job(full_name, parameters)
    results = []
    workspace = result.split('Building in workspace')[1].strip().split('\n')[0]
    next_build_number = server.get_job_info(full_name)['nextBuildNumber']
    results.extend(
	[jobName, host, workspace, start_time, "", next_build_number, next_build_number, "执行开始", "result", result_log])
    return results


@task
def import_goto_html(ret):
    from app.backend.fb_jenkins import import_release_sql
    import_release_sql(ret)
    return True


@task
def import_goto_running(ret, jid):
    from app.backend.exec_jobs import import_release_sql
    import_release_sql(ret, jid)
    return True


@task
def update_goto_running(name, jid, statu):
    from app.backend.exec_jobs import update_release_sql
    update_release_sql(name, jid, statu)
    return True


@task
def import_schedule_running(ret, jid):
    from app.backend.exec_jobs import import_schedule_sql
    import_schedule_sql(ret, jid)
    return True


@task
def update_operate_running(ret, jid):
    from app.backend.exec_jobs import update_operate_sql
    update_operate_sql(ret, jid)
    return True


@task
def select_schedule_running(jid, time_now, action, command_names):
    from app.backend.exec_jobs import select_schedule_sql
    sel = select_schedule_sql(jid, time_now, action, command_names)
    return sel


@task
def update_schedule_running(name, jid, status):
    from app.backend.exec_jobs import update_schedule_sql
    update_schedule_sql(name, jid, status)
    return True


@task
def insert_schedule_running(scheduleName, result, time_now):
    from app.backend.exec_jobs import insert_schedule_sql
    insert_schedule_sql(scheduleName, result, time_now)
    return True


@task
def insert_operate_running(jid, results):
    from app.backend.exec_jobs import insert_operate_sql
    insert_operate_sql(jid, results)
    return True


@task
def get_job_runinng_in(full_name, ret):
    result = get_job_output(full_name)
    results = []
    jobName = ret[0]
    start_time = ret[3]
    workspace = ret[2]
    next_build_number = ret[5]
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for i in range(20):
	builds = server.get_running_builds()
	if len(builds) != 0: break
	time.sleep(0.2)
    result_log = ret[9] + "\n {0} {1} 程序构建中".format(time_now, full_name)
    results.extend(
	[jobName, host, workspace, start_time, "", next_build_number, next_build_number, "执行中", "result", result_log])
    import_goto_html(results)
    return results


@task
def get_job_runinng_end(full_name, ret):
    results = []
    jobName = ret[0]
    start_time = ret[3]
    workspace = ret[2]
    next_build_number = ret[5]
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time.sleep(3)
    while True:
	try:
	    build_info = server.get_build_info(full_name, next_build_number)
	except:
	    continue
	else:
	    if build_info[u'building'] == False:
		break
	    time.sleep(1)

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = get_job_output(full_name)
    result_log = ret[9] + "\n {0} {1} 程序构建中".format(time_now, full_name) + "\n {0} {1} 程序构建完成".format(end_time,
												      full_name)
    results.extend(
	[jobName, host, workspace, start_time, end_time, next_build_number, next_build_number, "执行成功", result,
	 result_log])
    import_goto_html(results)
    return results


@task
def get_job_running(full_name, jobName):
    result = get_job_output(full_name)
    workspace = result.split('Building in workspace')[1].strip().split('\n')[0]
    next_build_number = server.get_job_info(full_name)['nextBuildNumber']
    parameters = {}
    parameters['project0001'] = 'test001'
    server.build_job(full_name, parameters)
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_log = " {0} {1} 程序开始构建".format(start_time, full_name)
    results = []
    results.extend(
	[jobName, host, workspace, start_time, "", next_build_number, next_build_number, "执行开始", "result", result_log])
    import_goto_html(results)
    for i in range(50):
	builds = server.get_running_builds()
	if len(builds) != 0: break
	time.sleep(0.5)
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_log += "\n {0} {1} 程序构建中".format(time_now, full_name)
    results = []
    results.extend(
	[jobName, host, workspace, start_time, "", next_build_number, next_build_number, "执行中", "result", result_log])
    # print results
    import_goto_html(results)
    while True:
	builds = server.get_running_builds()
	try:
	    naer = builds[0]['name']
	except:
	    break
	else:
	    if full_name == naer:
		continue
	    time.sleep(1)
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results = []
    result = get_job_output(full_name)
    result_log += "\n {0} {1} 程序构建完成".format(end_time, full_name)
    # print results
    results.extend(
	[jobName, host, workspace, start_time, end_time, next_build_number, next_build_number, "执行成功", result,
	 result_log])
    import_goto_html(results)
    return results


@task
def get_zabbix_trigle():
    zabbix = zabbix_api()
    try:
	trigle = zabbix.get_trigle()
    except:
	return False
    else:
	if trigle is 'ok':
	    return 'update trigle success'


def pc2pcs(pc):
    pc = pc.split('[')[1].split(']')[0]
    pcs = ""
    n = 0
    for i in pc.split('u'):
	if i != '' and i != '"':
	    i = i.split("'")[1]
	    if n == 1:
		pcs = i
	    else:
		pcs = pcs + '|' + i
	n += 1
    return pcs


def isline(hostname):
    from app.backend.exec_jobs import select_salt_return
    line_id = local.cmd_async(hostname, 'test.ping', '', 'pcre')
    islines = select_salt_return(line_id)
    if not islines:
	return False
    else:
	return True


def file_output(editor, job_name, script, hostName, params):
    lines = isline(hostName)
    if lines is False:
	return False
    if script == 'shell':
	job_name = job_name.decode('utf-8').encode('utf-8')
	output = open('/data/auto_cmdb/exec_file/{0}.sh'.format(job_name), 'w')
	param_output = ""
	for param in params:
	    param_output = "{0}={1}".format(param['param_name'], param['param_value'])
	    output.write(param_output + '\n')
	output.write(editor)
	output.close()
	job_names = job_name + '.sh'
	local.cmd(hostName, 'cp.get_file',
		  ['salt://exec_file/{0}'.format(job_names), '/tmp/exec_job/{0}'.format(job_names), 'base', True], '',
		  'pcre')
	job_names = job_names.replace(" ", "\ ")
	job_id = local.cmd_async(hostName, 'cmd.run', ['bash  -xe /tmp/exec_job/{0}'.format(job_names)], 'pcre')
	command_names = 'bash  -xe /tmp/exec_job/{0}'.format(job_names)
    else:
	output = open('/data/auto_cmdb/exec_file/{0}.py'.format(job_name), 'w')
	output.write(editor)
	output.close()
	job_names = job_name + '.py'
	local.cmd(hostName, 'cp.get_file',
		  ['salt://exec_file/{0}'.format(job_names), '/tmp/exec_job/{0}'.format(job_names), 'base', True], '',
		  'pcre')
	job_names = job_names.replace(" ", "\ ")
	job_id = local.cmd_async(hostName, 'cmd.run', ['python /tmp/exec_job/{0}'.format(job_names)], 'pcre')
	command_names = 'bash  -xe /tmp/exec_job/{0}'.format(job_names)
    return job_id, command_names


@task
def work_running(jobName, user, hostName, script, action, editor, params):
    hostName = pc2pcs(hostName)
    if editor == "":
	if action != "":
	    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	    time_now2 = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
	    job_name = jobName + '_' + str(time_now2)
	    results = []
	    job_id = ""
	    end_time = ""
	    command = action
	    command_names = action
	    action = 'operate'
	    result = ""
	    results.extend(
		[job_name, user, '手动', time_now, end_time, 'unknow', '执行开始', job_id, action, result, command])
	    import_goto_running(results, job_id)
	    job_id = local.cmd_async(hostName, 'cmd.run', [command], 'pcre')
    else:
	time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	time_now2 = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
	job_name = jobName + '_' + str(time_now2)
	results = []
	job_id = ""
	action = 'operate'
	result = ""
	command = ""
	end_time = ""
	results.extend([job_name, user, '手动', time_now, end_time, 'unknow', '执行开始', job_id, action, result, command])
	import_goto_running(results, job_id)
	job_id, command_names = file_output(editor, job_name, script, hostName, params)
	if job_id is False:
	    statu = '执行失败'
	    update_goto_running(job_name, job_id, statu)
	    return False
    results = []
    results.extend([job_name, user, '手动', time_now, end_time, 'unknow', '执行中', job_id])
    ret = [job_name, time_now]
    statu = '执行中'
    update_goto_running(job_name, job_id, statu)
    results, status = select_schedule_running(job_id, time_now, action, command_names)
    return job_id, results


@task
def schedule_running(scheduleName, user, fun, action, id, all_result):
    results = []
    schedule_id = id
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_now2 = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    scheduleName = scheduleName + '_' + str(time_now2)
    result = ""
    command = ""
    end_time = ""
    action = "schedule"
    results.extend([scheduleName, user, fun, time_now, end_time, 'unknow', '执行开始', id, action, result, command])
    import_goto_running(results, schedule_id)
    for all_work in all_result:
	job_id, results, status = schedule_for_operate_running(all_work['name'], user, all_work['host'],
							       all_work['script'], all_work['action'],
							       all_work['editor'], scheduleName, all_work['list_id'],
							       schedule_id)
	if status == "执行失败":
	    break
    if status == "执行成功":
	insert_schedule_running(scheduleName, results, time_now)
    else:
	insert_schedule_running(scheduleName, results, time_now)
    return job_id, results, status


@task
def schedule_for_operate_running(jobName, user, hostName, script, action, editor, scheduleName, list_id, schedule_id):
    hostName = pc2pcs(hostName)
    if editor == "":
	if action != "":
	    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	    time_now2 = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
	    job_name = jobName + '_' + str(time_now2)
	    results = []
	    job_id = ""
	    end_time = ""
	    command = action
	    command_names = action
	    action = 'schedule'
	    result = ""
	    results.extend([job_name, user, '手动', time_now, end_time, 'unknow', '执行开始', job_id, action, result, command,
			    scheduleName, list_id])
	    import_schedule_running(results, job_id)
	    job_id = local.cmd_async(hostName, 'cmd.run', [command], 'pcre')
    else:
	time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	time_now2 = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
	job_name = jobName + '_' + str(time_now2)
	results = []
	job_id = ""
	action = 'schedule'
	result = ""
	command = ""
	end_time = ""
	results.extend(
	    [job_name, user, '手动', time_now, end_time, 'unknow', '执行开始', job_id, action, result, command, scheduleName,
	     list_id])
	import_schedule_running(results, job_id)
	from app.views import select_params
	params = select_params(schedule_id)
	job_id, command_names = file_output(editor, job_name, script, hostName, params)
    results = []
    results.extend([job_name, user, '手动', time_now, 'end time', 'unknow', '执行中', job_id])
    status = "执行中"
    update_schedule_running(job_name, job_id, status)
    results, status = select_schedule_running(job_id, time_now, action, command_names)
    return job_id, results, status


if __name__ == '__main__':
    get_zabbix_trigle()
    # get_job_running("运维测试2","运维测试2")
