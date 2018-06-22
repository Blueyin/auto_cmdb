from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
from app.views import *

urlpatterns = patterns('',
		       # Examples:
		       # url(r'^$', 'CMDB.views.home', name='home'),
		       # url(r'^CMDB/', include('CMDB.foo.urls')),

		       # Uncomment the admin/doc line below to enable admin documentation:
		       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

		       # Uncomment the next line to enable the admin:
		       url(r'^admin/', include(admin.site.urls)),
		       (r'^index/$', index),
		       (r'^$', login),
		       (r'^login/$', login),
		       (r'^authin/$', authin),
		       (r'^loginout/$', loginout),
		       (r'accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
		       (r'^pc/idc/$', idc),
		       (r'^pc/addidc/$', addidc),
		       (r'^pc/idc/idc_delete/$', idc_delete),
		       (r'^pc/check_host/$', idc_manage),
		       (r'^key_result/$', key_result),
		       (r'^pc/mac/$', mac),
		       (r'^pc/addmac/$', addmac),
		       (r'^pc/mac/mac_delete/$', mac_delete),
		       (r'^pc/mac/mac_edit/$', mac_edit),
		       (r'^pc/macresult/$', macresult),
		       (r'^pc/operation_control/$', operation_control),
		       (r'^pc/group/$', group),
		       (r'^pc/group_result/$', group_result),
		       (r'^pc/group/group_delete/$', group_delete),
		       (r'^pc/group_manage/$', group_manage),
		       (r'^pc/group_manage/group_manage_delete/$', group_manage_delete),
		       (r'^pc/addgroup_host/$', addgroup_host),
		       (r'^pc/asset/$', asset),
		       (r'^pc/asset_auto/$', asset_auto),
		       (r'^pc/asset_auto_result/$', asset_auto_result),
		       (r'^pc/asset/asset_delete/$', asset_delete),

		       (r'^users/author/$', author),
		       (r'^users/addauthor/$', addauthor),
		       (r'^users/upauthor/$', upauthor),
		       (r'^users/author/author_delete/$', author_delete),
		       (r'^users/author/author_edit/$', author_edit),
		       (r'^users/author_result/$', author_result),

		       (r'^author/$', author),
		       (r'^addauthor/$', addauthor),
		       (r'^upauthor/$', upauthor),
		       (r'^author/author_delete/$', author_delete),
		       (r'^author/author_edit/$', author_edit),
		       (r'^author_result/$', author_result),

		       (r'^operate/command/$', command),
		       (r'^operate/command_group/$', command_group),
		       (r'^operate/command_group/check_result/$', check_result),
		       (r'^operate/command_group_result/$', command_group_result),
		       (r'^operate/command_result/$', command_result),
		       (r'^operate/file/$', file),
		       (r'^operate/file_result/$', file_result),
		       (r'^operate/operatelist/$', operatelist),
		       (r'^operate/addoperate/$', addoperate),
		       (r'^operate/operatelist/operateedit$', operateedit),
		       (r'^operate/operatelist/operate_del$', operate_delete),
		       (r'^operate/operateedit/param_del$', operate_param_delete),
		       (r'^operate/addoperate/add_action/$', addaction),
		       (r'^operate/operatelist/update_action$', update_action),
		       (r'^operate/schedule/$', schedule),
		       (r'^operate/addschedule/$', addschedule),
		       (r'^operate/schedule/scheduleedit/operate_edit$', schedule_operate_edit),
		       (r'^operate/addschedule/addfun$', addfun),
		       (r'^operate/schedule/scheduleedit$', schedule_edit),
		       (r'^operate/schedule/schedule_del$', schedule_delete),
		       (r'^operate/schedule/scheduleedit/operate_del$', schedule_operate_delete),
		       (r'^operate/schedule/update_schedule$', update_schedule),
		       (r'^operate/schedule/scheduleedit/update_operate$', update_operate),
		       (r'^operate/work/$', work),
		       (r'^operate/work/workoperate/$', work_operate),
		       (r'^operate/work/workeoperateresult/$', work_operate_result),
		       (r'^operate/work/workscheduleoperate/$', work_schedule_operate),
		       (r'^operate/work/workschedule/$', work_schedule),
		       (r'^operate/work/workresult/$', work_result),

		       (r'^soccer/$', soccer),

		       (r'^job/$', job),
		       (r'^job/bd_jenkins/$', bd_jenkins),
		       (r'^job/update_job/$', update_job),
		       (r'^job/job_history/$', job_history),
		       (r'^job/job_release/$', job_release),
		       (r'^job/job_history_result/$', job_history_result),
		       (r'^job/job_release_result/$', job_release_result),

		       (r'^monitor/$', monitor),
		       (r'^monitor/dash/$', monior_dash),
		       (r'^monitor/dash/urgent_alarm$', monitor_urgent_alarm),
		       (r'^monitor/dash/alarm$', monitor_alarm),
		       (r'^monitor/template/$', monitor_template),
		       (r'^monitor/template/searchtem/$', searchtem),
		       (r'^monitor/template/updatehost/$', update_bdhost),
		       (r'^monitor/template/updatetemplate_right$', update_template_right),
		       (r'^monitor/template/updatetemplate_left$', update_template_left),
		       (r'^monitor/maintenance/$', monitor_maintenance),
		       (r'^monitor/maintenance/addmaintenance/$', addmaintenance),
		       (r'^monitor/maintenance/maintenance_delete/$', maintenance_delete),
		       (r'^data/$', getdata),
		       (r'monitor_result/$', monitor_result),

		       (r'^search/$', search),
		       (r'^startsearch/$', startsearch),



		       )
