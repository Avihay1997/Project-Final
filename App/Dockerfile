# Jenkins - First stage
FROM jenkins/jenkins:lts-jdk17 AS jenkins

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

ENV JAVA_OPTS="-Xmx2g -Xms512m"

CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]

# Flask - Second stage
FROM python:3.11.11 AS flask

WORKDIR /App

RUN python3 -m venv /App/venv

COPY requirements.txt /App/requirements.txt
RUN /App/venv/bin/pip install --no-cache-dir -r /App/requirements.txt

COPY . /App/
RUN chmod +x /App/entrypoint.sh

EXPOSE 5000

CMD ["/App/venv/bin/python", "/App/app.py"]
