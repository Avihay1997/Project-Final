pipeline {
    agent {
        docker {
            image 'docker:dind'
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root'
        }
    }
    environment {
        EC2_USER = "ubuntu"
        EC2_HOST = "54.173.91.223"
        PEM_KEY = "/home/ubuntu/.ssh/private_key.pem"
        REMOTE_PATH = "/home/ubuntu/Project-Final"
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
    }
    stages {
        stage('Clone Repository') {
            steps {
                sh 'apk add --no-cache git'
                git(url: 'https://github.com/Avihay1997/Project-Final', branch: 'main')
            }
        }
        stage('Build & Test Flask App') {
            steps {
                script {
                    sh 'apk add --no-cache python3 py3-pip'
                    sh 'python3 -m venv ./App/venv || python3 -m pip install virtualenv && python3 -m virtualenv ./App/venv'
                    sh './App/venv/bin/pip install --upgrade pip'
                    sh './App/venv/bin/pip install -r App/requirements.txt'
                    def testsExist = fileExists('App/tests')
                    if (testsExist) {
                        sh './App/venv/bin/python -m unittest discover App/tests'
                    } else {
                        echo 'No tests directory found, skipping tests.'
                    }
                }
            }
        }
        stage('Docker Build & Push') {
            steps {
                sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
                sh 'docker build -t app-flask -f ./App/Dockerfile-flask .'
                sh 'docker build -t app-jenkins -f ./App/Dockerfile-jenkins .'
                sh 'docker tag app-flask avihay1997/app-flask:latest'
                sh 'docker tag app-jenkins avihay1997/app-jenkins:latest'
                sh 'docker push avihay1997/app-flask:latest'
                sh 'docker push avihay1997/app-jenkins:latest'
            }
        }
        stage('Deploy to EC2') {
            steps {
                sh 'apk add --no-cache openssh-client'
                sh 'mkdir -p ~/.ssh'
                sh 'echo "StrictHostKeyChecking no" > ~/.ssh/config'
                sh "echo '-----BEGIN RSA PRIVATE KEY-----' > ~/.ssh/id_rsa"
                sh "cat $PEM_KEY >> ~/.ssh/id_rsa"
                sh "echo '-----END RSA PRIVATE KEY-----' >> ~/.ssh/id_rsa"
                sh "chmod 600 ~/.ssh/id_rsa"
                
                sh """
                ssh ubuntu@ip-172-31-95-113 << EOF
                docker login -u avihay1997 -p dckr_pat_ulUWvLF7xjNfcV7QMzyiD2N_sl8
                docker pull avihay1997/app-flask:latest
                docker pull avihay1997/app-jenkins:latest
                docker stop app-flask || true
                docker stop app-jenkins || true
                docker rm app-flask || true
                docker rm app-jenkins || true
                docker run -d --name app-flask -p 5000:5000 avihay1997/app-flask:latest
                docker run -d --name app-jenkins -p 8080:8080 avihay1997/app-jenkins:latest
                EOF
                """
            }
        }
    }
}
