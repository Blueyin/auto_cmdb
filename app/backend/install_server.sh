#!/bin/bash
####yum install salt-master #####
sudo yum -y install https://repo.saltstack.com/yum/redhat/salt-repo-latest-2.el7.noarch.rpm
yum install salt-master -y
#####change config####
cp -rf /auto_cmdb/app/backend/master /etc/salt/master
#####start master####
sudo yum install salt-master

####install setuptools####
wget https://pypi.python.org/packages/6f/10/5398a054e63ce97921913052fde13ebf332a3a4104c50c4d7be9c465930e/setuptools-26.1.1.zip#md5=f81d3cc109b57b715d46d971737336db
unzip setuptools-26.1.1.zip
cd setuptools-26.1.1
python setup.py install

####install pip#####
cd /data/
wget "https://pypi.python.org/packages/source/p/pip/pip-1.5.4.tar.gz#md5=834b2904f92d46aaa333267fb1c922bb" --no-check-certificate
tar -xzvf pip-1.5.4.tar.gz
cd pip-1.5.4
python setup.py install

#####安装pip插件
pip install 'django==1.8.1'
pip install south
pip install MySQL-python
pip install django-celery
pip install celery
pip install jenkins

