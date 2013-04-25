setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config 
sed -i 's/SELINUX=permissive/SELINUX=disabled/g' /etc/selinux/config
