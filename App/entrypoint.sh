#!/bin/bash

/usr/bin/tini -- /usr/local/bin/jenkins.sh &

python3 /app/app.py
