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
      choices: ["python3.10", "python3.11", "python3.12"].join("\n")
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
    stage("Python"){
      steps{
        withPythonEnv("/usr/bin/${params.PYTHON}") {
          script {
            if ( env.REQUIREMENTS_FILE.isEmpty() ) {
              sh "python --version"
              sh "pip --version"
              sh "echo Requirements file not set. Run Python without requirements file."
            }
            else {
              sh "python --version"
              sh "pip --version"
              sh "echo Requirements file found. Run PIP install using requirements file."
              withFileParameter('REQUIREMENTS_FILE') {
                sh 'cat $REQUIREMENTS_FILE > requirements.txt'
              }
              sh "pip install -r requirements.txt"
            }
          }
        }
      }
    }
  }
}
