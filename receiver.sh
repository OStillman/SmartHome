#!/bin/sh

while true;  do
	output=`./RPi_utils/RFSniffer`
	if [ -n "$output" ]; then
		echo $output
		sleep 1
	fi
	sleep 0.1
done
exit
