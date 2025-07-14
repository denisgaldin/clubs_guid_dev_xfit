pipeline {
    agent any

    environment {
        BASE_URL = credentials('xfit_base_url')
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Получаем код из репозитория'
                checkout scm
            }
        }

        stage('Install & Run Tests in Order') {
            steps {
                echo '🐍 Установка зависимостей и запуск тестов по порядку'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    echo '🧹 Очистка прошлых результатов Allure'
                    rm -rf allure-results

                    echo '🚀 Запуск тестов в заданном порядке'
                    pytest --alluredir=allure-results \
                      tests/test_authorization_flow.py \
                      tests/test_get_clubs_list.py \
                      tests/test_get_club_details_guid.py \
                      tests/test_get_club_not_found.py
                '''
            }
        }

        stage('Allure Report') {
            steps {
                echo '📊 Генерация Allure отчета'
                allure([
                    includeProperties: false,
                    jdk: '',
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            echo '🧹 Очистка окружения'
            sh 'rm -rf .venv'
        }

        failure {
            echo '❌ Ошибка: Проверить тесты и окружение'
        }
    }
}
