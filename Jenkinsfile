pipeline {
    agent none

    options {
        timestamps()
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            agent { label 'builder' }
            steps {
                deleteDir()
                checkout scm
                sh 'echo "Checkout sur $(hostname)"'
                stash name: 'sources',
                      includes: 'app/**,tests/**,requirements*.txt,pyproject.toml,README.md'
            }
        }

        stage('Lint') {
            agent { label 'builder' }
            steps {
                sh '''
                    set -eu
                    echo "Lint sur $(hostname)"
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --disable-pip-version-check ruff
                    .venv/bin/ruff check .
                '''
            }
        }

        stage('Build') {
            agent { label 'builder' }
            steps {
                sh '''
                    set -eu
                    echo "Build sur $(hostname)"
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --disable-pip-version-check build setuptools wheel
                    .venv/bin/python -m build --wheel --no-isolation
                '''
                stash name: 'wheel', includes: 'dist/*.whl'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'dist/*.whl', fingerprint: true
                }
            }
        }

        stage('Tests') {
            agent { label 'tester' }
            steps {
                deleteDir()
                unstash 'sources'
                unstash 'wheel'
                sh '''
                    set -eu
                    echo "Tests sur $(hostname)"
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --disable-pip-version-check -r requirements-dev.txt
                    .venv/bin/python -m pip install --disable-pip-version-check dist/*.whl
                    mkdir -p reports
                    .venv/bin/python -m pytest --junitxml=reports/junit.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success { echo 'CI reussie : agents builder et tester executes.' }
        failure { echo 'CI echouee : consulter le stage en erreur.' }
    }
}
