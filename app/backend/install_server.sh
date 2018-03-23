#!/bin/bash
####yum install salt-master #####
sudo yum install https://repo.saltstack.com/yum/redhat/salt-repo-latest-2.el7.noarch.rpm
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
yum -y install pip
pip install 'django==1.8.1'
pip install south
pip install MySQL-python
pip install django-celery
pip install celery
pip install jenkins

~