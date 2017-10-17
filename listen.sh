#!/bin/bash

# Sleep to wait for system ready
cd /home/pi/workspace/wiflistener/
for i in {0..999}
do
	file="data/records"$i".log"
	if [ ! -f $file ]
	then
		echo "Filename chosen is "$file
		filename="/home/pi/workspace/wiflistener/"$file
		break
	fi
done
echo "Starting script at $(date)" >> $filename
sleep 15
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
echo "$num is 1 and my script is working up to this point $loop" >> $filename

while [[ $num -le $loop ]]
do
	echo "ITERATION $num" >> $filename
	echo $(date) >> $filename
	wpa_cli scan_results | sed '/Selected/,+1 d' >> $filename
	echo "END ITERATION $num" >> $filename
	sleep 5
	((num++))
done
