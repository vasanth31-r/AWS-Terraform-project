pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'Application/docker-compose.yml'
        DOCKERHUB_CREDENTIALS = 'dockerhub'  // Jenkins credentials ID for Docker Hub (Username + Password)
        DOCKERHUB_USER = 'vasanth31r'        // Your Docker Hub username
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
                    set -e
                    docker-compose -f ${COMPOSE_FILE} down || true
                    docker-compose -f ${COMPOSE_FILE} up -d --build
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                echo 'Running Trivy scan on built images...'
                sh '''
                    docker images --format "{{.Repository}}:{{.Tag}}" | grep "application_flask_app" > images.txt || true
                    
                    while read image; do
                        echo "Scanning $image..."
                        trivy image --no-progress --severity HIGH,CRITICAL "$image" || true
                    done < images.txt
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing application image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        set -e
                        echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
                        
                        IMAGE_NAME=${DOCKERHUB_USER}/application_flask_app
                        BUILD_TAG=${BUILD_NUMBER:-latest}

                        docker tag application_flask_app:latest $IMAGE_NAME:$BUILD_TAG
                        docker tag application_flask_app:latest $IMAGE_NAME:latest
                        
                        echo "Pushing $IMAGE_NAME:$BUILD_TAG..."
                        docker push $IMAGE_NAME:$BUILD_TAG
                        docker push $IMAGE_NAME:latest

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
