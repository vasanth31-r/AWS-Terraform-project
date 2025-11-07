pipeline {
    agent any

            environment {
            COMPOSE_FILE   = 'Application/docker-compose.yml'
            AWS_REGION     = 'ap-south-1'
            AWS_ACCOUNT_ID = '425816768212'
            ECR_REPO       = 'app_repo'
            IMAGE_TAG      = "${BUILD_NUMBER}"
            IMAGE_NAME     = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
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
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --no-progress --severity HIGH,CRITICAL "$image" || true
                    done < images.txt
                '''
            }
        }

                stage('AWS ECR Login') {
            steps {
                echo 'Logging into AWS ECR...'
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    sh '''
                        aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    '''
                }
            }
        }


        stage('Tag and Push to ECR') {
            steps {
                echo 'Tagging and pushing image to AWS ECR...'
                sh '''
                    docker tag application_flask_app:latest ${IMAGE_NAME}
                    echo "Pushing ${IMAGE_NAME}..."
                    docker push ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        always {
            echo 'Containers are running in background.'
            echo 'Flask app image is pushed to AWS ECR.'
        }
    }
}
