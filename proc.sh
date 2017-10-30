#!/bin/bash

DIR_PATH="/home/pi/workspace/drone-detector/"

# KILL all current running processes

bash $DIR_PATH"killp.sh"

# Find all file smaller than 30k and remove it.

find $DIR_PATH"data" -type f -size -30k -delete

for file in $DIR_PATH"data/*"
do
	python3 $DIR_PATH"analyze.py" $file
done


