def ENV_NAME = getEnvName(env.BRANCH_NAME)
def CONTAINER_NAME = "accountings-api-" + ENV_NAME
def CONTAINER_TAG = getTag(env.BUILD_NUMBER, env.BRANCH_NAME)
def HTTP_PORT = getHTTPPort(env.BRANCH_NAME)
def POETRY_VERSION = "1.8.2"
def EMAIL_RECIPIENTS = "franckafosoule@gmail.com"


properties([
  parameters([
    choice(
      name: 'PYTHON',
      description: 'Choose Python version',
      choices: ["3.12", "3.11", "3.10"].join("\n"),
    ),
    base64File(
      name: 'REQUIREMENTS_FILE',
      description: 'Upload requirements file (Optional)'
    )
  ])
])


pipeline {
    environment {
        AWS_DEFAULT_REGION="eu-west-3"
        DOCKERHUB_ID = "fafosoule"
        dockerHome = tool "DockerLocalhost"
        pysonarCredential = credentials('sonarqubeToken')
        PATH = "$dockerHome/bin:$PATH"
        ADMIN_EMAIL = "franckafosoule@gmail.com"
        APP_VERSION = "0.1.0"
        API_PATH_VERSION_PREFIX = "/api/v1"
        DYNAMODB_URL = 'http://localhost:8000'
        ALLOWED_ORIGINS ='http://localhost:4200,http://localhost:4000'
        TABLE_NAME = "accounting-erp-${ENV_NAME}"
    }
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        timeout(time: 60, unit:'MINUTES')
        timestamps()
    }
    stages {
        stage("Initialize") {
            steps {
                script {
                    echo "${BUILD_NUMBER} - ${env.BUILD_ID} on ${env.JENKINS_URL}"
                    echo "Branch Specifier :: ${env.BRANCH_NAME}"
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -la'
            }
        }

        stage('Make Virtual Env and run the Test') {
            steps {
                withPythonEnv("/usr/bin/python${params.PYTHON}") {
                    script {
                        poetryConfigAndInstall(params.PYTHON, POETRY_VERSION, WORKSPACE)
                        populateAppEnvVariables(WORKSPACE)
                        sh "poetry run pytest -v --cov=./ --cov-report=xml"
                    }
                }
            }
        }

        stage("Sonarqube Analysis"){
            steps{
                withPythonEnv("/usr/bin/python${params.PYTHON}") {
                    script {
                        def sonarqubeScannerHome = tool 'sonarqubeScanner'
                        echo "SonarQube Scanner installation directory: ${sonarqubeScannerHome}"
                        withSonarQubeEnv('sonaqubeServer') {
                            sh "${sonarqubeScannerHome}/bin/sonar-scanner"
                        }
                        timeout(time: 1, unit: 'MINUTES') {
                            def wfqg = waitForQualityGate()
                            if (wfqg.status != 'OK') {
                                error "Pipeline aborted due to quality gate failure: ${wfqg.status}"
                            }
                        }
                    }
                }
            }
        }

        stage('Image Prune') {
            steps {
                script {
                    imagePrune(CONTAINER_NAME, DOCKERHUB_ID)
                }
            }
        }

        stage ('Build Python FAstAPI Image and Push It to DockerHUB') {
            steps {
                script {
                    docker.withRegistry('', 'DOCKERHUB_CREDENTIAL') {
                        def dockerImage = docker.build("${DOCKERHUB_ID}/${CONTAINER_NAME}:${CONTAINER_TAG}", 
                            "--network=host --pull --no-cache .")
                        dockerImage.push();
                        dockerImage.push('latest');
                    }
                }
            }
        }

        stage('Run App') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'DOCKERHUB_CREDENTIAL', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        imagePrune(CONTAINER_NAME, DOCKERHUB_ID)
                        //runApp(CONTAINER_NAME, CONTAINER_TAG, USERNAME, HTTP_PORT)
                        
                        sh "docker pull  ${USERNAME}/${CONTAINER_NAME}:${CONTAINER_TAG}"
                        sh "docker run \
                            --name ${USERNAME}-${CONTAINER_NAME}  \
                            --rm \
                            -d \
                            -e ALLOWED_ORIGINS=${ALLOWED_ORIGINS} \
                            -e DYNAMODB_URL=${DYNAMODB_URL}  \
                            -e TABLE_NAME=${TABLE_NAME} \
                            -e VERSION=${APP_VERSION} \
                            -e API_PATH_VERSION_PREFIX=${API_PATH_VERSION_PREFIX} \
                            -e APP_ENVIRONMENT=${ENV_NAME} \
                            -e ADMIN_EMAIL=${ADMIN_EMAIL} \
                            -p ${HTTP_PORT}:${HTTP_PORT} \
                            ${USERNAME}/${CONTAINER_NAME}:${CONTAINER_TAG}"
                        echo "Application started on port:  ${HTTP_PORT} (http)"
                    }
                }
            }
        }
    }
    post {
        always {
            echo 'Backend FAstAPI build'
        }
        success {
            echo 'Backend FAstAPI build Done Successfully'
        }
        failure {
            echo 'Backend FAstAPI build Done with failure'
        }
    }
}



def populateAppEnvVariables(workspace) {
    sh "envsubst < $workspace/.env.temp > $workspace/.env"
}

def poetryConfigAndInstall(pythonVersion, poetryVersion, workspace) {
    sh "pip$pythonVersion install poetry==$poetryVersion \
        && poetry config virtualenvs.in-project true \
        && poetry config virtualenvs.path $workspace \
        && poetry install --no-root --no-ansi --no-interaction"
    
    echo "Show poetry env configs"
    sh "poetry env list"
    sh "poetry env info"
    sh "poetry config --list"
}

def imagePrune(containerName, dockerHubUser) {
    try {
        sh "docker system prune -f -a"
        sh "docker stop $dockerHubUser-$containerName"
    } catch (ignored) {}
}


def sendEmail(recipients) {
    mail(
        to: recipients,
        subject: "Build ${env.BUILD_NUMBER} - ${currentBuild.currentResult} - (${currentBuild.fullDisplayNames})",
        body: "Check console output at: ${env.BUILD_URL}/console" + "\n"
    )
}

String getEnvName(branchName) {
    if (branchName == 'main') {
        return 'prod'
    }
    return (branchName == 'develop') ? 'uat' : 'dev'
}

String getHTTPPort(branchName) {
    if (branchName == 'main') {
        return '8080'
    }
    return (branchName == 'develop') ? '8082' : '8083'
}

String getTag(builderNumber, branchName) {
    if (branchName == 'main') {
        return builderNumber + '-stable'
    }
    return builderNumber + '-unstable'
}
