pipeline {
    agent any
    environment {
        COMPOSE_FILE = 'Application/docker-compose.yml'
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'  // Jenkins credential ID for Docker Hub (Username + Password)
        DOCKERHUB_USER = 'vasanth31r'              // your Docker Hub username
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', 
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

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing images to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
                        
                        docker tag application_flask_app:latest ${DOCKERHUB_USER}/application_flask_app:latest
                        docker tag mysql:latest ${DOCKERHUB_USER}/mysql:latest
                        
                        docker push ${DOCKERHUB_USER}/application_flask_app:latest
                        docker push ${DOCKERHUB_USER}/mysql:latest
                        
                        docker logout
                    '''
                }
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
