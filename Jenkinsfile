def CONTAINER_NAME = "accountings API"
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
      choices: ["python3.10", "python3.11", "python3.12"].join("\n"),
    ),
    base64File(
      name: 'REQUIREMENTS_FILE',
      description: 'Upload requirements file (Optional)'
    )
  ])
])


pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
    timeout(time: 60, unit:'MINUTES')
    timestamps()
  }
  stages {

    stage('Make Virtual Env') {
        steps {
            withPythonEnv("/usr/bin/${params.PYTHON}") {
                sh "pip install poetry==${POETRY_VERSION} \
                    && poetry config virtualenvs.in-project true \
                    && poetry install --no-root --no-ansi --no-interaction"
                
                sh "poetry --version"
            }
        }
    }

    stage("Python with python env"){
      steps{
        withPythonEnv("/usr/bin/${params.PYTHON}") {
          script {
            sh "poetry --version"
          }
        }
      }
    }
  }
}


/*
pipeline {
    environment {
        dockerHome = tool "DockerLocalhost"
        PATH = "$dockerHome/bin:$PATH"
    }
    agent any
    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python version') {
            steps {
                echo "python --version"
            }
        }

        stage('Make Virtual Env') {
            steps {
                withPythonEnv('/usr/bin/python3.12') {
                    sh "pip install poetry==${POETRY_VERSION} && poetry config virtualenvs.in-project true && poetry install --no-root --no-ansi --no-interactio"
                    
                    sh "poetry --version"
                }
            }
        }

        stage('test poetry with pyenvt') {
            steps {
                withPythonEnv('/usr/bin/python3.12') {
                    sh "poetry --version"
                }
            }
        }

        stage('test poetry without pyenvt') {
            steps {
                sh "poetry --version"
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
*/