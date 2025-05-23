pipeline {
    agent any

    environment {
        PROJECT_ID = 'ml-pipeline-demo-460014'
        REGION = 'europe-west3'
        IMAGE_NAME = 'wine-quality-api'
        ARTIFACT_REPO = "europe-west3-docker.pkg.dev/${PROJECT_ID}/ml-models/${IMAGE_NAME}"
    }

    stages {
        stage('Use GCP Credentials') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    echo '✅ Using GCP Credentials from Jenkins Credentials Manager'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build --platform=linux/amd64 -t $IMAGE_NAME .'
            }
        }

        stage('Tag Image for Artifact Registry') {
            steps {
                sh 'docker tag $IMAGE_NAME $ARTIFACT_REPO'
            }
        }

        stage('Push Image to Artifact Registry') {
            steps {
                sh 'docker push $ARTIFACT_REPO'
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh """
                    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                    gcloud run deploy $IMAGE_NAME \
                        --image=$ARTIFACT_REPO \
                        --region=$REGION \
                        --platform=managed \
                        --allow-unauthenticated
                    """
                }
            }
        }
    }
}
