pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"
        PEM_KEY = "/home/ubuntu/.ssh/private_key.pem"
        DOCKER_USER = "avihay1997"
        FLASK_CONTAINER_NAME = "flask-app"
        FLASK_IMAGE_NAME = "avihay1997/flask-app:latest"
    }

    stages {
        stage('Get EC2 Private IP') {
            steps {
                script {
                    FLASK_EC2_HOST = sh(script: "aws ec2 describe-instances --filters 'Name=tag:Flask-Server,Values=ec2_private_new_1' --query 'Reservations[*].Instances[*].PrivateIpAddress' --output text", returnStdout: true).trim()
                    echo "Flask EC2 Private IP: 172.31.7.191"
                }
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
                ssh -o StrictHostKeyChecking=no -i ${PEM_KEY} ec2_private_new_1@172.31.7.191 << EOF
                echo 'dckr_pat_UyFi28fTMFGMwRKl0Ch_pKoy1kw' | docker login -u avihay1997--password-stdin
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
