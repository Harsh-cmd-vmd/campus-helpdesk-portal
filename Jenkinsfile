
pipeline {
    agent any

    environment {
        PATH = "C:\\Users\\Ajit\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
        IMAGE_NAME = 'campus-helpdesk'
        REGISTRY_CREDENTIALS = 'dockerhub-creds'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Tools') {
            steps {
                bat '''
                    python --version
                    git --version
                    docker --version
                    kubectl version --client
                '''
            }
        }

        stage('Build and Test') {
            steps {
                bat '''
                    if not exist .venv (
                        python -m venv .venv
                    )
                    if errorlevel 1 exit /b 1

                    call .venv\\Scripts\\activate.bat

                    python -m pip install --upgrade pip
                    if errorlevel 1 exit /b 1

                    python -m pip install -r requirements.txt
                    if errorlevel 1 exit /b 1

                    python -m unittest discover -v
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        docker build -t "%DOCKERHUB_USER%/%IMAGE_NAME%:%BUILD_NUMBER%" .
                        if errorlevel 1 exit /b 1

                        docker tag "%DOCKERHUB_USER%/%IMAGE_NAME%:%BUILD_NUMBER%" "%DOCKERHUB_USER%/%IMAGE_NAME%:latest"
                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    powershell '''
                        $ErrorActionPreference = "Stop"

                        $env:DOCKERHUB_TOKEN |
                            docker login -u $env:DOCKERHUB_USER --password-stdin

                        if ($LASTEXITCODE -ne 0) {
                            exit $LASTEXITCODE
                        }

                        $tag = "$($env:DOCKERHUB_USER)/$($env:IMAGE_NAME):$($env:BUILD_NUMBER)"
                        $latest = "$($env:DOCKERHUB_USER)/$($env:IMAGE_NAME):latest"

                        docker push $tag
                        if ($LASTEXITCODE -ne 0) {
                            exit $LASTEXITCODE
                        }

                        docker push $latest
                        if ($LASTEXITCODE -ne 0) {
                            exit $LASTEXITCODE
                        }

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        kubectl config current-context
                        if errorlevel 1 exit /b 1

                        kubectl apply -f k8s/
                        if errorlevel 1 exit /b 1

                        kubectl set image deployment/campus-helpdesk campus-helpdesk=%DOCKERHUB_USER%/%IMAGE_NAME%:%BUILD_NUMBER%
                        if errorlevel 1 exit /b 1

                        kubectl rollout status deployment/campus-helpdesk --timeout=180s
                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                bat '''
                    kubectl get pods
                    if errorlevel 1 exit /b 1

                    kubectl get deployments
                    if errorlevel 1 exit /b 1

                    kubectl get services
                    if errorlevel 1 exit /b 1
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }

        success {
            echo 'SUCCESS: Build, test, Docker push, and deployment completed.'
        }

        failure {
            echo 'FAILED: Check Console Output for the first error.'
        }
    }
}
