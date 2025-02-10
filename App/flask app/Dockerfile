FROM jenkins/jenkins:2.479.3-jdk17

USER root

RUN apt-get update && apt-get install -y \
    lsb-release \
    ca-certificates \
    curl \
    gnupg \
    python3 \
    python3-pip \
    python3-venv && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

EXPOSE 8080 5000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
