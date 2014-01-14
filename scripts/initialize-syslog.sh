echo "start init syslog."
if [ -f /etc/rsyslog.conf ];then
    SYSLOG="/etc/rsyslog.conf"
    SYSLOGD="rsyslog"
elif [ -f /etc/syslog.conf ];then
    SYSLOG="/etc/syslog.conf"
    SYSLOGD="syslog"
else
    SYSLOG="/dev/null"
fi
grep -q "122.11.39.45" $SYSLOG >> /dev/null
if [ $? != 0 ];then
    echo "*.*                             @122.11.39.45" >> $SYSLOG
    /etc/init.d/$SYSLOGD restart
fi
