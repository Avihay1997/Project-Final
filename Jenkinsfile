pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"
        EC2_HOST = "52.91.136.217"
        PEM_KEY = "/home/ubuntu/.ssh/private_key.pem"
        REMOTE_PATH = "/home/ubuntu/Project-Final"
        DOCKER_USER = "avihay1997"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git(url: 'https://github.com/Avihay1997/Project-Final', branch: 'main')
            }
        }

        stage('Build & Test Flask App') {
            steps {
                script {
                    sh 'echo $PATH'
                    sh 'which python3 || echo "Python3 not found!"'
                    sh '/usr/bin/python3 -m venv ./App/venv'
                    sh './App/venv/bin/python -m pip install --upgrade pip'
                    sh './App/venv/bin/python -m pip install -r App/requirements.txt'

                    def testsExist = fileExists('App/tests')
                    if (testsExist) {
                        sh './App/venv/bin/python3 -m unittest discover App/tests'
                    } else {
                        echo 'No tests directory found, skipping tests.'
                    }
                }
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh 'export PATH=$PATH:/usr/bin'

                sh 'docker build -t app-flask -f ./App/Dockerfile .'
                sh 'docker build -t app-jenkins -f ./App/Dockerfile .'
                
                sh "docker login -u avihay1997 -p dckr_pat_HsF9WPS9veZ6d3a5WjPiSGcvlQk"
                sh "docker tag app-flask avihay1997/app-flask:latest"
                sh "docker tag app-jenkins avihay1997/app-jenkins:latest"
                sh "docker push avihay1997/app-flask:latest"
                sh "docker push avihay1997/app-jenkins:latest"
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh """
                ssh -i $PEM_KEY $EC2_USER@$EC2_HOST << EOF
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
