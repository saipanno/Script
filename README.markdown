Profile.d
====

此项目包含常用命令行工具的配置文件以及日常使用的脚本.


### 一 初始化
使用如下命令进行工作环境初始化:

	cd ~
	ln -s Projects/Profile.d/script/ bin
	ln -s Projects/Profile.d/bashrc/bash .bash
	ln -s Projects/Profile.d/bashrc/bashrc .bashrc
	ln -s Projects/Profile.d/bashrc/bash_profile .bash_profile
	ln -s Projects/Profile.d/zshrc/zsh .zsh
	ln -s Projects/Profile.d/zshrc/zshrc .zshrc
	ln -s Projects/Profile.d/tmux.conf .tmux.conf
	ln -s Projects/Profile.d/vimrc/vim .vim
	
	cd ~/.ssh
	ln ~/Projects/Profile.d/ssh_config/config config
	ln ~/Projects/Profile.d/ssh_config/authorized_keys authorized_keys
	
### 二 说明文档


##### 2.1 脚本说明
###### auto_login.expect
联通性测试脚本,支持socket测试以及ping测试.

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
SSH交互脚本,基于auto_login.expect

支持登录测试.执行命令以及从模板执行命令.

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

注:下面为-f参数指定变量文件的格式.

用`|`作为key和value的分隔符,用`,`作为多个变量赋值的分隔符,用`=`作为变量赋值的分隔符

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
      
##### 2.2 配置文件说明
###### vimrc
###### zshrc
###### bashrc
###### tmux.conf
###### vimperatorrc