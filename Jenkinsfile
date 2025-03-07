pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        EC2_USER = "ubuntu"
        PEM_KEY = "/home/ubuntu/.ssh/private_key.pem"
        DOCKER_USER = "avihay1997"
        FLASK_CONTAINER_NAME = "flask-app"
        FLASK_IMAGE_NAME = "avihay1997/flask-app:latest"
        EC2_INSTANCE_ID = "i-0240376f821f04c5a"
        EC2_REGION = "us-east-1"
        EC2_PUBLIC_IP = "35.173.134.29"
        EC2_PRIVATE_IP = "172.31.95.113"
        EC2_FLASK_PRIVATE_IP = "172.31.19.76"
        ROOT_PASSWORD = credentials('root_password')
        DOCKER_REGISTRY = "docker.io"
        IMAGE_NAME = "docker.io/avihay1997/flask-app"
        DOCKER_HUB_TOKEN = credentials('DOCKER_HUB_TOKEN')
        MY_SSH_KEY = credentials('MY_SSH_KEY')
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
                        aws ec2 start-instances --instance-ids i-0240376f821f04c5a --region us-east-1 || true
                        aws ec2 wait instance-running --instance-ids i-0240376f821f04c5a --region us-east-1 || true
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

        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'DOCKER_HUB_TOKEN', variable: 'DOCKER_HUB_TOKEN')]) {
                        sh """
                        echo "\$DOCKER_HUB_TOKEN" | docker login -u avihay1997 --password-stdin
                        """
                    }
                }
            }
        }

        stage('Build Flask Docker Image') {
            steps {
                script {
                    sh "docker build -f /App/Dockerfile-flask -t avihay1997/flask-app:latest /App"
                }
            }
        }
        
        stage('Push Flask Image to Docker Hub') {
            steps {
                script {
                    sh "docker push avihay1997/flask-app:latest"
                }
            }
        }

        stage('Deploy Flask on EC2 with Private IP') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'MY_SSH_KEY', 
                                                       keyFileVariable: 'SSH_KEY', 
                                                       usernameVariable: 'ubuntu')]) {
                        sh '''
                        ssh -o StrictHostKeyChecking=no -i $SSH_KEY ubuntu@172.31.19.76 " \
                            echo \$DOCKER_HUB_TOKEN | docker login -u avihay1997 --password-stdin && \
                            docker pull avihay1997/flask-app:latest && \
                            docker stop flask-app || true && \
                            docker rm flask-app || true && \
                            docker run -d --name flask-app -p 5000:5000 avihay1997/flask-app:latest \
                        "
                        '''
                    }
                }
            }
        }
    }
}
