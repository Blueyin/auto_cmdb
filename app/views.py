#encoding=utf-8
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
from django.template import Template,loader,RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import auth
from django import  forms
from app.models import *
from app.backend.saltapi  import SaltAPI
from app.backend.es  import ES_SEARCH
from app.backend.key  import * 
from app.backend.fb_jenkins  import * 
from app.backend.asset_info import *
from app.backend.tasks import *
from app.backend.zbx_tool import *
import MySQLdb
#import MySQLdb as mysql
import  ConfigParser,sys,json,os,time,pickle
import time
db =  MySQLdb.connect(host="192.168.0.2",user="test",passwd="test_1234",db="cmdb",charset="utf8")
db.autocommit(True)
job_enable = 1
work_enable = 1


def saltstack():
    config = ConfigParser.ConfigParser()  
    config.read("/CMDB/app/backend/config.ini")
    url = config.get("saltstack","url")
    user = config.get("saltstack","user")
    passwd = config.get("saltstack","pass")
    device = config.get("network","device")
    result_api={'url':url,'user':user,'passwd':passwd,'device':device}
    return result_api
def wirte_track_mark(num):
    f = open("/CMDB/app/backend/track_num.conf",'w')
    try:
        f.write(num)
    finally:
        f.close()
    return "ok"
def read_track_mark():
    f = open("/CMDB/app/backend/track_num.conf")
    try:
	num = f.read()
    finally:
	f.close()
    return num
def date_result(data):
    timeArray = time.strptime(data, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray)) - 50400
    return timeStamp
 
@login_required
def index(request): 
    total_idc =Idc.objects.aggregate(Count('idc_name'))
    idc_num = total_idc["idc_name__count"]
    total_host = HostList.objects.aggregate(Count('hostname'))
    host_num = total_host["hostname__count"]
    return render_to_response("index.html",locals()) 
def login(request):
    return render_to_response("login.html")
def authin(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    total_idc =Idc.objects.aggregate(Count('idc_name'))
    idc_num = total_idc["idc_name__count"]
    user = auth.authenticate(username=username,password=password)
    total_host = HostList.objects.aggregate(Count('hostname'))
    host_num = total_host["hostname__count"]
    if user is not None:
            auth.login(request,user)
            return  render_to_response('index.html',{'login_user':request.user,'idc_num':idc_num,'host_num':host_num})
    else:
            return render_to_response('login.html',{'login_err':'Wrong username or password'})
@login_required
def idc(request):
    all_idc = Idc.objects.all()
    return render_to_response("idc.html",locals())
@login_required
def addidc(request):
    nameInput = request.GET['nameInput'] 
    msgInput = request.GET['msgInput'] 
    idc_add = Idc(idc_name=nameInput,remark=msgInput)
    idc_add.save()
    return HttpResponse('ok')
@login_required
def idc_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        Idc.objects.filter(id=id).delete()
        return HttpResponseRedirect('/idc/')
@login_required
def author(request):
    all_host = HostList.objects.all() 
    all_author = Author.objects.all()
    return render_to_response("author.html",locals())
@login_required
def addauthor(request):
    if request.method == 'GET':
        name = request.GET['name']
        user = request.GET['user']
        passwd = request.GET['passwd']
        key = request.GET['key']
        group = request.GET['group']
        author_add = Author(name=name,user=user,passwd=passwd,key=key,group=group)
        author_add.save()
        return HttpResponse('ok')
@login_required
def upauthor(request):
    if request.method == 'GET':
	name = request.GET['kname']
 	all_result = Author.objects.filter(name=name)	
	user = all_result.values()[0]['user']
	#user = request.GET['kuser']
	passwd = request.GET['kpasswd']
	# kip change ip
	old_ip = request.GET['kip']
        old_ip = json.loads(json.dumps(old_ip))
        main_ip =  old_ip.split('[')[1].split(']')[0]
	ip = []
        for ips in main_ip.split(','):
            ip.append(ips.split('"')[1])
	group = request.GET['kgroup']
	try:
	    cp(ip)
	    if group == 'yw':
                print ywadd(user, ip, group)
            elif group == 'dev':
                print add(user, ip, group)
            else:
                print bigdata(user, ip, group)
	except:
	    return HttpResponse('false')
	else:
	    return HttpResponse('ok')
@login_required
def author_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        all_result = Author.objects.filter(id=id)
        user = all_result.values()[0]['user']
	group = all_result.values()[0]['group']
	if group == 'dev':
	    devdel(user,group)
	elif group == 'bigdata':
	    bigdatadel(user,group)
        Author.objects.filter(id=id).delete()
        return HttpResponseRedirect('/author/')
@login_required
def author_edit(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        all_user = Author.objects.all()
        all_author = Author.objects.filter(id=id)
        return render_to_response("author_edit.html",locals())
def author_result(request):
    if request.method =='GET':
	id = request.GET['id']
        name = request.GET['name']
        key = request.GET['key']
        user = request.GET['user']
        passwd = request.GET['passwd']
	group = request.GET['group']
        try:
            author_update = Author.objects.filter(id=id).update(name=name,user=user,passwd=passwd,key=key,group=group)
            author_update.save()
        except:
            print "get exception"
        finally:
            return HttpResponse('ok')
@login_required
def key_result(request):
    if request.method == 'GET':
        ret_api = saltstack()
        #user = request.GET.get('user')
	user = Author.objects.filter(id=id)
        for user in user:
            key_id = user.user
	    key_group = user.group
            sapi = SaltAPI(url=ret_api["url"],username=ret_api["user"],password=ret_api["passwd"])
            ret = sapi.remote_execution(key_group,'cmd.run','ls')
            print salt_return.objects.all()
            all_result = salt_return.objects.all().order_by("-id")[0:1]
            for ret in all_result:
                print ret.result
                key_id = ret.host
                ret = ret.result
                r_data = {'host':key_id,'ret':ret}
                data = json.dumps(r_data)
                print data
                return HttpResponse(data)

class UploadForm(forms.Form):
    headImg = forms.FileField()

@login_required
def mac(request):
    all_host = HostList.objects.all()
    all_idc = Idc.objects.all()
    return render_to_response("mac.html",locals())


@login_required
def addmac(request):
    if request.method == 'GET':
        name = request.GET['name']
        ip = request.GET['ip'] 
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg'] 
        mac_add = HostList(ip=ip,hostname=name,application=service,idc_name=idc_name,bianhao=idc_bh) 
        mac_add.save()
        return HttpResponse('ok')
@login_required
def mac_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        HostList.objects.filter(id=id).delete()
        return HttpResponseRedirect('/mac/')
@login_required
def mac_edit(request,id=None):   
    if request.method == 'GET':
	id = request.GET.get('id')
	all_idc = Idc.objects.all()
        all_host=HostList.objects.filter(id=id)
	return render_to_response("mac_edit.html",locals())
@login_required
def macresult(request):
    if request.method =='GET':
        id = request.GET['id']
        ip = request.GET['ip']
        name = request.GET['name']
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg']
        try:
            mac_update = HostList.objects.filter(id=id).update(ip=ip,hostname=name,application=service,idc_name=idc_name,bianhao=idc_bh)
            mac_update.save()
	except:
	    print "get exception"
	finally: 
            return HttpResponse('ok') 
class UploadForm(forms.Form):
    headImg = forms.FileField()
@login_required
def file(request):
#    if request.method == 'POST':
    all_group = Group.objects.all()
    all_file = Upload.objects.all()
    uf = UploadForm(request.POST,request.FILES)
    if uf.is_valid():
        headImg = uf.cleaned_data['headImg']
        user = Upload()
        user.headImg = headImg
        user.save()
    return render_to_response('file.html',locals())
#    else:
#        uf = UserForm()
#        return render_to_response('file.html',{'uf':uf})  
@login_required
def file_result(request):
    if request.method == 'GET':
	import sys
	reload(sys)
	sys.setdefaultencoding( "utf-8" )
	g_name = request.GET.get('g_name')
	file = request.GET.get('file')
	dir = request.GET.get('dir')
	GroupList = Group.objects.all()
#	file_result = []
	list_coun = []
        project_success = []
        project_fail = []
	for groupname in GroupList:
            if groupname.name in g_name:
                print "slected group:",groupname.name
                for selected_ip in HostList.objects.filter(group__name = groupname.name):
                    host = HostList.objects.filter(ip=selected_ip.ip)
                    for host in host:
			key_id = host.hostname
			cmd = "salt %s cp.get_file salt://%s %s"%(key_id,file,dir)
     		        os.popen(cmd).read()
			list_coun.append(host)
                num = len(list_coun)
                wirte_track_mark(str(num))
                all_result = salt_return.objects.all()[0:num]
                for projects in all_result:
                    project=projects.success
                    if project == '1' or project == 'True':
                        project_success.append(project)
                    else:
                        project_fail.append(project)
                success_num = len(project_success)
                fail_num = len(project_fail)
                result = {'success':success_num,'fail':fail_num}
                return HttpResponse(json.dumps(result))
#			key_id = {'host':key_id,'ret':result}
#			file_result.append(key_id)
#		data = json.dumps(file_result)
#		print data
#		return HttpResponse(data)
@login_required
def command(request):
    if request.method == 'GET':
	all_host = HostList.objects.all()
    return render_to_response("command.html",locals())
@login_required
def command_result(request):
    if request.method == 'GET':
        ret_api = saltstack()
        ip = request.GET.get('ip')
        command = request.GET.get('command')
        host = HostList.objects.filter(ip=ip)
        for host in host:
            key_id = host.hostname
            sapi = SaltAPI(url=ret_api["url"],username=ret_api["user"],password=ret_api["passwd"])
            ret = sapi.remote_execution(key_id,'cmd.run',command)
	    #print salt_return.objects.all()
            time.sleep(0.8)
	    all_result = salt_return.objects.all().order_by("-id")[0:1]
	    for ret in all_result:
		print ret.result
		key_id = ret.host
		ret = ret.result
		r_data = {'host':key_id,'ret':ret}
                data = json.dumps(r_data)
                print data
                return HttpResponse(data)
@login_required
def command_group(request):
    if request.method == 'GET':
	all_group = Group.objects.all()
    return render_to_response("command_group.html",locals())
def command_group_result(request):
    if request.method == 'GET':
	ret_api = saltstack()
        g_name = request.GET.get('g_name')
        command = request.GET.get('command')
        selectIps = []
	list_coun = []
        project_success = []
	project_fail = []
        GroupList = Group.objects.all()
        for groupname in GroupList:
            if groupname.name in g_name:
                print "slected group:",groupname.name
                for selected_ip in HostList.objects.filter(group__name = groupname.name): 
                    host = HostList.objects.filter(ip=selected_ip.ip) 		
                    for host in host:
                        key_id = host.hostname 
                        sapi = SaltAPI(url=ret_api["url"],username=ret_api["user"],password=ret_api["passwd"])
                        ret = sapi.remote_execution(key_id,'cmd.run',command)
		        list_coun.append(host)
		num = len(list_coun)	
	        wirte_track_mark(str(num))
		all_result = salt_return.objects.all()[0:num]
		#print all_result
		for projects in all_result:
		    project=projects.success
		    if project == '1' or project == 'True':
			project_success.append(project) 
		    else:
			project_fail.append(project)
		success_num = len(project_success)
		fail_num = len(project_fail)
		result = {'success':success_num,'fail':fail_num}
                return HttpResponse(json.dumps(result))
@login_required
def check_result(request):
    num = int(read_track_mark())
    all_result = salt_return.objects.all().order_by("-id")[0:num]
    return render_to_response("check_result.html",locals())
@login_required
def job(request):
    return render_to_response("job.html")
@login_required
def bd_jenkins(request):
    global job_enable
    job_enable = 1
    all_result = jenkins_return.objects.all()
    return render_to_response("bd_jenkins.html",locals())
@login_required
def update_job(request):
    get_all_jobs_name() 
    return HttpResponse('ok')
    #all_result = jenkins_return.objects.all()
    #return render_to_response("bd_jenkins.html",locals())
def job_history(request):
    if request.method == 'GET':
	try:
            id = request.GET.get('id')
            all_result = jenkins_return.objects.filter(id=id)
	    job_name = all_result[0]
            full_name = all_result.values()[0]['full_name']
	    get_one_result(full_name,job_name)
	    all_result = job_history_return.objects.all()
	except:
	    all_result = job_history_return.objects.filter(id=id)
            return render_to_response("job_history.html",locals())
	else:
    	    return render_to_response("job_history.html",locals())
def job_history_result(request):
    if request.method == 'GET':
        id = request.GET.get('id')
	all_result = job_history_return.objects.filter(id=id)
	return render_to_response("job_history_result.html",locals())
def job_release(request):
    if request.method == 'GET':
	try:
	    global job_enable
	    id = request.GET.get('id')
   	    name =  request.GET.get('name') 
            all_result = jenkins_return.objects.filter(id=id)
            job_name = all_result[0]
	    full_name = all_result.values()[0]['full_name']
	except:
	    all_result = job_release_return.objects.filter(id=id)
	    return render_to_response("job_release.html",locals())
	else:
	    if job_enable == 1: 
	        res = goto_html.delay(full_name,job_name)
	        import_goto_html.delay(res.get())
	        ret_in = get_job_runinng_in.delay(full_name,res.get())
	        ret_end =get_job_runinng_end.delay(full_name,res.get())
	        job_enable = 0
	    time.sleep(0.5)
	    all_result = job_release_return.objects.all()
	    return render_to_response("job_release.html",locals())
def job_release_result(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        all_result = job_release_return.objects.filter(id=id)
        return render_to_response("job_release_result.html",locals())
@login_required
def asset(request):
    all_asset = ServerAsset.objects.all()    
    return render_to_response("asset.html",locals())
@login_required
def asset_auto(request):
    all_host = HostList.objects.all()
    return render_to_response("asset_auto.html",locals())
@login_required
def asset_auto_result(request):
     if request.method == 'GET':
	ret_api = saltstack()
	try:
	    client = request.GET.get('client')
	    result = get_server_asset_info(client,ret_api["url"],ret_api["user"],ret_api["passwd"],ret_api["device"])
	except:
	    result = get_server_asset_info(client,ret_api["url"],ret_api["user"],ret_api["passwd"],"eth1")
	else:
	    a=1 
	try:
            result_data = ServerAsset()
            result_data.manufacturer = result[0][0]
            result_data.productname = result[0][1]
            result_data.service_tag = result[0][2]
            result_data.cpu_model = result[0][3]
            result_data.cpu_nums = result[0][4]
            result_data.cpu_groups = result[0][5]
            result_data.mem = result[0][6]
            result_data.disk = result[0][7]
            result_data.hostname = result[0][8]
            result_data.ip = result[0][9][0]
            result_data.os = result[0][10]
            result_data.save() 
	except:
	    print "print check you asset"
	    return HttpResponse('ok')
	else:     
            data = json.dumps(result)
            return HttpResponse(data)
@login_required
def asset_delete(request,id=None):
    if request.method == 'GET':
	id = request.GET.get('id')
        ServerAsset.objects.filter(id=id).delete()
	return HttpResponseRedirect('/asset/')
@login_required
def group(request):
    all_group = Group.objects.all()
    return render_to_response("group.html",locals())
@login_required
def group_result(request):
    if request.method == 'GET':
	group = request.GET.get('g_name')
	data = Group()
	data.name = group
	data.save()
	return HttpResponse("ok")
@login_required
def group_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        Group.objects.filter(id=id).delete()
        return HttpResponseRedirect('/group/')
@login_required
def group_manage(request,id=None):
    if request.method == 'GET':
	id = request.GET.get('id')
	group_name = Group.objects.get(id=id)	
 	all_ip = group_name.hostlist_set.all()
	all_host = HostList.objects.all()	
        return render_to_response("group_manage.html",locals())
@login_required
def group_manage_delete(request,group_name=None,ip=None):
    if request.method == 'GET':
	group_name = request.GET.get('group_name')
	ip = request.GET.get('ip')
	all_group = Group.objects.filter(name=group_name)
	all_host = HostList.objects.filter(ip=ip)
	for group in all_group:
	    group_id= group.id 
	for host in all_host:
	    host_id= host.id
	h = HostList.objects.get(id=host_id)
	g = Group.objects.get(id=group_id)
	h.group.remove(g)
	return HttpResponse('ok')
@login_required
def addgroup_host(request):
    if request.method == 'GET':
	group = request.GET.get('nameInput')
	ip = request.GET.get('hostInput')
	all_group = Group.objects.filter(name=group)
        all_host = HostList.objects.filter(ip=ip)
	for group in all_group:
            group_id= group.id
        for host in all_host:
            host_id= host.id
        h = HostList.objects.get(id=host_id)
        g = Group.objects.get(id=group_id)
	h.group.add(g)
	return HttpResponse('ok')

def monitor(request):
    return render_to_response("maintenance.html",locals())

def monior_dash(request):
    total_host = HostList.objects.aggregate(Count('hostname'))
    host_num = total_host["hostname__count"]
    total_zy = HostList.objects.aggregate(Count('hostname'))
    zy_num = total_host["hostname__count"]
    total_gj = zabbix_trigle.objects.aggregate(Count('name'))
    gj_num =  total_gj["name__count"]
    jj_num = 0
    jj_num += int(zabbix_trigle.objects.filter(priority='严重').count())
    jj_num += int(zabbix_trigle.objects.filter(priority='一般严重').count())
    jj_num += int(zabbix_trigle.objects.filter(priority='错误').count())
    all_trigles = zabbix_trigle.objects.all()
    return render_to_response("monitor_dash.html",locals())

def monitor_urgent_alarm(request):
    all_trigles = zabbix_trigle.objects.all()
    all_trigles = all_trigles.exclude(priority='警告')
    all_trigles = all_trigles.exclude(priority='信息')
    all_trigles = all_trigles.exclude(priority='ok')
    return render_to_response("monitor_urgent_alarm.html",locals())

def monitor_alarm(request):
    all_trigles = zabbix_trigle.objects.all()
    return render_to_response("monitor_alarm.html",locals())

def monitor_template(request):
    all_tem = zabbix_tem_return.objects.all()
    all_host = zabbix_host_return.objects.all()
    return render_to_response("monitor_template.html",locals())

def monitor_maintenance(request):
    all_results = zabbix_maintenance.objects.all()
    all_host = zabbix_host_return.objects.filter(template="Template OS Linux")
    return render_to_response("monitor_maintenance.html",locals())

def update_bdhost(request):
    zabbix = zabbix_api()
    res = zabbix.template_get() 
    all_tem = zabbix_tem_return.objects.all()
    all_host = zabbix_host_return.objects.all()
    if res is 'ok':
        return HttpResponse('ok')
    else:
        return HttpResponse('error')
    #return render_to_response("monitor_template.html",locals())

def update_template_right(request):
    zabbix = zabbix_api()
    if request.method == 'GET':
	template = request.GET.get('template')
	nbdhost = request.GET.get('nbdhost')
        hosts = []
        for host in nbdhost.split('ISZ'):
	    print host
            if host == "Zabbix server":
                hosts.append(host)
            elif host != "" :
                value = "ISZ" + host
                hosts.append(value)
	    elif host == "":
		continue
	    else:
	        hosts.append(host)
	all_tem = zabbix_tem_return.objects.filter(template=template)
        template_id = all_tem.values()[0]['tem_id']
	hosts_id = []
	for name in hosts:
	    all_host = zabbix_host_return.objects.filter(name=name)
	    host_id = all_host.values()[0]['host_id']
	    hosts_id.append(host_id)
	    zabbix_host_return.objects.create(name=name,template=template,host_id=host_id)
	res = zabbix.template_addhost(template_id,hosts_id)
	all_host = zabbix_host_return.objects.all()	
	return render_to_response("monitor_template.html",locals())

def update_template_left(request):
   zabbix = zabbix_api() 
   if request.method == 'GET':
        template = request.GET.get('template')
        bdhost = request.GET.get('bdhost')
	hosts = []
	for host in bdhost.split('ISZ'):
	    if host == "Zabbix server":
		hosts.append(host)
	    elif host != "" :
		value = "ISZ" + host
	        hosts.append(value)
	    elif host == "":
		continue
	    else:
		hosts.append(host)
	all_tem = zabbix_tem_return.objects.filter(template=template)
        template_id = all_tem.values()[0]['tem_id']
        hosts_id = []
	u_id = ""
        for name in hosts:
            all_host = zabbix_host_return.objects.filter(name=name)
            host_id = all_host.values()[0]['host_id']
            hosts_id.append(host_id)
	    for i in zabbix_host_return.objects.filter(template=template).values():
		if i['name'] == name:
		    u_id = i['id']
	    zabbix_host_return.objects.filter(id=u_id).delete()
	res = zabbix.host_removetemplate(template_id,hosts_id)
        all_host = zabbix_host_return.objects.all()	
	return render_to_response("monitor_template.html",locals())

def addmaintenance(request):
    zabbix = zabbix_api()
    if request.method == 'GET':
        maint_name = request.GET.get('maintenance_name')
        maint_host = request.GET.get('maintenance_host')
        maint_time = request.GET.get('maintenance_time')
	main_host = json.loads(json.dumps(maint_host))
	hostid = []
	main_host =  main_host.split('[')[1].split(']')[0]
	for host in main_host.split(','):
	    hosts = host.split('"')[1]
	    hostid.append(zabbix_host_return.objects.filter(name = hosts).values()[0]['host_id'])
        zabbix.create_maintenance(maint_name, hostid, maint_time)
        res = zabbix.get_maintenance()
        all_results = zabbix_maintenance.objects.all()
        if res  is True:
            return HttpResponse('ok')
        else:
            return HttpResponse('error')

def maintenance_delete(request):
    zabbix = zabbix_api()
    if request.method == 'GET':
	main_id = request.GET.get('id')
	all_result = zabbix_maintenance.objects.filter(id=main_id)
	id = all_result.values()[0]['maintenanceid']
	response = zabbix.delete_maintenance(id)
	if response:
            all_result.delete()
            return HttpResponseRedirect('/monitor/maintenance/')
	else:
	    return HttpResponse('error')
def searchtem(request):
    if request.method == 'GET':
	data_list=[]
	host_list=[]
	hosts_list=[]
	template = request.GET.get('template')
 	all_host=zabbix_host_return.objects.filter(template=template)
	hosts = zabbix_host_return.objects.all()
	for i in all_host:
	    data_list.append(i.name)
	for i in hosts:
	    host_list.append(i.name)
	hosts_list=list(set(host_list).difference(set(data_list)))
    return HttpResponse(json.dumps({"data_list":data_list,"hosts_list":hosts_list}))	
    #print data_list
def getdata(request):
    if request.method == 'GET':
	data_list = []
	item = str(request.GET.get('item'))
	start =str(request.GET.get('from'))
	stop  = str(request.GET.get('to'))
	host = str(request.GET.get('host'))
	if item != 'None':
	    data_list = [item,start,stop,host]
	    print data_list
	    f = open("/data1/web/CMDB/app/backend/monitor_data.txt",'w')
            try:
	        for i in data_list:
                    f.write(i)
		    f.write("\n")
            finally:
                f.close()
	if item == 'None':
	    pass 
	return HttpResponse('ok')
def search(request):
    all_search = search_return.objects.all()
    return render_to_response("search.html",locals())
def startsearch(request):
    if request.method == 'GET':
	start = request.GET.get("start")
        end = request.GET.get("end")
        samples = request.GET.get("samples")
    	search=ES_SEARCH(start,end,samples)
	data=search.es_search()
	#print data
	if data is 'OK':
	    return HttpResponse('ok')
	else:
	    return HttpResponse('error')
def monitor_result(request):
    return render_to_response('monitor_result.html')
def monitor_data(request):
    data = []
    f = open("/data1/web/CMDB/app/backend/monitor_data.txt")
    try:
        lines = f.readlines()
    finally:
        f.close()
    for line in lines:
        data.append(line.strip())
    item = data[0]
    start = data[1]
    stop = data[2]
    host = data[3]
    if start == '' and stop == '':
	starttime = int(time.time())
	c.execute("SELECT `time`,`%s` FROM `statusinfo` where `hostname` = '%s' and `time` < %d" %(item,host,starttime))
	ones = [[i[0]*1000 + 28800000, i[1]] for i in c.fetchall()]
	return HttpResponse(json.dumps(ones))	
    if start == '' and stop != '':
	stop = stop.strip()
    	timeStamp = date_result(stop)
	c.execute("SELECT `time`,`%s` FROM `statusinfo` where `hostname` = '%s' and `time` < %d" %(item,host,timeStamp))
        ones = [[i[0]*1000 + 28800000, i[1]] for i in c.fetchall()]
	return HttpResponse(json.dumps(ones))
    if start != '' and stop == '':
	timeStamp=date_result(data)
	c.execute("SELECT `time`,`%s` FROM `statusinfo` where `hostname` = '%s' and `time` > %d" %(item,host,timeStamp))
	ones = [[i[0]*1000 + 28800000, i[1]] for i in c.fetchall()]
        return HttpResponse(json.dumps(ones))
    if start != '' and stop != '': 
        start_timeStamp = date_result(start) 
        stop_timeStamp = date_result(stop)
        c.execute("SELECT `time`,`%s` FROM `statusinfo` where `hostname` = '%s' and `time` > %d and `time` < %d" %(item,host,start_timeStamp,stop_timeStamp))	
	ones = [[i[0]*1000 + 28800000, i[1]] for i in c.fetchall()]
        return HttpResponse(json.dumps(ones))

@login_required
def operatelist(request):
    global work_enable
    work_enable = 1
    all_result = operate_list.objects.all()
    return render_to_response("operatelist.html",locals())

@login_required
def addoperate(request):
    all_host = HostList.objects.all()
    return render_to_response("add_operate.html",locals())

@login_required
def operateedit(request):
    if request.method == 'GET':
	id = request.GET['id']
        all_result = operate_list.objects.filter(id=id)
	all_host = HostList.objects.all()
	all_param = operate_params.objects.filter(job_id=id)
        return render_to_response("edit_operate.html",locals())

@login_required
def operate_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        operate_list.objects.filter(id=id).delete()
	all_result = operate_list.objects.all()
        return render_to_response("operatelist.html",locals())


@login_required
def operate_param_delete(request):
    if request.method == 'GET':
        id = request.GET['id']
        new_id = request.GET['newid']
        operate_params.objects.filter(id=id).delete()
        all_result = operate_list.objects.filter(id=new_id)
        all_host = HostList.objects.all()
        all_param = operate_params.objects.filter(job_name=all_result.values()[0]['name'])
	return HttpResponseRedirect("/operate/operatelist/operateedit?id={0}".format(new_id),locals()) 
        #return render_to_response("edit_operate.html",locals())


@login_required
def update_action(request):
    if request.method == 'GET':
	id = request.GET['id']
        name = request.GET['name']
        label = request.GET['label']
        kinds = request.GET['kinds']
        editor = request.GET['editor']
        action = request.GET['action']
        script = request.GET['script']
        hosts = request.GET['host']
        hosts = json.loads(json.dumps(hosts))
        hosts =  hosts.split('[')[1].split(']')[0]
        host = []
        for i in hosts.split(','):
            host.append(i.split('"')[1])
	status="可用"
	change_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        params = request.GET['params']
        params = json.loads(params)
        #var_params=list()
        for i in params:
            var_list = i['param_id']
            var_name = i['param_name']
            var_value = i['param_value']
            var_text = i['param_text']
	    try:
	        operate_id = i['operate_id']
	    except:
		print "operate id get exception"
	    else:
	    	if operate_id == "":
		    params_add = operate_params(param_id=var_list,param_name=var_name,param_value=var_value,param_text=var_text,job_id=id)
		    params_add.save()
		else:
		    all_param = operate_params.objects.filter(id=operate_id)
		    #print var_list,var_name,=var_value,var_text,name
		    try:
		        params_update = all_param.update(param_id=var_list,param_name=var_name,param_value=var_value,param_text=var_text,job_id=id)
		        params_update.save()
		    except:
			continue
			#print "param get exception"
		    else:
			continue
        try:
            action_update = operate_list.objects.filter(id=id).update(name=name,label=label,kinds=kinds,host=host,change_time=change_time,script=script,editor=editor,status=status,action=action)
            action_update.save()
        except:
	    log_update = "get exception"
            #print "get exception"
        finally:
            return HttpResponse('ok')


@login_required
def update_operate(request):
    if request.method == 'GET':
        id = request.GET['id']
        name = request.GET['name']
        label = request.GET['label']
        kinds = request.GET['kinds']
        editor = request.GET['editor']
        action = request.GET['action']
        script = request.GET['script']
        hosts = request.GET['host']
        hosts = json.loads(json.dumps(hosts))
        hosts =  hosts.split('[')[1].split(']')[0]
        host = []
        for i in hosts.split(','):
            host.append(i.split('"')[1])
        status="可用"
        change_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        params = request.GET['params']
        params = json.loads(params)
        for i in params:
            var_list = i['param_id']
            var_name = i['param_name']
            var_value = i['param_value']
            var_text = i['param_text']
            try:
                operate_id = i['operate_id']
            except:
                print "operate id get exception"
            else:
                if operate_id == "":
                    params_add = schedule_params(param_id=var_list,param_name=var_name,param_value=var_value,param_text=var_text,job_id=id)
                    params_add.save()
                else:
                    all_param = schedule_params.objects.filter(id=operate_id)
                    try:
                        params_update = all_param.update(param_id=var_list,param_name=var_name,param_value=var_value,param_text=var_text,job_id=id)
                        params_update.save()
                    except:
                        continue
                        #print "param get exception"
                    else:
                        continue

        try:
            action_update = schedule_for_operate.objects.filter(id=id).update(name=name,label=label,kinds=kinds,host=host,change_time=change_time,script=script,editor=editor,status=status,action=action)
            action_update.save()
        except:
            print "get exception"
        finally:
            return HttpResponse('ok')

@login_required
def addaction(request):
    if request.method == 'GET': 
	name = request.GET['name']
        label = request.GET['label']
        kinds = request.GET['kinds']
        editor = request.GET['editor']
        action = request.GET['action']
        script = request.GET['script']
        hosts = request.GET['host']
        hosts = json.loads(json.dumps(hosts))
        hosts =  hosts.split('[')[1].split(']')[0] 
	host = []
	for i in hosts.split(','):
            host.append(i.split('"')[1])
	#print name,label,kinds,host,editor,action
	status="可用"
	change_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        action_add = operate_list(name=name,label=label,kinds=kinds,host=host,change_time=change_time,script=script,editor=editor,status=status,action=action)
        action_add.save()

        operate_id = operate_list.objects.filter(name=name).values()[0]['id']
        params = request.GET['params']
        params = json.loads(params)
        var_params=list()
        for i in params:
            var_list = i['param_id']
            var_name = i['param_name']
            var_value = i['param_value']
            var_text = i['param_text']
            var_params.append(operate_params(param_id=var_list,param_name=var_name,param_value=var_value,param_text=var_text,job_id=operate_id))
        parama_add = operate_params.objects.bulk_create(var_params)
        return HttpResponse('ok')

@login_required
def schedule(request):
    global work_enable
    work_enable = 1
    all_result = schedule_list.objects.all()
    return render_to_response("schedule.html",locals())

@login_required
def addschedule(request):
    all_host = HostList.objects.all()
    all_result = operate_list.objects.all()
    return render_to_response("add_schedule.html",locals())

@login_required
def schedule_edit(request):
    if request.method == 'GET':
        id = request.GET['id']
        all_result = schedule_list.objects.filter(id=id)
        all_operate = operate_list.objects.all()
	all_result_operate = schedule_for_operate.objects.filter(schedule_id=id).order_by("id")
        all_host = HostList.objects.all()
        return render_to_response("edit_schedule.html",locals())

@login_required
def schedule_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        schedule_list.objects.filter(id=id).delete()
	schedule_for_operate.objects.filter(schedule_id=id).delete()
        all_result = schedule_list.objects.all()
        return render_to_response("schedule.html",locals())

@login_required
def schedule_operate_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        newid = request.GET.get('newid')
        schedule_for_operate.objects.filter(id=id).delete()
        all_result = schedule_list.objects.filter(id=newid)
	all_operate = operate_list.objects.all()
	all_result_operate = schedule_for_operate.objects.filter(schedule_id=newid)
	return HttpResponseRedirect("/operate/schedule/scheduleedit?id={0}".format(newid), locals())
        #return render_to_response("edit_schedule.html",locals())

@login_required
def schedule_operate_edit(request):
    if request.method == 'GET':
	id = request.GET['id']
	newid = request.GET['newid']
	all_result = schedule_for_operate.objects.filter(id=id)
	all_host = HostList.objects.all()
	all_param = schedule_params.objects.filter(job_id=id)
	return render_to_response("edit_schedule_operate.html",locals())


@login_required
def update_schedule(request):
    if request.method == 'GET':
        id = request.GET['id']
        name = request.GET['name']
        code = request.GET['code']
        kinds = request.GET['kinds']
        editor = request.GET['editor']
        user = request.GET['user']
	change_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        jobs = request.GET['jobs']
        jobs = json.loads(jobs)
        job_id=[]
        for i in jobs:
            job_id.append(i['job_id'])
	try:
            schedule_update = schedule_list.objects.filter(id=id).update(name=name,code=code,fun=kinds,user=user,editor=editor,action_name=job_id,count_job=len(jobs),change_time=change_time)
            schedule_update.save()
        except:
            log_schedule =  "schedule get exception"
        finally:
	    for i in jobs:
                job_id = i['job_id']
                list_id = i['list_id']
                job_name = i['job_name']
		try:
               	    operate_id = i['operate_id']
		except:
		    print "operate id get exception"
		else:
		    if operate_id == "":
		        all_result = operate_list.objects.filter(name=job_id)
                        label = all_result.values()[0]['label']
                        kinds = all_result.values()[0]['kinds']
                        host = all_result.values()[0]['host']
                        editor = all_result.values()[0]['editor']
                        script = all_result.values()[0]['script']
                        action = all_result.values()[0]['action']
                        change_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                        status = all_result.values()[0]['status']
                        schedule_for_operate_add = schedule_for_operate(name=job_id,list_id=list_id,job_name=job_name,label=label,kinds=kinds,host=host,change_time=change_time,script=script,editor=editor,status=status,action=action,schedule_id=id)
                        schedule_for_operate_add.save()
			var_params=add_param(id,list_id)
		    else:
                        all_result = schedule_for_operate.objects.filter(id=operate_id)
		        try:
                            schedule_for_operate_update = schedule_for_operate.objects.filter(id=operate_id).update(name=job_id,list_id=list_id,job_name=job_name)
                            schedule_for_operate_update.save()
                        except:
                            log_schedule_operate = "get exception"
                        else:
                            continue
            return HttpResponse('ok')

def add_param(schedule_id,list_id):
    var_params = list()
    schedule_results = schedule_for_operate.objects.filter(schedule_id=schedule_id)
    for schedule_result in schedule_results.values():
        if list_id == schedule_result['list_id']:
            operate_id=schedule_result['id']
            operate_name=schedule_result['name']
    job_id = operate_list.objects.filter(name=operate_name).values()[0]['id']
    params_result = operate_params.objects.filter(job_id=job_id)
    for j in operate_params.objects.filter(job_id=job_id).values():
        param_id = j['param_id']
        param_name = j['param_name']
        param_value = j['param_value']
        param_text = j['param_text']
    	var_params.append(schedule_params(param_id=param_id,param_name=param_name,param_value=param_value,param_text=param_text,job_id=operate_id))
    param_add = schedule_params.objects.bulk_create(var_params)
    return var_params

@login_required
def addfun(request):
   if request.method == 'GET':
        name = request.GET['name']
        code = request.GET['code']
        kinds = request.GET['kinds']
        editor = request.GET['editor']
        user = request.GET['user']
        jobs = request.GET['jobs']
	jobs = json.loads(jobs)
	job_id=[]
	for i in jobs:
	    job_id.append(i['job_id'])
	change_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	try:
	    schedule_add = schedule_list(name=name,code=code,fun=kinds,user=user,editor=editor,action_name=job_id,count_job=len(jobs),change_time=change_time)
	    schedule_add.save()
        except:
            print "get exception"
        finally:
            all_result = schedule_list.objects.filter(name=name)
            schedule_id = all_result.values()[0]['id']
	    for i in jobs:
		job_id = i['job_id'] 
		list_id = i['list_id'] 
		job_name = i['job_name'] 
		all_result = operate_list.objects.filter(name=job_id)
		print job_id
		#all_result.values()[0]
		label = all_result.values()[0]['label']
		kinds = all_result.values()[0]['kinds']
	        host = all_result.values()[0]['host']
		editor = all_result.values()[0]['editor']
		script = all_result.values()[0]['script']
		action = all_result.values()[0]['action']
		change_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		status = all_result.values()[0]['status']
		
		try:
		    schedule_for_operate_add = schedule_for_operate(name=job_id,list_id=list_id,job_name=job_name,label=label,kinds=kinds,host=host,change_time=change_time,script=script,editor=editor,status=status,action=action,schedule_id=schedule_id) 
		    schedule_for_operate_add.save()
		except:
		    print "get exception"
		else:
		    var_params = add_param(schedule_id,list_id)
		    #print var_params
	    return HttpResponse('ok')
      

@login_required
def work(request):
    all_result = running_list.objects.all()
    return render_to_response("work.html", locals())

@login_required
def work_operate(request):
    import datetime
    global work_enable
    if request.method == 'GET':
        id = request.GET['id']
        all_result = operate_list.objects.filter(id=id)
        all_work = all_result.values()[0]
	all_param = operate_params.objects.filter(job_id=id).values()
        work_id = work_running.delay(all_work['name'], all_work['host'], all_work['script'], all_work['action'],
                                      all_work['editor'],all_param)
    return HttpResponseRedirect("/operate/work", locals())

@login_required
def work_operate_result(request):
    if request.method == 'GET':
	id = request.GET['id']
	all_result = running_list.objects.filter(id=id)
	if all_result.values()[0]['action'] == 'operate':
	    work_id = 1
	    jobname = all_result.values()[0]['name'] 
	    op_name = jobname.split('_')[0]
	    all_job = operate_list.objects.filter(name = op_name)
	else:
	    work_id =  all_result.values()[0]['id']
	    jobname = all_result.values()[0]['name']  
    return render_to_response("operate_work.html",locals())

@login_required
def work_schedule_operate(request):
    if request.method == 'GET':
        id = request.GET['id']
    	all_result = schedule_running_list.objects.filter(id=id)
	jobname = all_result.values()[0]['name']
	schedule_name = all_result.values()[0]['scheduleName']
	schedule_id = running_list.objects.filter(name=schedule_name).values()[0]['jid']
	#schedule_id = all_result.values()[0]['jid']
	#all_job = schedule_for_operate.objects.filter(schedule_id = schedule_id)[:1]
	jobname = jobname.split('_')[0]
	all_job = schedule_for_operate.objects.filter(schedule_id = schedule_id)
	all_job = all_job.filter(name=jobname)[:1]
	return render_to_response("schedule_operate_work.html",locals())

@login_required
def work_schedule(request):
    global work_enable
    if work_enable == 1:
    #if request.method == 'GET':
        id = request.GET['id']
        all_result = schedule_list.objects.filter(id=id)
        all_schedule = all_result.values()[0]
        all_results =  schedule_for_operate.objects.filter(schedule_id=id)
        try:
            schedule_running.delay(all_schedule['name'],all_schedule['user'],all_schedule['fun'],all_schedule['action_name'],id,all_results.values())
	    work_enable = 0
        except:
            print "编排失败"
        else:
	    return HttpResponseRedirect("/operate/work",locals())
		
@login_required
def work_result(request):
    if request.method == 'GET':
	id = request.GET['id']
	all_result = running_list.objects.filter(id=id)
	schedulename = all_result.values()[0]['name'].split('_')[0]
	all_schedule = schedule_list.objects.filter(name = schedulename)
	schedule_id = all_schedule.values()[0]['id']
	all_job = schedule_for_operate.objects.filter(schedule_id =schedule_id)
	all_job_result = schedule_running_list.objects.filter(scheduleName = all_result.values()[0]['name'])
	schedulename = all_result.values()[0]['name']
	return render_to_response("schedule_work.html",locals())

def select_params(schedule_id):
    job_id = schedule_for_operate.objects.filter(schedule_id=schedule_id).values()[0]['id']
    params_result = schedule_params.objects.filter(job_id=job_id).values()
    return params_result
