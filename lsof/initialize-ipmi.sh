MANUFACTURER=`dmidecode -t 1 | awk 'BEGIN {DEF="NONE"} /Manufacturer/{ DEF=$2 } END { print DEF }'`
PRODUCT=`dmidecode -t 1 | awk 'BEGIN {DEF="NONE"} /Product Name/ { DEF=$4 } END { print DEF }'`

yum -q -y install ipmitool OpenIPMI
service ipmi start
IPMI=`echo {ip} | awk 'BEGIN{FS="."} { print $3"."$4 }'`
ipmitool lan set 1 ipaddr 10.254.$IPMI
ipmitool lan set 1 netmask 255.255.0.0 
ipmitool lan set 1 defgw ipaddr 10.254.0.1
ipmitool lan set 1 access on
ipmitool user set name 3 saipanno 
ipmitool user set password 3 saipanno.com
ipmitool user enable 3
ipmitool channel setaccess 1 3 callin=on ipmi=on link=on privilege=4
service ipmi stop
