@Library('mbl-jenkins-library@master') _
 

pipeline {
    agent any

    stages {
        stage("checkout") {
            steps {
                checkout scm
            }
        }
        stage("sanity-check") {
            steps {
                sanityCheckPipeline {
                    credentialsId = "fc6db1f7-2a3f-4655-b54a-476bac1194e5"
                }
            }
        }
        stage("run-tests") {
            steps{
                dir("${WORKSPACE}/tests/") {
                    echo "Running tests."
                    sh "./run-tests.sh"
                    sh "cp ./report ${WORKSPACE}/report.xml"
                }
            }
        }
        stage("build-wheel") {
            when { tag "*" }
            steps {
                echo "Building wheel."
                sh "./build-wheel.sh"
            }           
        }
        stage("deploy-to-pypi") {
            when { tag "*" }
            steps {
                echo "Uploading to pypi."
                sh "twine ${WORKSPACE}/dist/*"
            }
        }
    }

    post {
        always {
            junit "report.xml"
            archiveArtifacts allowEmptyArchive: true, artifacts: "${WORKSPACE}/dist/*whl", fingerprint: true
        }
        failure {
            mail to: "rob.walton@arm.com", subject: "The Pipeline failed.", body: "Build failed."
        }
    }
}