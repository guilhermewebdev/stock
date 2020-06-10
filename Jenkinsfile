pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker-compose -f stack.yaml build; \
                docker-compose -f stack.yaml push'
            }
        }
        stage('Test') {
            steps {
                sh 'docker-compose up -d; \
                docker-compose exec api ./manage.py test; \
                docker-compose exec client npm run test; \
                docker-compose down'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker swarm init; \
                docker stack deploy --compose-file stack.yaml stock'
            }
        }
    }
}
