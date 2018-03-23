# coding: utf-8
from django.db import models
from django.contrib import admin
# Create your models here.
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import *
import time


class Idc(models.Model):
    idc_name = models.CharField(max_length=40, verbose_name=u'机房名称')
    remark = models.CharField(max_length=40, verbose_name=u'备注')

    def __unicode__(self):
	return self.idc_name

    class Meta:
	verbose_name = u'机房列表'
	verbose_name_plural = u'机房列表'


class HostList(models.Model):
    ip = models.GenericIPAddressField(unique=True, verbose_name=u'IP地址')
    hostname = models.CharField(max_length=60, verbose_name=u'主机名')
    group = models.ManyToManyField('Group', null=True, blank=True, verbose_name=u'组名')
    application = models.CharField(max_length=20, verbose_name=u'应用')
    bianhao = models.CharField(max_length=30, verbose_name=u'编号')
    idc_name = models.CharField(max_length=40, null=True, blank=True, verbose_name=u'所属机房')

    def __unicode__(self):
	return self.ip

    class Meta:
	verbose_name = u'主机列表'
	verbose_name_plural = u'主机列表'


class ServerAsset(models.Model):
    manufacturer = models.CharField(max_length=20, verbose_name=u'厂商')
    productname = models.CharField(max_length=30, verbose_name=u'产品型号')
    service_tag = models.CharField(max_length=80, unique=True, verbose_name=u'序列号')
    cpu_model = models.CharField(max_length=50, verbose_name=u'CPU型号')
    cpu_nums = models.PositiveSmallIntegerField(verbose_name=u'CPU线程数')
    cpu_groups = models.PositiveSmallIntegerField(verbose_name=u'CPU物理核数')
    mem = models.CharField(max_length=100, verbose_name=u'内存大小')
    disk = models.CharField(max_length=300, verbose_name=u'硬盘大小')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    ip = models.CharField(max_length=20, verbose_name=u'IP地址')
    os = models.CharField(max_length=20, verbose_name=u'操作系统')

    def __unicode__(self):
	return u'%s - %s' % (self.ip, self.hostname)

    class Meta:
	verbose_name = u'主机资产信息'
	verbose_name_plural = u'主机资产信息管理'


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
	return self.name

    class Meta:
	verbose_name = u'主机组信息'
	verbose_name_plural = u'主机组信息管理'


class Upload(models.Model):
    headImg = models.FileField(upload_to='./upload/')

    def __unicode__(self):
	return unicode(self.headImg) or u''

    class Meta:
	verbose_name = u'文件上传'
	verbose_name_plural = u'文件上传'


class cmd_run(models.Model):
    # ip = GenericGenericIPAddressField(verbose_name=u'IP地址')
    ip = models.GenericIPAddressField(verbose_name=u'IP地址')
    command = models.CharField(max_length=30, verbose_name=u'命令')
    track_mark = models.IntegerField()

    def __unicode__(self):
	return self.ip

    class Meta:
	verbose_name = u'命令管理'
	verbose_name_plural = u'命令管理'


class salt_return(models.Model):
    fun = models.CharField(max_length=50)
    jid = models.CharField(max_length=255)
    result = models.TextField()
    host = models.GenericIPAddressField(max_length=255)
    success = models.CharField(max_length=10)
    full_ret = models.TextField()

    def __unicode__(self):
	return self.host

    class Meta:
	verbose_name = u'命令返回结果'
	verbose_name_plural = u'命令返回结果'


class Author(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'姓名')
    user = models.CharField(max_length=50, verbose_name=u'用户')
    passwd = models.CharField(max_length=50, verbose_name=u'密码')
    key = models.CharField(max_length=20, verbose_name=u'KEY')
    group = models.CharField(max_length=50, verbose_name=u'组名')

    def __unicode__(self):
	return self.user

    class Meta:
	verbose_name = u'用户'
	verbose_name_plural = u'权限管理'


class search_return(models.Model):
    logstash_checksum = models.CharField(max_length=50, verbose_name=u'项目')
    samples = models.CharField(max_length=1024, verbose_name=u'语句')
    query_time_avg = models.CharField(max_length=50, verbose_name=u'平均')
    query_time_sum = models.CharField(max_length=50, verbose_name=u'综合')
    cnt_sum = models.CharField(max_length=50, verbose_name=u'总次数')

    def __unicode__(self):
	return self.logstash_checksum

    class Meta:
	verbose_name = u'项目'


class zabbix_tem_return(models.Model):
    tem_id = models.CharField(max_length=50, verbose_name=u'ID')
    template = models.CharField(max_length=50, verbose_name=u'模板')

    def __unicode__(self):
	return self.tem_id

    class Meta:
	verbose_name = u'ID'


class zabbix_host_return(models.Model):
    template = models.CharField(max_length=50, verbose_name=u'模板')
    name = models.CharField(max_length=50, verbose_name=u'主机')
    host_id = models.CharField(max_length=50, verbose_name=u'主机ID')

    def __unicode__(self):
	return self.host_id

    class Meta:
	verbose_name = u'ID'


class jenkins_return(models.Model):
    job_name = models.CharField(max_length=100, verbose_name=u'项目名称')
    job_date = models.CharField(max_length=50, verbose_name=u'发布时间 ')
    job_id = models.CharField(max_length=50, verbose_name=u'版本')
    job_url = models.CharField(max_length=1024, verbose_name=u'地址')
    job_status = models.CharField(max_length=100, verbose_name=u'状态')
    full_name = models.CharField(max_length=100, verbose_name=u'全名')

    def __unicode__(self):
	return self.job_name

    class Meta:
	verbose_name = u'项目名称'


class job_history_return(models.Model):
    job_name = models.CharField(max_length=100, verbose_name=u'项目名称')
    job_host = models.CharField(max_length=100, verbose_name=u'项目发布主机 ')
    job_work = models.CharField(max_length=100, verbose_name=u'工作路径')
    job_bigtime = models.CharField(max_length=1024, verbose_name=u'验证包时间')
    job_endtime = models.CharField(max_length=100, verbose_name=u'包安装时间')
    job_index = models.CharField(max_length=100, verbose_name=u'发布版本')
    pc_index = models.CharField(max_length=100, verbose_name=u'服务器版本')
    job_history = models.TextField(max_length=65535, verbose_name=u'返回信息')

    def __unicode__(self):
	return self.job_name

    class Meta:
	verbose_name = u'项目名称'


class job_release_return(models.Model):
    job_name = models.CharField(max_length=100, verbose_name=u'项目名称')
    job_host = models.CharField(max_length=100, verbose_name=u'项目发布主机 ')
    job_work = models.CharField(max_length=100, verbose_name=u'工作路径')
    job_starttime = models.CharField(max_length=1024, verbose_name=u'开始时间')
    job_endtime = models.CharField(max_length=100, verbose_name=u'结束时间')
    job_index = models.CharField(max_length=100, verbose_name=u'发布版本')
    pc_index = models.CharField(max_length=100, verbose_name=u'服务器版本')
    job_status = models.CharField(max_length=100, verbose_name=u'执行状态')
    job_history = models.TextField(max_length=65535, verbose_name=u'返回信息')
    result_log = models.CharField(max_length=1024, verbose_name=u'执行日志')

    def __unicode__(self):
	return self.job_name

    class Meta:
	verbose_name = u'项目名称'


class zabbix_maintenance(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'维护名称')
    host = models.GenericIPAddressField(max_length=1024, verbose_name=u'维护主机')
    maintenanceid = models.CharField(max_length=100, verbose_name=u'维护ID')
    active_since = models.CharField(max_length=100, verbose_name=u'屏蔽开始时间')
    active_till = models.CharField(max_length=100, verbose_name=u'屏蔽结束时间')

    def __unicode__(self):
	return self.name

    class Meta:
	verbose_name = u'维护名称'


class zabbix_trigle(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'资源名称')
    host = models.GenericIPAddressField(max_length=100, verbose_name=u'维护主机')
    description = models.CharField(max_length=1024, verbose_name=u'事件描述')
    priority = models.CharField(max_length=100, verbose_name=u'告警级别')
    lasttime = models.CharField(max_length=100, verbose_name=u'发生时间')

    def __unicode__(self):
	return self.name

    class Meta:
	verbose_name = u'维护名称'


class operate_list(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'操作名称')
    label = models.CharField(max_length=100, verbose_name=u'标签')
    kinds = models.CharField(max_length=100, verbose_name=u'所属分类')
    host = models.GenericIPAddressField(max_length=100, verbose_name=u'执行主机')
    editor = models.TextField(verbose_name=u'脚本内容')
    script = models.CharField(max_length=20, verbose_name=u'脚本语言')
    action = models.CharField(max_length=100, verbose_name=u'执行命令')
    change_time = models.CharField(max_length=100, verbose_name=u'修改时间')
    status = models.CharField(max_length=100, verbose_name=u'状态')

    def __unicode__(self):
	return self.name

    class Meta:
	verbose_name = u'操作名称'


class operate_params(models.Model):
    param_id = models.CharField(max_length=100, verbose_name=u'操作ID')
    param_name = models.CharField(max_length=100, verbose_name=u'参数名')
    param_value = models.CharField(max_length=100, verbose_name=u'参数值')
    param_text = models.CharField(max_length=100, verbose_name=u'参数描述 ')
    job_id = models.CharField(max_length=100, verbose_name=u'操作id')

    def __unicode__(self):
	return self.job_id

    class Meta:
	verbose_name = u'操作名称'


class schedule_params(models.Model):
    param_id = models.CharField(max_length=100, verbose_name=u'操作ID')
    param_name = models.CharField(max_length=100, verbose_name=u'参数名')
    param_value = models.CharField(max_length=100, verbose_name=u'参数值')
    param_text = models.CharField(max_length=100, verbose_name=u'参数描述 ')
    job_id = models.CharField(max_length=100, verbose_name=u'操作id')

    def __unicode__(self):
	return self.job_id

    class Meta:
	verbose_name = u'操作id'


class schedule_list(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'编排名称')
    code = models.CharField(max_length=100, verbose_name=u'编排编码')
    fun = models.CharField(max_length=100, verbose_name=u'执行类型')
    user = models.CharField(max_length=100, verbose_name=u'执行人')
    editor = models.CharField(max_length=4096, verbose_name=u'编排描述')
    action_name = models.CharField(max_length=4096, verbose_name=u'操作名称')
    count_job = models.CharField(max_length=20, verbose_name=u'任务数')
    change_time = models.CharField(max_length=100, verbose_name=u'修改时间')

    # schedule_id = models.CharField(max_length=100, verbose_name=u'编排ID')
    def __unicode__(self):
	return self.name

    class Meta:
	verbose_name = u'编排名称'


class schedule_for_operate(models.Model):
    schedule_id = models.CharField(max_length=100, verbose_name=u'编排ID')
    list_id = models.CharField(max_length=100, verbose_name=u'序列ID')
    name = models.CharField(max_length=100, verbose_name=u'操作名称')
    job_name = models.CharField(max_length=100, verbose_name=u'任务名称')
    label = models.CharField(max_length=100, verbose_name=u'标签')
    kinds = models.CharField(max_length=100, verbose_name=u'所属分类')
    host = models.GenericIPAddressField(max_length=100, verbose_name=u'执行主机')
    editor = models.TextField(verbose_name=u'脚本内容')
    script = models.CharField(max_length=20, verbose_name=u'脚本语言')
    action = models.CharField(max_length=100, verbose_name=u'执行命令')
    change_time = models.CharField(max_length=100, verbose_name=u'修改时间')
    status = models.CharField(max_length=100, verbose_name=u'状态')

    def __unicode__(self):
	return self.schedule_id

    class Meta:
	verbose_name = u'编排ID'


class running_list(models.Model):
    name = models.CharField(max_length=1024, verbose_name=u'作业名称')
    user = models.CharField(max_length=1024, verbose_name=u'执行人')
    fun = models.CharField(max_length=1024, verbose_name=u'执行类型')
    start_time = models.CharField(max_length=4096, verbose_name=u'开始时间')
    end_time = models.CharField(max_length=4096, verbose_name=u'结束时间')
    sum_time = models.CharField(max_length=4096, verbose_name=u'总耗时')
    status = models.CharField(max_length=1024, verbose_name=u'执行状态')
    jid = models.CharField(max_length=4096, verbose_name=u'作业ID')
    action = models.CharField(max_length=100, verbose_name=u'作业或编排')
    command = models.CharField(max_length=100, verbose_name=u'执行命令')
    result = models.TextField(verbose_name=u'返回日志')

    def __unicode__(self):
	return self.name

    class Meta:
	verbose_name = u'作业名称'


class schedule_running_list(models.Model):
    list_id = models.CharField(max_length=100, verbose_name=u'序列ID')
    scheduleName = models.CharField(max_length=100, verbose_name=u'编排名称')
    name = models.CharField(max_length=1024, verbose_name=u'作业名称')
    user = models.CharField(max_length=1024, verbose_name=u'执行人')
    fun = models.CharField(max_length=1024, verbose_name=u'执行类型')
    start_time = models.CharField(max_length=4096, verbose_name=u'开始时间')
    end_time = models.CharField(max_length=4096, verbose_name=u'结束时间')
    sum_time = models.CharField(max_length=4096, verbose_name=u'总耗时')
    status = models.CharField(max_length=1024, verbose_name=u'执行状态')
    jid = models.CharField(max_length=4096, verbose_name=u'作业ID')
    action = models.CharField(max_length=100, verbose_name=u'作业或编排')
    command = models.CharField(max_length=100, verbose_name=u'执行命令')
    result = models.TextField(verbose_name=u'返回日志')

    def __unicode__(self):
	return self.name

    class Meta:
	verbose_name = u'作业名称'
