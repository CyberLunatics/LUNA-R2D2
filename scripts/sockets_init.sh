#!/bin/sh

mkdir /tmp/payload_sockets
nc -vklU /tmp/payload_sockets/pl_sock_a &
PID=$!
sleep 1
kill $PID
nc -vklU /tmp/payload_sockets/pl_sock_b &
PID=$!
sleep 1
kill $PID
