#!/bin/bash
if [[ -z $1 ]]; then
	echo "No interface supplied, using any instead"
	IFACE="any"
else
	IFACE=$1
fi
echo "Using $IFACE"

ssh ryu@192.168.0.36 -i /path/to/privatekey tcpdump -i $IFACE -U -s0 -w - 'not port 22' | wireshark -k -i -