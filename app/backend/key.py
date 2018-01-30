#!/usr/bin/python
#encoding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import salt.client,commands
local = salt.client.LocalClient()

# ywuser
ywuser=['master']

def chuser(user):
    newuser=''
    for i in user:
        if i == "'":
            continue
        elif i != ",":
            newuser = newuser+i
        else:
            newuser = newuser+' '
    return newuser
def replace(dev,user):
    if dev == 'dev':
        file1 = '/data1/web/CMDB/user/devadd.sls'
        file2 = '/data1/web/CMDB/user/devdel.sls'
        old = commands.getoutput("cat /data1/web/CMDB/user/devadd.sls|grep set|awk -F '[' {'print $2'}|awk -F ']' {'print $1'}")
    elif dev == 'yw':
        file1 = '/data1/web/CMDB/user/ywadd.sls'
        file2 = '/data1/web/CMDB/user/ywdel.sls'
        old = commands.getoutput("cat /data1/web/CMDB/user/ywadd.sls|grep set|awk -F '[' {'print $2'}|awk -F ']' {'print $1'}")
    else:
        file1 = '/data1/web/CMDB/user/bigdataadd.sls'
        file2 = '/data1/web/CMDB/user/bigdatadel.sls'
        old = commands.getoutput("cat /data1/web/CMDB/user/bigdataadd.sls|grep set|awk -F '[' {'print $2'}|awk -F ']' {'print $1'}")
    new=user
    print old,new
    new="'{0}'".format(new)
    commands.getoutput('sed -i "s/{0}/{1}/" {2}'.format(old,new,file1))
    commands.getoutput('sed -i "s/{0}/{1}/" {2}'.format(old,new,file2))
    pc='192.168.0.8'
    local.cmd(pc, 'cmd.run', ['sed -i "s/{0}/{1}/" {2}'.format(old,new,file1)])
    local.cmd(pc, 'cmd.run', ['sed -i "s/{0}/{1}/" {2}'.format(old,new,file2)])
    return True

def ywadd(user,pc,dev):
    try:
	replace(dev,user)
	pc = pc2pcs(pc)
	n = 0
        local.cmd(pc, 'state.sls', ['user.ywdel'],'','pcre')
        local.cmd(pc, 'state.sls', ['user.ywadd'],'','pcre')
        user = chuser(user)
        local.cmd(pc, 'cmd.run', ['bash /tmp/user/add_key.sh "{0}"'.format(user)],'','pcre')
        if user == "chenyin" or user == "yuxiaomeng" or user == "wangmingbo" or user == "shiyichao":
	    n = 1
	else:
            local.cmd(pc, 'cmd.run', ["sed -i 's/User_Alias ADMIN = yanfei, chenkeke, yuxiaomeng, chenyin, shiyichao, wangmingbo, jenkins/User_Alias ADMIN = yanfei, chenkeke, yuxiaomeng, chenyin, shiyichao, wangmingbo, jenkins, {0}/g' /etc/sudoers".format(user)],'','pcre')
    except:
        print 'add {0} faild!'.format(user)
    else:
        return 'add {0} success!'.format(user)

def add(user,pc,dev):
    try:
	replace(dev,user)
	pc = pc2pcs(pc)
        local.cmd(pc, 'state.sls', ['user.devdel'],'','pcre')
        local.cmd(pc, 'state.sls', ['user.devadd'],'','pcre')
        user = chuser(user)
        local.cmd(pc, 'cmd.run', ['bash /tmp/user/add_key.sh "{0}"'.format(user)],'','pcre')
    except:
        print 'add {0} faild!'.format(user)
    else:
        return 'add {0} success!'.format(user)

def bigdata(user,pc,dev):
    try:
	replace(dev,user)
	pc = pc2pcs(pc)
        local.cmd(pc, 'state.sls', ['user.bigdatadel'],'','pcre')
        local.cmd(pc, 'state.sls', ['user.bigdataadd'],'','pcre')
        user = chuser(user)
        local.cmd(pc, 'cmd.run', ['bash /tmp/user/addbig_key.sh "{0}"'.format(user)],'','pcre')
    except:
        print 'add {0} faild!'.format(user)
    else:
        return 'add {0} success!'.format(user)

def devdel(user,dev):
    try:
        replace(dev,user)
	pc = "192.168.0.12"
	local.cmd(pc, 'state.sls', ['user.devdel'],'','pcre')
    except:
	print "del {0} failed!".format(user)
    else:
	return 'del {0} success!'.format(user)

def bigdatadel(user,bigdata):
    try:
        replace(bigdata,user)
        pc = "192.168.0.9|192.168.0.10|192.168.0.11"
        local.cmd(pc, 'state.sls', ['user.bigdatadel'],'','pcre')
    except:
        print "del {0} failed!".format(user)
    else:
        return 'del {0} success!'.format(user)

def pc2pcs(pc):
    pcs =""
    for i in range(len(pc)):
        if len(pc) == 1:
            pcs = pc[0]
        else:
            if pc[-1] == pc[i]:
                pcs += pc[i]
            else:
                pcs = pcs + pc[i] + '|'
    return pcs
def cp(pc):
    try:
	pcs = pc2pcs(pc)
        local.cmd(pcs, 'cp.get_file', ['salt://admin/user.tar.gz', {'dest': '/tmp/user.tar.gz', '__kwarg__': True}],'','pcre')
        local.cmd(pcs, 'archive.tar', ['zxvf', '/tmp/user.tar.gz', {'dest': '/tmp/', '__kwarg__': True}],'','pcre')
    except:
        print "failed"
    else:
        return True

if __name__=='__main__':
    try:
        pc = sys.argv[1]
        user = sys.argv[2]
        dev = sys.argv[3]
    except:
        print u"请输入指定服务器，用户，所属组！"
    else:
        cp(pc)
        if dev == 'yw':
            print ywadd(user, pc, dev)
        elif dev =='dev':
            print add(user, pc, dev)
        else:
            print bigdata(user,pc,dev)
