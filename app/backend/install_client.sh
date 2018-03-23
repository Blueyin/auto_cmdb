#!/bin/bash
####install #####
sudo yum install https://repo.saltstack.com/yum/redhat/salt-repo-latest-2.el7.noarch.rpm
yum install salt-minion -y
####change master ###
sed -i "s/#id:/id: $1/g" /etc/salt/minion
sed -i "s/#master: salt/master: $2/g" /etc/salt/minion
####start client####
sudo systemctl restart salt-minion