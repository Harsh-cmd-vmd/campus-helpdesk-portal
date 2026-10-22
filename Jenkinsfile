pipeline {
    agent any
    environment {
        IMAGE_NAME = "campus-helpdesk"
        REGISTRY_CREDENTIALS = "dockerhub-creds"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build and Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python -m unittest -v
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${REGISTRY_CREDENTIALS}",
                    usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} .
                        docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }
        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${REGISTRY_CREDENTIALS}",
                    usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${REGISTRY_CREDENTIALS}",
                    usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        kubectl apply -f k8s/
                        kubectl set image deployment/campus-helpdesk campus-helpdesk=${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}
                        kubectl rollout status deployment/campus-helpdesk --timeout=180s
                    '''
                }
            }
        }
        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl get pods
                    kubectl get deployment campus-helpdesk
                    kubectl get service campus-helpdesk
                '''
            }
        }
    }
    post {
        always { sh 'docker image prune -f || true' }
        success { echo 'Pipeline succeeded. Check the campus-helpdesk service in Kubernetes.' }
    }
}
