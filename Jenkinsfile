pipeline {
  agent any
  triggers { githubPush() } 

  environment {
    DOCKER_IMAGE   = "gulsherkhan/defect-ci-cd"
    SHORT_SHA      = "${env.GIT_COMMIT.substring(0,7)}"
    IMAGE_TAG      = "${DOCKER_IMAGE}:${SHORT_SHA}"
    LATEST_TAG     = "${DOCKER_IMAGE}:latest"
    DOCKERHUB_CRED = "dockerhub-creds"        
    ADMIN_EMAIL    = "i222637@nu.edu.pk"      
  }

  stages {
    stage("Docker Build") {
      steps {
        // Fail fast if Docker isn't available on the agent
        sh 'docker version'
        sh "docker build -t ${IMAGE_TAG} -t ${LATEST_TAG} ."
      }
    }

    stage("Docker Push") {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CRED}", usernameVariable: 'U', passwordVariable: 'P')]) {
          sh """
            echo "$P" | docker login -u "$U" --password-stdin
            docker push ${IMAGE_TAG}
            docker push ${LATEST_TAG}
            docker logout
          """
        }
      }
    }
  }

  post {
    success {
      emailext(
        to: "${ADMIN_EMAIL}",
        subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
        body: """<p>Image pushed:</p>
                 <ul>
                   <li><code>${IMAGE_TAG}</code></li>
                   <li><code>${LATEST_TAG}</code></li>
                 </ul>
                 <p>Commit: ${env.GIT_COMMIT}</p>""",
        mimeType: "text/html"
      )
    }
    failure {
      emailext(
        to: "${ADMIN_EMAIL}",
        subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
        body: "Check Jenkins console output."
      )
    }
    cleanup {
      // Only prune if Docker exists on the agent
      sh 'command -v docker >/dev/null 2>&1 && docker image prune -f || true'
    }
  }
}
