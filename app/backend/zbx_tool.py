#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import sys
import urllib2
import argparse
import MySQLdb
from urllib2 import URLError
from datetime import datetime,timedelta
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class zabbix_api:
    def __init__(self):
        self.url = 'http://127.0.0.1:81/api_jsonrpc.php'
	self.prioritytostr = {'0':'ok','1':'信息','2':'警告','3':'一般严重','4':'严重','5':'灾难'} #告警级别
        self.header = {"Content-Type":"application/json"}

    def user_login(self):
        data = json.dumps({
                           "jsonrpc": "2.0",
                           "method": "user.login",
                           "params": {
                                      "user": "blue",
                                      "password": "blue1234"
                                      },
                           "id": 0
                           })

        request = urllib2.Request(self.url, data)

        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "\033[041m 认证失败，请检查URL !\033[0m",e.code
        except KeyError as e:
            print "\033[041m 认证失败，请检查用户名密码 !\033[0m",e
        else:
            response = json.loads(result.read())
            result.close()
            #print response['result']
            self.authID = response['result']
            return self.authID

    def hostid_get_groupname(self, groupids= ''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output":["hostid","name"],
                "groupids": groupids,
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        request.add_header("Content-Type", "application/json")
        req = urllib2.urlopen(request)
        #print json.loads(req.read())
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            #print reqponse
            result.close()
        group_dict={}
        for groupid in response['result']:
            group_dict['name'] = groupid['name']
            group_dict['hostid'] = groupid['hostid']
        #return group_dict
            print "name:  \033[31m%s\033[0m \thostid : %s" % (groupid['name'], groupid['hostid'])

    def hostids_get_templatename(self, templateids = ''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output":["hostid","name"],
                "templateids": templateids,
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        request.add_header("Content-Type", "application/json")
        req = urllib2.urlopen(request)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
        tem_name=[]
        tem_hostid=[]
        for templateid in response['result']:
            tem_name.append(templateid['name'])
            tem_hostid.append(templateid['hostid'])
        return tem_name, tem_hostid


    def hostid_get_hostname(self, hostId=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter":
                    {"hostid": hostId}
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            #print response
            result.close()

            if not len(response['result']):
                print "hostId is not exist"
                return False

            host_dict=dict()
            for host in response['result']:
                status = {"0": "OK", "1": "Disabled"}
                available = {"0": "Unknown", "1": "available", "2": "Unavailable"}
                host_dict['name']=host['name']
                host_dict['status']=status[host['status']]
                host_dict['available']=available[host['available']]
                return host_dict

    def hostid_get_hostip(self, hostId=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostinterface.get",
            "params": {
                "output": "extend",
                "filter": {"hostid": hostId}
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            # print response
            result.close()

            if not len(response['result']):
                print "\033[041m hostid \033[0m is not exist"
                return False

            for hostip in response['result']:
                return hostip['ip']

    def host_get(self,hostName=''):
        data=json.dumps({
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                          "output": "extend",
                          "filter":{"host":hostName}
                          },
                "auth": self.user_login(),
                "id": 1
                })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            result.close()

            if not len(response['result']):
                print "\033[041m %s \033[0m is not exist" % hostName
                return False

            for host in response['result']:
                status ={"0":"OK","1":"Disabled"}
                available ={"0":"Unknown","1":"available","2":"Unavailable"}
                #print host
                if len(hostName)==0:
                    n = 1
                else:
                    n = 2
                    return host['hostid']

    def hostip_get(self, hostIp=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostinterface.get",
            "params": {
                "output": "extend",
                "filter": {"ip": hostIp}
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            # print response
            result.close()

            if not len(response['result']):
                print "\033[041m hostip \033[0m is not exist"
                return False

            print "主机数量: \33[31m%s\33[0m" % (len(response['result']))
            for hostip in response['result']:
                host = self.hostid_get_hostname(hostip['hostid'])
                if len(hostip) == 0:
                    print "HostID : %s\t HostName : %s\t HostIp : %s\t Status :\33[32m%s\33[0m \t Available :\33[31m%s\33[0m"%(hostip['hostid'],host['name'],hostip['ip'],host['status'],host['available'])
                else:
                    print "HostID : %s\t HostName : %s\t HostIp : %s\t Status :\33[32m%s\33[0m \t Available :\33[31m%s\33[0m"%(hostip['hostid'],host['name'],hostip['ip'],host['status'],host['available'])
                    return hostip['hostid']


    def hostgroup_get(self, hostgroupName='',hostName=''):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"hostgroup.get",
                           "params":{
                                     "output": "extend",
                               "filter": {
                                   "name": hostgroupName,
                                   "host": hostName,
                                   }
                           },
                           "auth": self.user_login(),
                           "id": 1,
                           })
        #print data,self.user_login()
        request = urllib2.Request(self.url, data)
        request.add_header("Content-Type", "application/json")
        req = urllib2.urlopen(request)
        # print json.loads(req.read())
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            # result.read()
            response = json.loads(result.read())
            result.close()
            #print response()
            if not len(response['result']):
                print "\033[041m %s \033[0m is not exist" % hostgroupName
                return False
            print response['result']
            for group in response['result']:
                groupids = group['groupid']
                if  len(hostgroupName)==0:
                    print "hostgroup:  \033[31m%s\033[0m \tgroupid : %s" %(group['name'],group['groupid'])
                    print zabbix.hostid_get_groupname(groupids=groupids)
                else:
                    print "hostgroup:  \033[31m%s\033[0m\tgroupid : %s" %(group['name'],group['groupid'])
                    print zabbix.hostid_get_groupname(groupids=groupids)
                    self.hostgroupID = group['groupid']
            return group['groupid']

    def template_get(self,templateName=''):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method": "template.get",
                           "params": {
                                      "output": "extend",
                                      "filter": {
                                                 "name":templateName
                                                 }
                                      },
                           "auth":self.user_login(),
                           "id":1,
                           })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            if not len(response['result']):
                return False
            reta = []
            retb = []
            retc = []
            retd = []
            rete = []
            result_data_tem = list()
            result_data_host = list()
            for template in response['result']:
                if len(templateName) == 0:
                    reta.append(template['templateid'])
                    retb.append(template['name'])
                    if self.hostids_get_templatename(templateids=template) is None:
                        retc.append('None')
                        retd.append('None')
                        rete.append(template['name'])
                    else:
                        (n,m) = self.hostids_get_templatename(templateids=template)
                        for i in n:
                            rete.append(template['name'])
                            retc.append(i)
                        for i in m:
                            retd.append(i)
                else:
                    self.templateID = response['result'][0]['templateid']
                    return response['result'][0]['templateid']

            sql_del = '''DELETE FROM `app_zabbix_tem_return`'''
            sql_del2 = '''DELETE FROM `app_zabbix_host_return`'''
     
            for i in range(len(reta)):
                values = (reta[i], retb[i])
                result_data_tem.append(values)
            for i in range(len(retc)):
                values = (rete[i], retc[i],retd[i])
                result_data_host.append(values)
            conn = MySQLdb.connect(host="192.168.0.192", user="test", passwd="test_1234", db="cmdb", charset="utf8")
            cursor = conn.cursor()

            sql_one = '''INSERT INTO `app_zabbix_tem_return`
                (`tem_id`, `template`)
                VALUES ( %s, %s)'''
            sql_two = '''INSERT INTO `app_zabbix_host_return`
                (`template`, `name`, `host_id`)
                VALUES ( %s, %s, %s)'''

            try:
                cursor.execute(sql_del)
                cursor.executemany(sql_one,result_data_tem)
                cursor.execute(sql_del2)
                cursor.executemany(sql_two,result_data_host)
                cursor.execute("COMMIT")
            except:
                conn.rollback()
                return 'false'
            else:
                conn.close()
                return 'ok'

    def get_trigle(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "only_true": '1',
                "skipDependent": '1',
                "monitored": '1',
                "active": '1',
                "output": "extend",
                "selectHosts": "['host']"
            },
            "auth":self.user_login(),
            "id": 1
        })
	ret = list()
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            result.close()
            for t in response['result']:    
		if int(t['value']) == 1:
                    name = self.hostid_get_hostname(hostId = t['hosts'][0]['hostid'])['name']
		    host = self.hostid_get_hostip(hostId = t['hosts'][0]['hostid'])
		    description = t['description']
		    priority = self.prioritytostr[t['priority']]
                    lasttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(t['lastchange'])))
		    values = (name,host,description,priority,lasttime)
                    ret.append(values)
	    self.import_sql_trigle(ret)
	    return  'ok'


    def hostgroup_create(self,hostgroupName):
        if self.hostgroup_get(hostgroupName):
            print "hostgroup  \033[42m%s\033[0m is exist !" % hostgroupName
            sys.exit(1)

        data = json.dumps({
                          "jsonrpc": "2.0",
                          "method": "hostgroup.create",
                          "params": {
                          "name": hostgroupName
                          },
                          "auth": self.user_login(),
                          "id": 1
                          })
        request=urllib2.Request(self.url,data)

        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print "添加主机组:%s  hostgroupID : %s"%(hostgroupName,self.hostgroup_get(hostgroupName))

    def host_create(self, hostIp, hostgroupName, templateName, hostName):
        if self.host_get(hostName) or self.hostip_get(hostIp):
            print "该主机已经添加!"
            sys.exit(1)

        group_list=[]
        template_list=[]
        for i in hostgroupName.split(','):
            var = {}
            var['groupid'] = self.hostgroup_get(i)
            group_list.append(var)
        for i in templateName.split(','):
            var={}
            var['templateid']=self.template_get(i)
            template_list.append(var)

        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"host.create",
                           "params":{
                                     "host": hostName,
                                     "interfaces": [
                                     {
                                     "type": 1,
                                     "main": 1,
                                     "useip": 1,
                                     "ip": hostIp,
                                     "dns": "",
                                     "port": "10050"
                                      }
                                     ],
                                   "groups": group_list,
                                   "templates": template_list,
                                     },
                           "auth": self.user_login(),
                           "id":1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
            print "add host : %s id :%s" % (hostIp, hostName)
        except URLError as e:
            print "Error as ", e
        except KeyError as e:
            print "\033[041m 主机添加有误，请检查模板正确性或主机是否添加重复 !\033[0m",e
            print response

    def host_disable(self,hostip):
        data=json.dumps({
                "jsonrpc": "2.0",
                "method": "host.update",
                "params": {
                "hostid": self.host_get(hostip),
                "status": 1
                },
                "auth": self.user_login(),
                "id": 1
                })
        request = urllib2.Request(self.url,data)
        for key in self.header:
                request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print '------------主机现在状态------------'
            print self.host_get(hostip)

    def host_enable(self,hostip):
        data=json.dumps({
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
            "hostid": self.host_get(hostip),
            "status": 0
            },
            "auth": self.user_login(),
            "id": 1
            })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
            #result = opener.open(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print '------------主机现在状态------------'
            print self.host_get(hostip)

    def host_delete(self,hostNames):
        hostid_list=[]
        for hostName in hostNames.split(','):
            hostid = self.host_get(hostName=hostName)
            if not hostid:
                print "主机 \033[041m %s\033[0m  删除失败 !" % hostName
                sys.exit()
            hostid_list.append(hostid)

        data=json.dumps({
                "jsonrpc": "2.0",
                "method": "host.delete",
                "params": hostid_list,
                "auth": self.user_login(),
                "id": 1
                })

        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
            result.close()
            print "主机 \033[041m %s\033[0m  已经删除 !" % hostName
        except Exception,e:
            print  e

    def template_addhost(self,template_id,host_id):
        hosts = list()
        for i in host_id:
            host = {"hostid": i}
            hosts.append(host)
        data = json.dumps({
                            "jsonrpc": "2.0",
                            "method": "template.massadd",
                            "params": {
                                "templates": [
                                    {
                                        "templateid": template_id
                                    }
                                ],
                                "hosts": hosts
                            },
                            "auth": self.user_login(),
                            "id": 1
                        })
        request = urllib2.Request(self.url, data)

        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
	    print result.read()
            return "添加主机到模板成功"

    def template_removehost(self, template_id, host_id):
        hosts = list()
        data = json.dumps({
            		"jsonrpc": "2.0",
            		"method": "template.massremove",
            		"params": {
                	    "templateids": template_id,
                	    "hostids": host_id
            		},
            		"auth": self.user_login(),
            		"id": 1
        		})
        request = urllib2.Request(self.url, data)

        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
	    print result.read()
	    #print data
	    return "删除主机到模板成功"

    def host_removetemplate(self, template_id, host_id):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.massremove",
            "params": {
                "hostids": host_id,
                "templateids_clear": template_id
            },
            "auth": self.user_login(),
            "id": 1
        })

        request = urllib2.Request(self.url, data)

        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            print result.read()
	    return  "删除主机到模板成功"

    def get_maintenance(self):
        params = {
            "output": "extend",
            "selectGroups": "extend",
            "selectHosts": "extend",
            "selectTimeperiods": "extend"
        }

        data = json.dumps({
                          "jsonrpc": "2.0",
                          "method": "maintenance.get",
                          "params": params,
                          "auth": self.user_login(),
                          "id": 1
                          })

        request = urllib2.Request(self.url,data)
        name = []
        active_till = []
        active_since = []
        maintenanceid = []
        ret = list()
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
        except URLError as e:
            print "Error as ", e
        except KeyError as e:
            return response
        else:
             for i in response['result']:
                hosts = ""
                for j in i['hosts']:
                    for key,value in  j.items():
                        if key == 'name':
                            hosts =hosts + "  " + value
                for key,value in i['timeperiods'][0].items():
                    if key == 'start_date':
                        oldtime = int(value)
                        time_since = time.localtime(int(value))
                        active_sinces = time.strftime("%Y-%m-%d %H:%M:%S",time_since)
                        active_since = active_sinces
                    if key == 'period':
                        keep_minutes = value
                date_old = datetime.fromtimestamp(oldtime)
                date_new = date_old + timedelta(seconds=int(keep_minutes))
                active_till = date_new.strftime('%Y-%m-%d %H:%M:%S')
                maintenanceid = i['maintenanceid']
                name=i['name']
                values = (name,hosts,maintenanceid,active_since,active_till)
                ret.append(values)
        self.import_sql(ret)
        return True

    def delete_maintenance(self, maintenanceid):
        data = json.dumps({
                          "jsonrpc": "2.0",
                          "method": "maintenance.delete",
                          "params": [
			       maintenanceid	
			   ],
                          "auth": self.user_login(),
                          "id": 1
                          })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])

        try:
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
        except URLError as e:
            print "Error as ", e
        except KeyError as e:
            return response
        else:
            return response

    def create_maintenance(self, maint_name, hostids, maint_time):
        #hostids = self.host_get(maint_host)
	#print maint_host,hostids
        #hostids = hostids.strip()
        now_time = int(time.time())
        date_old = datetime.fromtimestamp(time.time())
        data_new = date_old + timedelta(days=1024)
        new_main_time = int(time.mktime(data_new.timetuple()))
        period = int(maint_time) * 60
        params = {
            "name": maint_name,
            "active_since": now_time,
            "active_till": new_main_time,
            "hostids": hostids,
            "timeperiods": [
                {
                    "timeperiod_type": 0,
                    "period": period
                }
            ]
        }

        data = json.dumps({
                          "jsonrpc": "2.0",
                          "method": "maintenance.create",
                          "params": params,
                          "auth": self.user_login(),
                          "id": 1
                          })


        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()

        except URLError as e:
            return "Error as ", e
        except KeyError as e:
            return response

    def  import_sql(self, ret):
        conn = MySQLdb.connect(host="127.0.0.1",user="test",passwd="test_1234",db="cmdb",charset="utf8")
        cursor = conn.cursor()
        sql_del = '''DELETE FROM `app_zabbix_maintenance`'''
        set_names = '''set names utf8'''
        sql = '''INSERT INTO `app_zabbix_maintenance`
                (`name`, `host`, `maintenanceid`, `active_since`, `active_till`)
                VALUES ( %s, %s, %s, %s, %s)'''
        try:
            cursor.execute(set_names)
            cursor.execute(sql_del)
            cursor.executemany(sql, ret)
            cursor.execute("COMMIT")
        except:
            conn.rollback()
        else:
            conn.close()



    def  import_sql_trigle(self, ret):
        conn = MySQLdb.connect(host="127.0.0.1",user="test",passwd="test_1234",db="cmdb",charset="utf8")
        cursor = conn.cursor()
        sql_del = '''DELETE FROM `app_zabbix_trigle`'''
        set_names = '''set names utf8'''
        sql = '''INSERT INTO `app_zabbix_trigle`
                (`name`, `host`, `description`, `priority`, `lasttime`)
                VALUES ( %s, %s, %s, %s, %s)'''
        try:
            cursor.execute(set_names)
            cursor.execute(sql_del)
            cursor.executemany(sql, ret)
            cursor.execute("COMMIT")
        except:
            conn.rollback()
        else:
            conn.close()

if __name__ == "__main__":
    zabbix=zabbix_api()
    print zabbix.get_trigle()

    if len(sys.argv) == 1:
	     print 1
    else:
        args = parser.parse_args()
        if args.listhost != 'host':
            if args.listhost:
                zabbix.host_get(args.listhost)
            else:
                zabbix.host_get()
        if args.listgroup != 'group':
            if args.listgroup:
                zabbix.hostgroup_get(args.listgroup)
            else:
                zabbix.hostgroup_get()
        if args.listtemp != 'template':
            if args.listtemp:
                zabbix.template_get(args.listtemp)
            else:
                zabbix.template_get()
        if args.addgroup:
            zabbix.hostgroup_create(args.addgroup[0])
        if args.addhost:
            zabbix.host_create(args.addhost[0], args.addhost[1], args.addhost[2], args.addhost[3])
        if args.disablehost:
            zabbix.host_disable(args.disablehost)
        if args.deletehost:
            zabbix.host_delete(args.deletehost[0])



