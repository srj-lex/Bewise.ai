# Bewise.ai

### Описание

Веб-приложение для получения уникальных вопросов для викторин.

### Стэк технологий
  
- Backend - Flask.
  
- ORM - SQLAlchemy

- Database - PostgreDB.

### Как запустить проект:

Клонировать репозиторий:

```
git clone git@github.com:srj-lex/Bewise.ai.git
```
Перейти в директорию с проекта:
```
cd bewise_ai
```
Переименовать .env_example в .env, при необходимости, внести изменения.

Запустить проект:
```
docker compose up
```
API будет доступно по адресу http://localhost:5000/quiz/.

### Примеры запроса к API

Для получения вопроса для викторины необходимо отправить POST-запрос с содержимым

вида {"questions_num": integer} на http://localhost:5000/quiz/.

