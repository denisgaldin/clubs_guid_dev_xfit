pipeline {
    agent any

    environment {
        BASE_URL = credentials('xfit_base_url')
    }

    tools {
        allure 'allure' // Убедись, что это имя совпадает с Jenkins > Global Tool Configuration
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Получаем код из репозитория'
                checkout scm
            }
        }

        stage('Install Dependencies & Prepare') {
            steps {
                echo '🐍 Создание виртуального окружения и установка зависимостей'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    rm -rf allure-results
                '''
            }
        }

        stage('Run Tests in Order') {
            steps {
                echo '🚀 Запуск тестов по порядку с Allure-отчётом'
                sh '''
                    . .venv/bin/activate
                    pytest --alluredir=allure-results tests/test_authorization_flow.py
                    pytest --alluredir=allure-results tests/test_get_clubs_list.py
                    pytest --alluredir=allure-results tests/test_get_club_details_guid.py
                    pytest --alluredir=allure-results tests/test_get_club_not_found.py
                '''
            }
        }

        stage('Allure Report') {
            steps {
                echo '📊 Генерация Allure отчёта'
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
            echo '❌ Сборка завершилась с ошибкой'
        }
    }
}
