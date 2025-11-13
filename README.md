# AI-Service

RAG (Retrieval-Augmented Generation) сервис для подбора идеального Python фреймворка под запрос пользователя.

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
2. **Создайте файл переменных окружения:**
   - Скопируйте шаблон:
     ```bash
     cp .env.example .env
     ```

## Ручной запуск парсера:

1. **Выполните следующие действия в терминале в папке проекта:**
   - Ручной запуск парсера:
     ```bash
     docker compose exec web python scripts/collect_frameworks.py
     ```

## Ручной запуск препроцессинг + эмбеддинг

1. **Выполните следующие действия в терминале в папке проекта:**
   - Ручной запуск парсера:
     ```bash
     docker compose exec web python scripts/prepare_embeddings.py
     ```
     
## Линтеры, форматировщики и тайпчекеры

Перед отправкой изменений в origin обязательно выполните все эти действия:

- используйте linter ruff с этой командой:
  ```bash
  docker exec -it robo-server ruff check --fix
  ```
- используйте форматер ruff с помощью этой команды:
  ```bash
  docker exec -it robo-server ruff format
  ```
- используйте mypy с помощью этой команды:
  ```bash
  docker exec -it robo-server mypy .
  ```

Если найдены ошибки, исправьте их в своей ветке фич. После исправления всех ошибок
вы готовы делать commit и push.