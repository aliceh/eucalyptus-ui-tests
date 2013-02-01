#!/bin/sh

source eucarc
ip=`euca-describe-instances  |grep INSTANCE  |awk '{print $4}' |head -1`
ssh-keyscan $ip >> ~/.ssh/known_hosts
output=`ssh -i selenium.key root@$ip mkfs.ext4 /dev/vdb`
if [ $? = "0" ]; then
  echo "Successfully formatted attached volume"
else
  echo "Unable to format attached volume!"
  exit 1
fi
