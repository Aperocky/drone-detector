#!/bin/bash
 
# Sleep to wait for system ready

sleep 60
filename="/home/pi/workspace/wiflistener/records.log"
echo "Starting script at $(date)" >> $filename
wpa_cli scan >> $filename

loop=99999

if [[ $# -ge 1 ]]
then
	echo "doing $1 loops"
	loop=$1
else
	echo "doing infinite loops"
fi

num=1

while [[ $num -le $loop ]]
do
	echo $num
	echo "ITERATION $num" >> $filename
	date >> $filename
	wpa_cli scan_results | sed '/Selected/,+1 d' >> $filename
	echo "END ITERATION $num" >> $filename
	sleep 5
	((num++))
done
