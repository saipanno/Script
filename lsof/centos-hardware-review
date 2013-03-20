#!/bin/bash

MEM_TOTAL=`free -g | awk '/Mem/ { print $2+1 }'`
echo "MEM_TOTAL: "$MEM_TOTAL

MEM_TYPE=`dmidecode | grep -A5 "Memory Device$" | awk 'BEGIN {ORS=","} /Size/ {if(NF==3 && $3=="MB") { print $2/1024"G" }}'`
echo "MEM_TYPE: "$MEM_TYPE

CPU_INFO=`awk -F ":" '/model name/ { CPU=$2 } END { print CPU }' /proc/cpuinfo`
echo "CPU_INFO: "$CPU_INFO

DISK_INFO=`fdisk -l | grep "^Disk /dev" | awk 'BEGIN {ORS=","} {print $3}'`
echo "DISK_INFO: "$DISK_INFO
