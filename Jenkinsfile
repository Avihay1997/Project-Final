pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"
        PEM_KEY = "/home/ubuntu/.ssh/private_key.pem"
        DOCKER_USER = "avihay1997"
        FLASK_CONTAINER_NAME = "flask-app"
        FLASK_IMAGE_NAME = "avihay1997/flask-app:latest"
        EC2_INSTANCE_ID = "i-0a16e2cee77eb8e88"
        EC2_REGION = "us-east-1"
        EC2_PUBLIC_IP = "44.211.74.145"
        EC2_PRIVATE_IP = "172.31.95.113"
    }

    stages {
        stage('Start EC2 Instance') {
            steps {
                sh """
                aws ec2 start-instances --instance-ids i-0a16e2cee77eb8e88 --region us-east-1
                aws ec2 wait instance-running --instance-ids i-0a16e2cee77eb8e88 --region us-east-1
                """
            }
        }

        stage('Clone Repository') {
            steps {
                git(url: 'https://github.com/Avihay1997/Project-Final', branch: 'main')
            }
        }

        stage('Build & Push Flask Image') {
            steps {
                sh 'docker build -f Dockerfile-flask -t flask-app .'
                sh "echo 'dckr_pat_UyFi28fTMFGMwRKl0Ch_pKoy1kw' | docker login -u avihay1997 --password-stdin"
                sh "docker push flask-app"
            }
        }

        stage('Deploy Flask on EC2') {
            steps {
                sh """
                ssh -o StrictHostKeyChecking=no -i ${PEM_KEY} ubuntu@44.211.74.145  << EOF
                echo 'dckr_pat_UyFi28fTMFGMwRKl0Ch_pKoy1kw' | docker login -u avihay1997 --password-stdin
                docker pull flask-app
                docker stop flask-app || true
                docker rm flask-app || true
                docker run -d --name flask-app -p 5000:5000 flask-app
                EOF
                """
            }
        }

        stage('Deploy Flask on Second EC2') {
            steps {
                sh """
                ssh -o StrictHostKeyChecking=no -i ${PEM_KEY} ubuntu@172.31.95.113 << EOF
                echo 'dckr_pat_UyFi28fTMFGMwRKl0Ch_pKoy1kw' | docker login -u avihay1997 --password-stdin
                docker pull flask-app
                docker stop flask-app || true
                docker rm flask-app || true
                docker run -d --name flask-app -p 5000:5000 flask-app
                EOF
                """
            }
        }
    }
}
