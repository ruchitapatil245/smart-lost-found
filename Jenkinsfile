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
    }
}
