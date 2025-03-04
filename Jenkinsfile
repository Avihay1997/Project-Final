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
        EC2_PUBLIC_IP = "3.84.27.17"
        EC2_PRIVATE_IP = "3.84.27.17"
        EC2_FLASK_PRIVATE_IP = "172.31.7.191"
    }

    stages {
        stage('Set AWS Credentials') {
            steps {
                script {
                    sh '''
                    aws configure set aws_access_key_id ""
                    aws configure set aws_secret_access_key ""
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
                        aws ec2 start-instances --instance-ids ${EC2_INSTANCE_ID} --region ${EC2_REGION} || true
                        aws ec2 wait instance-running --instance-ids ${EC2_INSTANCE_ID} --region ${EC2_REGION} || true
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
                sh 'docker build -f Dockerfile-flask -t flask-app .'
            }
        }

        stage('Push Flask Image to Docker Hub') {
            steps {
                sh "echo 'dckr_pat_UyFi28fTMFGMwRKl0Ch_pKoy1kw' | docker login -u avihay1997 --password-stdin"
                sh "docker push flask-app"
            }
        }

        stage('Deploy Flask on EC2 with Private IP') {
            steps {
                sh """
                ssh -o StrictHostKeyChecking=no -i ${PEM_KEY} ubuntu@172.31.7.191 << EOF
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
