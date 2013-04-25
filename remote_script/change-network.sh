echo "PASSWORD" | passwd root --stdin
echo "NETWORKING=yes" > /etc/sysconfig/network
echo "NETWORKING_IPV6=no" >> /etc/sysconfig/network
echo "HOSTNAME=ku6" >> /etc/sysconfig/network
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
