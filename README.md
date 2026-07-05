GIT Url : https://github.com/Ashish111279/Flask-application.git

EC2 instance created for Jenkins installation]
 
 
sudo apt update -y
sudo apt upgrade -y
 
sudo apt install openjdk-17-jdk -y
 
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
 

sudo apt update -y
sudo apt install -y Jenkins

 
 



Jenkins File :

pipeline {
  agent any

  environment {
    RECIPIENTS = 'devops-team@example.com'
  }

  stages {
    stage('Build') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'python -m pip install -r requirements.txt'
        sh 'python -m pip install -r requirements-dev.txt'
      }
    }

    stage('Test') {
      steps {
        sh 'pytest --maxfail=1 --disable-warnings -q'
      }
    }

    stage('Deploy') {
      when {
        branch 'main'
      }
      steps {
        sh 'bash scripts/deploy_staging.sh'
      }
    }
  }

  post {
    success {
      mail to: "${RECIPIENTS}",
           subject: "Jenkins: Build Successful - ${JOB_NAME} #${BUILD_NUMBER}",
           body: "The Jenkins pipeline completed successfully.\nJob: ${JOB_NAME}\nBuild: ${BUILD_NUMBER}\nURL: ${BUILD_URL}"
    }
    failure {
      mail to: "${RECIPIENTS}",
           subject: "Jenkins: Build Failed - ${JOB_NAME} #${BUILD_NUMBER}",
           body: "The Jenkins pipeline failed.\nJob: ${JOB_NAME}\nBuild: ${BUILD_NUMBER}\nURL: ${BUILD_URL}"
    }
  }
}

Local Host url : http://localhost:5000/ui
 
 

 
 
 
 
