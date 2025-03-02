pipeline {
    agent any
    environment {
        CONTAINER_NAME = "flask-app"
        IMAGE_NAME = "flask-image"
        SERVER_IP = "172.31.7.191"
        DOCKER_USER = "avihay1997"
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Avihay1997/Project-Final'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -f Dockerfile-flask -t flask-app .'
                }
            }
        }
        stage('Run New Flask Container') {
            steps {
                script {
                    sh 'docker run -d --name flask-app -p 5000:5000 flask-app'
                }
            }
        }
    }
}
