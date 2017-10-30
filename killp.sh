#!/bin/bash

for pid in $(pgrep listen)
do
	echo "killing process "$pid
	kill -9 $pid
done
