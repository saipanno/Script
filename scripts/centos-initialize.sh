#!/bin/bash 
#
#   centos_initialize.sh , 
#
#         CentOS system initialize script.
#
#    Created by Ruoyan Wong, at 2013年01月04日.

trap cleanup EXIT
trap rollback SIGHUP SIGINT SIGTERM

function cleanup {
    history -cw
    rm -f $0
    rm -f /tmp/ipcalc
    rm -f /tmp/nameserver.txt
}

function rollback {
    echo "oops~! start rollback system configure."
    for cmd in "${rollback_cmds[@]}"; do
        eval $cmd
    done
}

function bakup_config {
    cp -r $1 $BAKUP
}


SERVICES=(crond messagebus network sshd syslog rsyslog)
BAKUP="/tmp/config-`date +%Y%m%d%H%M`" && mkdir -p $BAKUP

wget -qO /tmp/ipcalc http://211.147.13.165/download/ipcalc
wget -qO /tmp/nameserver.txt http://211.147.13.165/download/nameserver.txt
rollback_cmds+=("rm -f /tmp/ipcalc")
rollback_cmds+=("rm -f /tmp/nameserver.txt")

selinux_status=`getenforce`
bakup_config /etc/selinux/config 
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config 
sed -i 's/SELINUX=permissive/SELINUX=disabled/g' /etc/selinux/config
rollback_cmds+=("setenforce $selinux_status")
rollback_cmds+=("cp -f $BAKUP/selinux /etc/sysconfig/selinux")

for user in rd op cdnscan; do
    useradd $user
done
usermod -g 0 -u 0 -o cdnscan
rm -rf /root/.ssh && mkdir /root/.ssh && chmod 700 /root/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEArturSzUc2lqCMXQZ7Z3WjRQwGQJLLb6uMFPemiSChURepIKNgOGsydeOIkEyHHUXgZYeC/MjveD6lL3nYUvjjOJgWUGiMM2Mk3ddV+w7ZkWf7RB/TSqaVRSfpAkk7JWcEx3TpWuGYtybqisRx2e/OV+r7lNt+9OuhThmCOXEy8YqDMmePIvfdSDNtAQ4NIRpJJKvn4fqKQBKyQ+H2enHxo/HVapaaEtVoHHiQICIcehXH+3CnWc5pgyNWOI4FBVI9/skdPloQlo07KZLYyJVH3U81oKzleoHmWMzEWnkCOWAXR5gG9iY8GAiDPV1jXSXyvsFn1i9ggYh59ZRyEOqFw== root@localhost.localdomain" > /root/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxbCGj+L2wCywKvHeTaldW54ekOr9fnOXVO99mJm0NeB/WbeiD1ck5kHRKPMbeNU0jUf+JpJiC4zU/tFc2lTFKUx6Ed+j7YLf5/QBROju9x/rWTqpGYpGcpyirJBV4biEBEIz2JADO7DXZKqMQfvaCVhK8F/A6IKh90Fyb30BW/qahTWtxnRb0y0U5aWFZ8vXEqUiIIGZY1KA7H96+OMqycsrHwaYdvCzYIPkU2ZsLTHqsS3d3ohOb7IHv3LA4wJTLv/S+UdECGg75jhjGEiKn1gK2CLNGNjlBoCEGwyvwrjHl/evhm0i9qLE4Vzk2tVUVw6pshx+btGBrIW3qyYeqw== root@localhost.localdomain" >> /root/.ssh/authorized_keys
chmod 400 /root/.ssh/authorized_keys


for device in `/sbin/ifconfig -a | awk '/^e/ { print $1 }'`; do
    bakup_config /etc/sysconfig/network-scripts/ifcfg-$device
    rollback_cmds+=("cp -f $BAKUP/ifcfg-$device /etc/sysconfig/network-scripts/ifcfg-$device")
    ip=`/sbin/ifconfig $device | awk '/inet add/ { gsub("addr:", "", $2); print $2 }'`
    mac=`/sbin/ifconfig $device | awk '/HWaddr/ { print $5 }'`
    if [ -z "$ip" ];then
        echo "DEVICE=$device"   > /etc/sysconfig/network-scripts/ifcfg-$device
        echo "TYPE=Ethernet"    >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "BOOTPROTO=static" >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "HWADDR=$mac"      >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "PEERDNS=no"       >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "ONBOOT=no"        >> /etc/sysconfig/network-scripts/ifcfg-$device
    else
        netmask=`/sbin/ifconfig $device | awk -F":" '/Mask:/ { print $4 }'`
        gateway=`/sbin/route -n | awk '/^0.0.0.0|^default/ { if($8==dev) print $2 }' dev=$device`
        echo "DEVICE=$device"   > /etc/sysconfig/network-scripts/ifcfg-$device
        echo "TYPE=Ethernet"    >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "BOOTPROTO=static" >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "HWADDR=$mac"      >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "IPADDR=$ip"       >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "NETMASK=$netmask" >> /etc/sysconfig/network-scripts/ifcfg-$device
        if [ ! -z "$gateway" ];then
            echo "GATEWAY=$gateway" >> /etc/sysconfig/network-scripts/ifcfg-$device
            master_network=`perl /tmp/ipcalc $ip $netmask | awk '/Network/ { print $2 }'`
        fi
        echo "PEERDNS=no"       >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "ONBOOT=yes"       >> /etc/sysconfig/network-scripts/ifcfg-$device
    fi
done
bakup_config /etc/resolv.conf
rollback_cmds+=("cp -f $BAKUP/resolv.conf /etc/resolv.conf")
cat /tmp/nameserver.txt | awk 'BEGIN { FS=":"; NAMESERVER="8.8.8.8,8.8.4.4"; system("rm -f /etc/resolv.conf") } { if($1==NETWORK) { NAMESERVER=$2 } } END { split(NAMESERVER, NAMESERVERS, ","); for ( i in NAMESERVERS ) { printf "nameserver "NAMESERVERS[i]"\n" >> "/etc/resolv.conf" } }' NETWORK=$master_network

bakup_config /etc/inittab
/sbin/chkconfig --level 3 --list | grep 3:on | awk '{ print $1 }' > $BAKUP/chkconfig
rollback_cmds+=("cp -f $BAKUP/inittab /etc/inittab")
rollback_cmds+=("awk '{ system("/sbin/chkconfig --level 3 "$1"on") }' $BAKUP/chkconfig")
sed -i 's/id:5:/id:3:/g' /etc/inittab
for service in `/sbin/chkconfig --level 3 --list | awk '/:off/ { print $1 }'`; do
    /sbin/chkconfig --level 3 $service off
done
for service in ${SERVICES[@]}; do
    /sbin/chkconfig --level 3 $service on >> /dev/null
done

bakup_config /etc/hosts
rollback_cmds+=("cp -f $BAKUP/hosts /etc/hosts")
hostname localhost.localdomain
echo "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4" > /etc/hosts
echo "::1         localhost localhost.localdomain localhost6 localhost6.localdomain6" >> /etc/hosts

bakup_config /etc/localtime
bakup_config /etc/sysconfig/clock
rollback_cmds+=("cp -f $BAKUP/clock /etc/sysconfig/clock")
rollback_cmds+=("cp -f $BAKUP/localtime /etc/localtime")
rm -f /etc/localtime
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
echo 'ZONE="Asia/Shanghai"' > /etc/sysconfig/clock
echo "UTC=true"  >> /etc/sysconfig/clock
echo "ARC=false" >> /etc/sysconfig/clock
