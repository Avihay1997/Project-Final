pipeline {
    agent any

    environment {
        EC2_USER = "ec2-user"
        EC2_HOST = "54.196.30.144"
        PEM_KEY = "/home/ubuntu/.ssh/private_key.pem"  // Corrected secure path
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
                sh 'pip install -r App/requirements.txt'
                script {
                    // Check if the 'App/tests' directory exists before running tests
                    def testsExist = fileExists('App/tests')
                    if (testsExist) {
                        sh 'python3 -m unittest discover App/tests'
                    } else {
                        echo 'No tests directory found, skipping tests.'
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t flask-app -f App/Dockerfile .'
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
