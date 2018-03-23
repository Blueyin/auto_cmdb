**运维平台搭建过程**
___

**https://www.jianshu.com/p/26624ca55212**

**开发环境**

    centos 7.4 django 1.8.18 python 2.7.5 Mysql 5.6
    
######此版本基于linuxhub/lmanager的基础上做的开发

    运维平台基于saltstack的接口调用来实现，操作管理，用户管理，权限管理，jenkins代码发布，作业管理，任务编排等系统，有监控管理系统，监控告警，模板管理和维护周期。
    
    安装步骤（基本环境，需要安装好（Django、South、MySQLdb、Celery、Jenkins模块）安装过程报错就继续安装模块即可）：

    Mysql这边自己装一下，可以参考https://segmentfault.com/a/1190000005066501
 
    pip install 'django==1.8.1'
    
    pip install south
    
    pip install MySQL-python
    
    pip install django-celery
    
    pip install celery
    
    pip install python-jenkins

**1、在服务端data目录。把项目拷贝到当前目录下，命名auto-cmdb。**

**2、在服务起端执行脚本:(在/auto_cmdb/app/backend目录存放)**

    install_server.sh
    
**3、在cp 客户端脚本到client执行，注意执行格式：**

    bash -x install_client.sh 127.0.0.1 127.0.0.1     
    
    client表示客户端主机ID，建议跟主机的Hostname一致，后面的IP表示server端的IP地址,我这里用的本机。
    
**4、安装完成之后；测试是否成功：在server执行命令如下：**
    
    [root@VM_45_127_centos backend]# salt-key -L
    Accepted Keys:
    Denied Keys:
    Unaccepted Keys:
    127.0.0.1
    Rejected Keys:
    [root@VM_45_127_centos backend]# salt-key -A
    The following keys are going to be accepted:
    Unaccepted Keys:
    127.0.0.1
    Proceed? [n/Y] y
    Key for minion 127.0.0.1 accepted.
    
    [root@VM_45_127_centos backend]# salt '*' test.ping
    127.0.0.1:
        True
    有这个返回值说明成功安装了，saltstack的master 和客户端。
    
**5、在server端同步client脚本到client：**
    
    salt '*' saltutil.sync_all
    
**6、在server端安装salt-api：**

    pip install salt-api
    参考文档构建证书：
    https://jaminzhang.github.io/saltstack/SaltStack-API-Config-and-Usage/
    
**7、建立mysql 数据库并且授权账号登录：**

    create database cmdb default charset=utf8;
    select host,user,password from mysql.user;
    create user test identified by 'test_1234';
    grant all privileges on *.* to 'test'@'localhost'identified by 'test_1234' with grant option;
    flush privileges ;
    
**8、修改配置文件config.ini(所在目录：/app/backend/):**

    [db]
    db_host = 127.0.0.1  
    db_port = 3306
    db_user = test
    db_pass = test_1234
    db_name = cmdb
    
    [saltstack]
    url = https://127.0.0.1:8888
    user = saltapi
    pass = saltapi
    [network]
    device = eth0

**9、数据库创建：**

    python manage.py syncdb
    python manage.py migrate app
    python manage.py makemigrations
    python manage.py migrate
    
**10、安装成功启动登录：**

    启动步骤：
    启动/data/auto_cmdb/app/backend
    
    
    nohup python salt_event_to_mysql.py &
    nohup python salt_event_to_mysql.py &   **#事件监听返回日志
    
    nohup ./manage.py runserver 0.0.0.0:80 &
    nohup python manage.py celery worker -A CMDB -l info &
    nohup python manage.py celery beat --loglevel=info &

