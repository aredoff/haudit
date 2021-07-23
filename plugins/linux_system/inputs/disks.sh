#!/bin/sh
df -H | grep -vE '^Filesystem|udev|tmpfs|cdrom' | awk '{ print $1 " " $5 $4 }' | while read output;
do
  echo $output
  used=$(echo $output | awk '{ print $1}' | cut -d'%' -f1  )
  partition=$(echo $output | awk '{ print $2 }' )

done
