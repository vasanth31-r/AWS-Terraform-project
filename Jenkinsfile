pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Compose') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Run Trivy Scan') {
            steps {
                echo 'Running Trivy scans on images...'
                // List all compose images
                script {
                    def images = sh(script: "docker compose images --quiet", returnStdout: true).trim().split('\n')
                    for (img in images) {
                        echo "Scanning image: ${img}"
                        // Run scan but ignore exit code (so pipeline won't fail)
                        sh "trivy image --no-progress --exit-code 0 ${img} || true"
                    }
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                echo 'Starting application with Docker Compose...'
                sh 'docker compose up -d'
            }
        }
    }

    post {
        always {
            echo 'Stopping containers...'
            sh 'docker compose down || true'
        }
    }
}

