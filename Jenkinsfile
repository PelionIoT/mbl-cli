pipeline {
    agent any

    environment {
        MBLTOOLSDIR = "${pwd(tmp:true)}"
    }

    stages {
        stage("checkout") {
            steps {
                checkout scm
            }
        }
        stage("sanity-check") {
            steps {
                dir("${MBLTOOLSDIR}") {
                    git url: "git@github.com:armmbed/mbl-tools", credentialsId: "fc6db1f7-2a3f-4655-b54a-476bac1194e5"
                }

                sh "${MBLTOOLSDIR}/ci/sanity-check/run-me.sh --no-tty \
                    --workdir ${WORKSPACE}/mbl/cli"
            }
        }
        stage("run-tests") {
            steps{
                dir("${WORKSPACE}/tests/") {
                    echo "Running tests."
                    sh "./run-tests.sh"
                    mv "./report" "${WORKSPACE}/report.xml"
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
            when { tag "*" }
            archiveArtifacts allowEmptyArchive: true, artifacts: "${WORKSPACE}/dist/*whl", fingerprint: true
        }
        failure {
            mail to: "rob.walton@arm.com", subject: "The Pipeline failed.", body: "Build failed."
        }
    }
}