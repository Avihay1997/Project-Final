pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"
        EC2_HOST = "100.25.110.68"
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
                sh 'docker build -t flask-image -f App/Dockerfile .'
                sh 'docker build -t jenkins-image -f Jenkins/Dockerfile .'
                
                sh "docker login -u avihay1997 -p dckr_pat_ulUWvLF7xjNfcV7QMzyiD2N_sl8"
                sh "docker tag flask-image avihay1997/flask-image:latest"
                sh "docker tag jenkins-image avihay1997/jenkins-image:latest"
                sh "docker push avihay1997/flask-image:latest"
                sh "docker push avihay1997/jenkins-image:latest"
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh """
                ssh -i $PEM_KEY $EC2_USER@$EC2_HOST << EOF
                docker login -u avihay1997 -p dckr_pat_ulUWvLF7xjNfcV7QMzyiD2N_sl8
                docker pull avihay1997/flask-image:latest
                docker pull avihay1997/jenkins-image:latest
                docker stop flask-server || true
                docker stop jenkins-server || true
                docker rm flask-server || true
                docker rm jenkins-server || true
                docker run -d --name flask-server -p 5000:5000 avihay1997/flask-image:latest
                docker run -d --name jenkins-server -p 8080:8080 avihay1997/jenkins-image:latest
                EOF
                """
            }
        }
    }
}
