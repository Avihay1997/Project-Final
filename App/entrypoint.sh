#!/bin/bash
java -jar /usr/share/jenkins/jenkins.war &

sleep 20

python3 /App/app.py
