# AI-Service

RAG (Retrieval-Augmented Generation) сервис для для подбора идеального Python фреймворка под запрос пользователя.

## Установка проекта:

1. **Клонируйте проект и перейдите в каталог с ним:**
   ```bash
   git clone git@github.com:Baklachok/AI-Service.git
   cd AI-Service
   ```

## Запуск сервиса:

1. **Выполните следующие действия в терминале в папке проекта:**
   - Собираем проект в докере:
     ```bash
     docker-compose up -d --build
     ```
     

## Запуск парсера:

1. **Выполните следующие действия в терминале в папке проекта:**
   - Ручной запуск парсера:
     ```bash
     docker compose exec web python scripts/collect_frameworks.py
     ```

## Запуск препроцессинг + эмбеддинг

1. **Выполните следующие действия в терминале в папке проекта:**
   - Ручной запуск парсера:
     ```bash
     docker compose exec web python scripts/prepare_embeddings.py
     ```