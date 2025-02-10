FROM jenkins/jenkins:2.479.3-jdk17

USER root

RUN apt-get update && apt-get install -y \
    lsb-release \
    ca-certificates \
    curl \
    gnupg \
  && curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
    https://download.docker.com/linux/debian/gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
    https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
  && apt-get update && apt-get install -y docker-ce-cli \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

USER jenkins
