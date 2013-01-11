Script
====

此项目包含日常使用的脚本.


### 一、初始化
使用如下命令进行工作环境初始化:

	mkdir ~/bin && cd ~/bin
	for file in `ls ~/Projects/Script/*`; do; script=`echo $file | awk -F"/" '{ print $NF }'`; ln -s $file $script; done

	
### 二、说明文档


###### auto_login.expect
SSH交互脚本,支持登录测试,执行命令.

    $ expect auto_login.expect help
    Usage: auto_login.expect [arguments]: 

    必须参数:
        o  OPERATE 操作类型,支持run, test和interact三种,必须项
        a  ADDRESS 待处理机器, 支持主机名或IP地址
        d  LOGDIR  日志目录
        u  USER    SSH用户
        p  PORT    SSH端口
        c  SCRIPT  远程执行的脚本
        i  SECRET  SSH用户密钥
        s  SHADOW  SSH用户密码
        t  TIMEOUT 程序内建超时

###### multiexpect.py
批量SSH交互脚本,基于auto_login.expect.支持登录测试.执行命令以及从模板执行命令.

    $ python multiexpect.py -h
    usage: multiexpect.py [-h] -o {run,test} [-u USER] [-p PORT] [-d LOGDIR]
                          [-i SECRET] [-s SHADOW] [-r PROCS] [-t TIMEOUT]
                          [-f SCRIPT] [-v VARIABLE]
                          target

    必须参数:
      待处理机器列表, 支持主机名或IP地址.

    非必须参数:
      -h, --help     显示帮助
      -o {run,test}  操作类型,支持run和test两种,必须项
      -u USER        SSH用户,默认为: root
      -p PORT        SSH端口,默认为: 22
      -d LOGDIR      日志目录,默认为: ~/logging
      -i SECRET      SSH用户密钥,默认为: ~/.ssh/ku_rsa
      -s SHADOW      SSH用户密码,默认为: ~/.ssh/ku_password
      -r PROCS       并发数量,默认为: 250
      -t TIMEOUT     程序内建超时,默认为: 45

    run操作必须参数:
      -f SCRIPT      远程执行的脚本或脚本模板
      -v VARIABLE    用于模板生成的变量文件

脚本模板以及变量文件的格式

**脚本模板**: 用`{`和`}`作为外部变量的定界符,模板中的`{var}`会自动按照变量文件中的定义进行替换.同时模板依然支持shell中的`$`变量


    for device in `/sbin/ifconfig -a | awk '/^e/ { print $1 }'`; do
      mac=`ifconfig $device | grep HWaddr | awk '{ print $5 }'` 
      if [ "$device" == "eth0" -o "$device" == "em1" ]; then
        echo "DEVICE=$device"    > /etc/sysconfig/network-scripts/ifcfg-$device
        echo "TYPE=Ethernet"     >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "BOOTPROTO=static"  >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "HWADDR=$mac"       >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "IPADDR={address}"  >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "NETMASK={netmask}" >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "GATEWAY={gateway}" >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "ONBOOT=yes"        >> /etc/sysconfig/network-scripts/ifcfg-$device
      else
        echo "DEVICE=$device"    > /etc/sysconfig/network-scripts/ifcfg-$device
        echo "TYPE=Ethernet"     >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "HWADDR=$mac"       >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "ONBOOT=no"        >> /etc/sysconfig/network-scripts/ifcfg-$device
      fi  
    done
**变量文件**: 用`|`作为key和value的分隔符,用`,`作为多个变量赋值的分隔符,用`=`作为变量赋值的分隔符

    60.175.193.194|address=61.132.226.195,gateway=61.132.226.254,netmask=255.255.255.192
###### multichecking.py
联通性测试脚本,支持socket测试以及ping测试.


    $ python multichecking.py -h
    usage: multichecking.py [-h] -o {ping,socket} [-d LOGDIR] [-b PROCS]
                            [-t TIMEOUT]
                            target

    必须参数:
      待测试机器列表, 支持主机名或IP地址.

    非必须参数:
      -h, --help        显示帮助
      -o {ping,socket}  测试类型,支持socket和ping两种,必须项
      -d LOGDIR         日志目录,默认为: ~/logging
      -b PROCS          并发数量,默认为: 250
      -t TIMEOUT        程序内建超时,默认为: 10
      
