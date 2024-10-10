def ENV_NAME = getEnvName(env.BRANCH_NAME)
def CONTAINER_NAME = "accountings-api-" + ENV_NAME
def CONTAINER_TAG = getTag(env.BUILD_NUMBER, env.BRANCH_NAME)
def HTTP_PORT = getHTTPPort(env.BRANCH_NAME)
def EMAIL_RECIPIENTS = "franckafosoule@gmail.com"
def POETRY_VERSION = "1.8.2"
def APP_VERSION = "0.1.0"
def PROJECT_NAME = "stam-haen-api-" + ENV_NAME


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
                    imagePrune(CONTAINER_NAME)
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
                        imagePrune(CONTAINER_NAME)
                        runApp(CONTAINER_NAME, CONTAINER_TAG, USERNAME, HTTP_PORT, ENV_NAME, PROJECT_NAME, APP_VERSION)
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

def imagePrune(containerName) {
    try {
        sh "docker system prune -f -a"
        sh "docker stop $containerName"
    } catch (ignored) {}
}

// Not using this
def imageBuild(containerName, tag) {
    sh "docker build -t $containerName:$tag -t $containerName --pull --no-cache ."
    echo "Image build complete"
}

// Not using this
def pushToImage(containerName, tag, dockerUser, dockerPassword) {
    sh "docker login -u $dockerUser -p $dockerPassword"
    sh "docker tag $containerName:$tag $dockerUser/$containerName:$tag"
    sh "docker push $dockerUser/$containerName:$tag"
    echo "Image push complete"
}

def runApp(containerName, tag, dockerHubUser, httpPort, envName, projectName, version) {
    sh "docker pull  $dockerHubUser/$containerName:$tag"
    sh "docker run \
        --name $dockerHubUser-$containerName  \
        --rm \
        -d \
        -e APP_ENVIRONMENT=$envName  \
        -e ALLOWED_ORIGINS='http://localhost:4200,http://localhost:4000'  \
        -e DYNAMODB_URL='http://localhost:8000'  \
        -e TABLE_NAME=accounting-erp-$envName  \
        -e PROJECT_NAME=$projectName  \
        -e VERSION=$version \
        -p $httpPort:$httpPort \
        $dockerHubUser/$containerName:$tag"
    echo "Application started on port:  $httpPort (http)"
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
