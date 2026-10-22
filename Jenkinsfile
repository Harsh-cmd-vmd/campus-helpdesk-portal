pipeline {
    agent any

    environment {
        IMAGE_NAME = "campus-helpdesk"
        REGISTRY_CREDENTIALS = "dockerhub-creds"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                bat '''
                    python --version
                    if not exist .venv python -m venv .venv
                    call .venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    python -m unittest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${REGISTRY_CREDENTIALS}",
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
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
                withCredentials([usernamePassword(
                    credentialsId: "${REGISTRY_CREDENTIALS}",
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    bat '''
                        docker login -u "%DOCKERHUB_USER%" --password-stdin < nul
                    '''
                    powershell(
                        label: 'Login and push Docker images',
                        script: '''
                            $ErrorActionPreference = 'Stop'
                            $env:DOCKERHUB_TOKEN | docker login -u $env:DOCKERHUB_USER --password-stdin
                            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

                            docker push "$env:DOCKERHUB_USER/$env:IMAGE_NAME:$env:BUILD_NUMBER"
                            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

                            docker push "$env:DOCKERHUB_USER/$env:IMAGE_NAME`:latest"
                            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

                            docker logout
                        '''
                    )
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${REGISTRY_CREDENTIALS}",
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    bat '''
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

                    kubectl get deployment campus-helpdesk
                    if errorlevel 1 exit /b 1

                    kubectl get service campus-helpdesk
                    if errorlevel 1 exit /b 1
                '''
            }
        }
    }

    post {
        always {
            bat 'docker image prune -f'
        }

        success {
            echo 'Pipeline succeeded. Check the campus-helpdesk service in Kubernetes.'
        }
    }
}
