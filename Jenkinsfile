pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub-credentials')
        IMAGE_NAME = 'sahilbhuva2001/python-cicd-app'
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {
        stage('Sahil.Bhuva - Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG -t $IMAGE_NAME:latest .'
            }
        }

        stage('Sahil.Bhuva - Login to Dockerhub') {
            steps {
                sh 'echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin'
            }
        }

        stage('Sahil.Bhuva - Push image to Dockerhub') {
            steps {
                sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
                sh 'docker push $IMAGE_NAME:latest'
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
    }
}