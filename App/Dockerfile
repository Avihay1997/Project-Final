# Jenkins - First stage
FROM jenkins/jenkins:2.479.3-jdk17 AS jenkins

USER root

RUN apt-get update && apt-get install -y \
    lsb-release \
    curl \
    gnupg \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

VOLUME ["/var/jenkins_home"]

EXPOSE 8080 50000

ENV JAVA_OPTS=""

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]

# Flask - Second stage
FROM python:3.11-slim AS flask

WORKDIR /App

COPY requirements.txt /App/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /App/
RUN chmod +x /App/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/App/entrypoint.sh"]
