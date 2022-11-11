#!/bin/sh

touch /output1.log
touch /output2.log
# run both in background
python3 /home/payload/workspace/src/socket_coms_1.py &>> /output.log & 
python3 /home/payload/workspace/src/socket_coms_2.py &>> /output.log &

echo "Sleep for 5 seconds"
sleep 5s
echo "Entrypoint Done"

cat /output.log

bash
