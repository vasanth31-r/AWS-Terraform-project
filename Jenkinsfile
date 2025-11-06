pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/vasanthrathinam/AWS-Terraform-project.git'
            }
        }

        stage('Build and Run Containers') {
            steps {
                echo 'Starting application and database...'
                sh 'docker-compose up -d --build'
            }
        }

        stage('Trivy Scan') {
            steps {
                echo 'Running Trivy scan on images...'
                sh '''
                    docker images --format "{{.Repository}}:{{.Tag}}" | grep -E "application_flask_app|mysql" > images.txt || true
                    while read image; do
                        echo "Scanning $image..."
                        trivy image --no-progress --severity HIGH,CRITICAL $image || true
                    done < images.txt
                '''
            }
        }
    }

    post {
        always {
            echo 'Application and database are running in background.'
            echo 'Access the Flask app at: http://localhost:5000'
        }
    }
}
