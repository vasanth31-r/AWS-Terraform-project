pipeline {
    agent any
    environment {
        COMPOSE_FILE = 'Application/docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/vasanth31-r/AWS-Terraform-project.git', 
                    credentialsId: 'github-token'
            }
        }

        stage('Build and Run Containers') {
            steps {
                echo 'Building and starting containers...'
                sh '''
                    docker-compose -f ${COMPOSE_FILE} down || true
                    docker-compose -f ${COMPOSE_FILE} up -d --build
                '''
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
