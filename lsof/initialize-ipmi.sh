yum -q -y install dmidecode ipmitool OpenIPMI

IPMI_USERNAME=ADMIN
IPMI_PASSWORD=ADMIN

IPMI_ADDRESS=`echo {ip} | awk 'BEGIN{FS="."} { print $3"."$4 }'`
MANUFACTURER=`dmidecode -t 1 | awk 'BEGIN {RESULT="NONE"} /Manufacturer/{ RESULT=$2 } END { print RESULT }'`
PRODUCT_NAME=`dmidecode -t 1 | awk 'BEGIN {RESULT="NONE"} /Product Name/{ RESULT=$4 } END { print RESULT }'`

if [ "$PRODUCT_NAME" == "RH2285" ];then
    IPMI_CHANNEL_ID=2
    IPMI_USER_ID=3
else
    IPMI_CHANNEL_ID=1
    IPMI_USER_ID=3
fi

service ipmi start
ipmitool lan set $IPMI_CHANNEL_ID ipaddr 10.254.$IPMI_ADDRESS
ipmitool lan set $IPMI_CHANNEL_ID netmask 255.255.0.0 
ipmitool lan set $IPMI_CHANNEL_ID defgw ipaddr 10.254.0.1
ipmitool lan set $IPMI_CHANNEL_ID access on
ipmitool user set name $IPMI_USER_ID $IPMI_USERNAME
ipmitool user set password $IPMI_USER_ID $IPMI_PASSWORD
ipmitool user enable $IPMI_USER_ID
ipmitool channel setaccess $IPMI_CHANNEL_ID $IPMI_USER_ID callin=on ipmi=on link=on privilege=4
service ipmi stop
