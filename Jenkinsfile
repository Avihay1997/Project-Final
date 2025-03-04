pipeline {
    agent {
        docker {
            image 'docker:20.10.7'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        EC2_USER = "ubuntu"
        PEM_KEY = "/home/ubuntu/.ssh/private_key.pem"
        DOCKER_USER = "avihay1997"
        FLASK_CONTAINER_NAME = "flask-app"
        FLASK_IMAGE_NAME = "avihay1997/flask-app:latest"
        EC2_INSTANCE_ID = "i-0a16e2cee77eb8e88"
        EC2_REGION = "us-east-1"
        EC2_PUBLIC_IP = "18.233.102.46"
        EC2_PRIVATE_IP = "172.31.95.113"
        EC2_FLASK_PRIVATE_IP = "172.31.7.191"
    }

    stages {
        stage('Set AWS Credentials') {
            steps {
                script {
                    sh '''
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                    aws configure set region "us-east-1"
                    aws configure set output "json"
                    '''
                }
            }
        }

        stage('Check AWS Identity') {
            steps {
                script {
                    sh '''
                    export AWS_PAGER=""
                    aws sts get-caller-identity
                    '''
                }
            }
        }

        stage('Start EC2 Instance') {
            steps {
                script {
                    try {
                        sh """
                        aws ec2 start-instances --instance-ids i-0a16e2cee77eb8e88 --region us-east-1 || true
                        aws ec2 wait instance-running --instance-ids i-0a16e2cee77eb8e88 --region us-east-1 || true
                        """
                    } catch (Exception e) {
                        echo "EC2 instance start failed, skipping this stage."
                    }
                }
            }
        }

        stage('Clone Repository') {
            steps {
                git(url: 'https://github.com/Avihay1997/Project-Final', branch: 'main')
            }
        }

        stage('Build Flask Docker Image') {
            steps {
                sh 'docker --version'
                sh 'sh 'docker build -f /home/ubuntu/Project-Final/App/Dockerfile-flask -t flask-app /home/ubuntu/Project-Final/App'
'
            }
        }

        stage('Push Flask Image to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'DOCKER_HUB_TOKEN', variable: 'DOCKER_TOKEN')]) {
                    sh "echo 'DOCKER_HUB_TOKEN' | docker login -u avihay1997 --password-stdin"
                    sh "docker push flask-app"
                }
            }
        }

        stage('Deploy Flask on EC2 with Private IP') {
            steps {
                sh """
                ssh -o StrictHostKeyChecking=no -i ${PEM_KEY} ubuntu@172.31.7.191 << EOF
                echo 'DockerToken' | docker login -u avihay1997 --password-stdin
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
