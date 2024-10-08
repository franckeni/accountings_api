def CONTAINER_NAME = "accountings API"
def EMAIL_RECIPIENTS = "franckafosoule@gmail.com"
def POETRY_VERSION = "1.8.2"


//DOCKERHUB_CREDENTIAL
//MavenLocalhost


pipeline {
    agent any
    stages {
        stage('Initialize') {
            def dockerHome = tool 'DockerLocalhost'
            env.PATH = "${dockerHome}/bin:${env.PATH}"
        }

        stage('Checkout') {
            checkout scm
        }

        stage('Make Virtual Env') {
            steps {
                withPythonEnv('Python3.12') {
                    sh "pip install poetry==${POETRY_VERSION} && poetry config virtualenvs.in-project true && poetry install --no-root --no-ansi --no-interactio"
                }
            }
        }

        stage('test poetry without pyenvt') {
            sh "poetry --version"
        }

        stage('test poetry without pyenvt') {
            steps {
                withPythonEnv('Python3.12') {
                    sh "poetry --version"
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
            echo 'Backend FAstAPI build build Done with failure'
        }
    }
}

