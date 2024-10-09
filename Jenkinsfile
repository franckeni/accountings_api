def CONTAINER_NAME = "accountings-API"
def ENV_NAME = getEnvName(env.BRANCH_NAME)
def CONTAINER_TAG = getTag(env.BUILD_NUMBER, env.BRANCH_NAME)
def HTTP_PORT = getHTTPPort(env.BRANCH_NAME)
def EMAIL_RECIPIENTS = "franckafosoule@gmail.com"
def POETRY_VERSION = "1.8.2"


//DOCKERHUB_CREDENTIAL
//MavenLocalhost
properties([
  parameters([
    choice(
      name: 'PYTHON',
      description: 'Choose Python version',
      defaultValue: "python3.12",
      choices: ["python3.12", "python3.11", "python3.10"].join("\n"),
    ),
    base64File(
      name: 'REQUIREMENTS_FILE',
      description: 'Upload requirements file (Optional)'
    )
  ])
])


pipeline {
    environment {
        DOCKERHUB_ID = "fafosoule"
        dockerHome = tool "DockerLocalhost"
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
                sh 'ls -lah'
            }
        }

        stage('Make Virtual Env and Test') {
            steps {
                withPythonEnv("/usr/bin/${params.PYTHON}") {
                    script {
                        updateUpgradeInstallPackages()
                        createVirtualEnvironment()
                        poetryConfigAndInstall(params.PYTHON, POETRY_VERSION)
                        populateAppEnvVariables(WORKSPACE)
                        //runTest()
                    }
                }
            }
        }

        stage("Sonarqube Analysis"){
            steps{
                withPythonEnv("/usr/bin/${params.PYTHON}") {
                    script {
                        withSonarQubeEnv('sonaqubeServer') {
                            sh "pysonar-scanner"
                        }
                        timeout(time: 1, unit: 'MINUTES') {
                            def qq = waitForQualityGate()
                            if (qq.status != 'OK') {
                                error "Pipeline aborted due to quality gate failure: ${qq.status}"
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

        /*stage ('Build Python FAstAPI Image and Push It to DockerHUB') {
            steps {
                script {
                    docker.withRegistry('', 'DOCKERHUB_CREDENTIAL') {
                        def dockerImage = docker.build("${DOCKERHUB_ID}/${CONTAINER_NAME}:${TAG}", 
                            "--network=host --pull --no-cache")
                        dockerImage.push();
                        dockerImage.push('latest');
                    }
                }
            }
        }

        stage('Run App') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhubcredentials', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        runApp(CONTAINER_NAME, CONTAINER_TAG, USERNAME, HTTP_PORT, ENV_NAME)
                    }
                }
            }
        }*/
    }
}

def runTest() {
    sh "poetry run pytest test/e2e/test.py test/unit/test.py test/integration/test.py --cov=./ --cov-report=xml"
}

def createVirtualEnvironment() {
    sh "python -m venv venv && source venv/bin/activate"
}

def updateUpgradeInstallPackages() {
    sh "apt-get update && apt-get upgrade -y"
}

def populateAppEnvVariables(workspace) {
    sh "envsubst < $workspace/.env.temp > $workspace/.env"
}

def poetryConfigAndInstall(pythonVersion, poetryVersion) {
    sh "pip$pythonVersion install poetry==$poetryVersion \
        && poetry config virtualenvs.in-project false \
        && poetry install --no-root --no-ansi --no-interaction"
    sh "poetry env list"
    sh "poetry env info"
    sh "poetry config --list"
}

def imagePrune(containerName) {
    try {
        sh "docker image prune -f"
        sh "docker stop $containerName"
    } catch (ignored) {}
}

def imageBuild(containerName, tag) {
    sh "docker build -t $containerName:$tag -t $containerName --pull --no-cache ."
    echo "Image build complete"
}

def pushToImage(containerName, tag, dockerUser, dockerPassword) {
    sh "docker login -u $dockerUser -p $dockerPassword"
    sh "docker tag $containerName:$tag $dockerUser/$containerName:$tag"
    sh "docker push $dockerUser/$containerName:$tag"
    echo "Image push complete"
}

def runApp(containerName, tag, dockerHubUser, httpPort, envName) {
    sh "docker pull  $dockerHubUser/$containerName"
    sh "docker run --rm --env SPRING_ACTIVE_PROFILES=$envName -d -p $httpPort:$httpPort --name $containerName $dockerHubUser/$containerName:$tag"
    echo "Application started on port:  ${httpPort} (http)"
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
