echo "start init salt."
release=`cat /etc/redhat-release | awk '{ print $3 }' | awk -F"." '{ print $1 }'`
interface=`route -n | awk '/^0.0.0.0/ { print $8 }'`
address=`ifconfig $interface | awk '/inet addr/ { gsub("addr:", "", $2 ); print $2 }'`
salt=`rpm -qa salt-minion | awk 'BEGIN {INSTALLED="no"} /salt-minion/{ INSTALLED="yes"} END { print INSTALLED }'`

if [ "$salt" == "no" ];then
  if [ $release -lt 6 ];then
    rpm -ivh http://mirrors.sohu.com/fedora-epel/5/x86_64/epel-release-5-4.noarch.rpm
  else
    rpm -ivh http://mirrors.sohu.com/fedora-epel/6/x86_64/epel-release-6-8.noarch.rpm
  fi
  yum install -q -y salt-minion
  wget -q -O /tmp/minion http://211.147.13.165/download/minion
  sed "s/id: 61.158.160.188/id: $address/" /tmp/minion > /etc/salt/minion
  /etc/init.d/salt-minion start
  chkconfig salt-minion on
fi
