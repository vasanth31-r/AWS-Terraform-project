pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                // ✅ Add credentialsId for GitHub authentication
                git branch: 'master',
                    url: 'https://github.com/vasanthrathinam/AWS-Terraform-project.git',
                    credentialsId: 'github-token'  // <-- use your Jenkins credential ID
            }
        }

        stage('Build and Run Containers') {
            steps {
                echo 'Building and starting containers...'
                sh '''
                    docker-compose down || true
                    docker-compose up -d --build
                    echo "Containers are up and running..."
                    docker ps
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                echo 'Running Trivy scan for images...'
                sh '''
                    # Get relevant images
                    docker images --format "{{.Repository}}:{{.Tag}}" | grep -E "application_flask_app|mysql" > images.txt || true

                    while read image; do
                        if [ ! -z "$image" ]; then
                            echo "-----------------------------------------"
                            echo "🔍 Scanning image: $image"
                            echo "-----------------------------------------"
                            trivy image --no-progress --severity HIGH,CRITICAL $image || true
                        fi
                    done < images.txt
                '''
            }
        }
    }

    post {
        always {
            echo '✅ Build complete.'
            echo 'Flask application and MySQL database are running in background.'
            echo 'Access your Flask app at: http://localhost:5000'
            echo 'Use "docker ps" on your machine to verify running containers.'
        }
        cleanup {
            echo 'Cleaning temporary files...'
            sh 'rm -f images.txt || true'
        }
    }
}
