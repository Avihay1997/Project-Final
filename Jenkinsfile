pipeline {
    agent any

    environment {
        EC2_USER = "ec2-user"
        EC2_HOST = "54.196.30.144"
        PEM_KEY = "/home/ubuntu/.ssh/private_key.pem"
        APP_NAME = "flask-app"
        REMOTE_PATH = "/home/ubuntu/$APP_NAME"
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
                    sh 'python3 -m venv /App/venv'
                    sh '/App/venv/bin/pip install --upgrade pip'
                    sh '/App/venv/bin/pip install -r App/requirements.txt'
                    
                    def testsExist = fileExists('App/tests')
                    if (testsExist) {
                        sh '/App/venv/bin/python3 -m unittest discover App/tests'
                    } else {
                        echo 'No tests directory found, skipping tests.'
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t flask-image -f App/Dockerfile .'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh """
                scp -i $PEM_KEY App/Dockerfile ubuntu@$EC2_HOST:$REMOTE_PATH/
                ssh -i $PEM_KEY ubuntu@$EC2_HOST << EOF
                cd $REMOTE_PATH
                docker-compose up -d --build
                EOF
                """
            }
        }
    }
}
