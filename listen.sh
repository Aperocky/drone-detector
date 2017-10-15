#!/bin/bash
 
# Sleep to wait for system ready

sleep 30
filename="/home/pi/workspace/wiflistener/records.log"
echo "Starting script at $(date)" >> $filename
wpa_cli scan >> $filename
sleep 5

loop=99999

if [[ $# -ge 1 ]]
then
	echo "doing $1 loops" >> $filename
	loop=$1
else
	echo "doing infinite loops" >> $filename
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
