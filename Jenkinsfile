pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/ruchitapatil245/smart-lost-found.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install -r requirements.txt'
                sh 'venv/bin/pip install pytest'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'venv/bin/pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '/mnt/c/Users/yashp/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe build -t ruchita13/smart-lost-found:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | /mnt/c/Users/yashp/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe login -u "$DOCKER_USER" --password-stdin
                        /mnt/c/Users/yashp/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe push ruchita13/smart-lost-found:latest
                        /mnt/c/Users/yashp/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    export KUBECONFIG=/var/lib/jenkins/.kube/config
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    kubectl rollout restart deployment/lost-found-deployment
                    kubectl rollout status deployment/lost-found-deployment --timeout=120s
                '''
            }
        }
    }
}
