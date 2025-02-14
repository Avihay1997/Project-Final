#!/bin/bash
/usr/local/bin/jenkins.sh &

sleep 60

python3 /App/app.py
