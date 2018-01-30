# -*- coding: utf-8 -*-
from saltapi import SaltAPI
import threading
import ConfigParser
asset_info = []
def get_server_asset_info(tgt,url,user,passwd,device):
    '''
    Salt API得到资产信息，进行格式化输出
    '''
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    global asset_info 
    info = []
    sapi = SaltAPI(url=url,username=user,password=passwd)
    ret = sapi.remote_noarg_execution(tgt,'grains.items')
    #manufacturer = ret['manufacturer']
    #info.append(manufacturer)
    info.append('111')
    #productname = ret['productname']
    #info.append(productname)  
    info.append('222')  
    #serialnumber = ret['serialnumber']
    #info.append(serialnumber)
    #info.append('333')
    serialnumber = ret['server_id']
    info.append(serialnumber)
    cpu_model = ret['cpu_model']
    info.append(cpu_model)
    num_cpus = int(ret['num_cpus'])
    info.append(num_cpus)
    num_gpus = int(ret['num_gpus'])
    info.append(num_gpus)
    mem_total = ret['mem']
    info.append(mem_total)
    disk  = ret['disk']
    info.append(disk)
    id = ret['id']
    info.append(id)
    lan_ip = ret['ip4_interfaces'][device]
    info.append(lan_ip)
    sys_ver = ret['os'] + ret['osrelease'] + '-' + ret['osarch']
    info.append(sys_ver)
    asset_info = []
    asset_info.append(info)
    return asset_info
if __name__ == '__main__':
    print get_server_asset_info('192.168.0.195','https://192.168.0.194:8888','blue','blue1234','eth1')
