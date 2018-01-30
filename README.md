运维平台搭建过程

运维平台基于saltstack的接口调用来实现，操作管理，用户管理，代码发布，和任务编排等系统，有监控管理系统，监控告警，模板管理和维护周期。

安装步骤（基本环境，需要安装好（Django、south、MySQLdb、celery、模块）安装过程报错就继续安装模块即可）：

pip install 'django==1.8.1'

pip install south

pip install MySQL-python

pip install django-celery

pip install celery

1、在服务端建立/web目录。把项目拷贝到目录下。

2、在服务起端执行脚本:(在/web/CMDB/app/backend目录存放)

install_server.sh
3、在cp 客户端脚本到client执行，注意执行格式：

./install_client.sh client 192.168.63.239     
client表示客户端主机ID，建议跟主机的Hostname一致，，后面的IP表示server端的IP地址。
4、安装完成之后；测试是否成功：在server执行命令如下：

[root@master backend]# salt '*' test.ping
    client:
        True
        
有这个返回值说明成功安装了，saltstack的master 和客户端。
5、在server端同步client脚本到client：

salt '*' saltutil.sync_all
6、在server端安装salt-api，因为大部分操作都是调用api,可以参考博客（因为需要手工指定证书，所以没有做成脚本的形式）：

7、建立mysql 数据库并且授权账号登录：

create database cmdb default charset=utf8;
8、修改配置文件config.ini(所在目录：/data1/web/CMDB/app/backend/):

[db]
db_host = 127.0.0.1  
db_port = 3306
db_user = root
db_pass = 123456
db_name = cmdb
[saltstack]
url = https://192.168.0.194:8999
user = salt
pass = 123456
[network]
device = eth0
9、数据库创建：

python manage.py syncdb
python manage.py migrate app
python manage.py makemigrations
10、安装成功启动登录：

启动步骤：
启动/web/CMDB/app/backend


nohup python salt_event_to_mysql.py &
nohup python salt_event_to_mysql.py &   ###事件监听返回日志

nohup ./manage.py runserver 0.0.0.0:8999 &
nohup python manage.py celery worker -A CMDB -l info
nohup python manage.py celery beat --loglevel=info

