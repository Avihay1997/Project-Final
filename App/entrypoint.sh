#!/bin/bash
/usr/local/bin/jenkins.sh &

sleep 20

python3 ./App/app.py
