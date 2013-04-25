#!/bin/bash 
#
#    get_performance.sh,
#
#         some script.
#
#    Created by Ruoyan Wong, at 2013年03月27日.

whereis iostat | awk '
    {
        if(NF==1) {
            system("yum -q -y clean all >> /dev/null")
            system("yum -q -y install sysstat >> /dev/null")
        }
    }
'

iostat -c 2 6 | awk '
    BEGIN {START=0; IOWAIT=0; IDLE=0} 
    
    { 
        if($1~/avg-cpu/) { 
            if(START!=0) { 
                getline; 
                IOWAIT+=$4; 
                IDLE+=$6; 
            } else {
                START=1;
            } 
        }
    } 
        
    END { 
        print "CPU_IOWAIT: "IOWAIT/5;
        print "CPU_IDLE: "IDLE/5;
    }
'

sar -b 2 5 | awk '
    BEGIN{RTPS=0;WTPS=0} 
    
    { 
        IO_RTPS=$3;
        IO_WTPS=$4;
    }

    END {
        print "IO_RTPS: "IO_RTPS;
        print "IO_WTPS: "IO_WTPS;
    }
'

free -m | awk '
    /Mem/{ 
        print "MEM_TOTAL: "$2;
        print "MEM_FREE: "$4;
    }
'
