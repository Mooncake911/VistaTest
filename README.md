### Diary Backend API (FastAPI)

Простое backend‑приложение «Ежедневник» на Python + FastAPI + SQLAlchemy с поддержкой PostgreSQL (по умолчанию). Реализованы операции:

- Создать запись
- Прочитать запись по ID
- Обновить запись
- Удалить запись
- Просмотреть список записей (пагинация + фильтр по статусу выполнения)
- Пометить запись «выполненной» (is_completed)

Приложение можно запустить локально и развернуть на любом хостинге. В репозитории также приведены инструкции по настройке.

---

#### Стек

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL (по умолчанию). Можно использовать SQLite.
- Uvicorn
- python-dotenv (для переменных окружения)

---

#### Структура проекта

```
app/
  crud/            # CRUD-операции
  models/          # SQLAlchemy модели
  routers/         # FastAPI роутеры (эндпоинты)
  schemas/         # Pydantic-схемы запросов/ответов
  database.py      # Подключение к БД, Session, Base
  main.py          # Точка входа FastAPI
pyproject.toml     # Зависимости и метаданные проекта
README.md          # Документация проекта
```

---

#### Установка и запуск

1) Клонируйте репозиторий и перейдите в каталог проекта.

2) Установите зависимости (пример для uv/pip):

- pip (Python 3.12+):
  - python -m venv .venv
  - .venv\\Scripts\\activate
  - pip install -U pip
  - pip install -e .

- либо с uv (если установлен):
  - uv sync

3) Настройте переменные окружения. Создайте файл .env в корне с содержимым:

```
DATABASE_URL=postgresql://user:password@localhost:5432/diary_db
```

4) Запустите сервер разработки:

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Документация будет доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

При старте приложения таблицы создаются автоматически (демо-подход без миграций).

---

#### Эндпоинты

Базовый URL: http://localhost:8000

- GET / — корневой эндпоинт
- GET /health — проверка состояния
- POST /entries — создать запись
- GET /entries — список записей (параметры: skip=0, limit=100, completed=true/false)
- GET /entries/{id} — получить запись по ID
- PUT /entries/{id} — обновить запись
- DELETE /entries/{id} — удалить запись
- PATCH /entries/{id}/complete — изменить статус выполнения

Схемы:
- DiaryEntryCreate: { title: string, content: string }
- DiaryEntryUpdate: { title?: string, content?: string }
- DiaryEntryCompleteToggle: { is_completed: boolean }

---

#### Примеры запросов (curl)

Создать запись:
```
curl -X POST http://localhost:8000/entries \
  -H "Content-Type: application/json" \
  -d '{"title": "Моя запись", "content": "Содержание"}'
```

Получить список записей (только выполненные):
```
curl "http://localhost:8000/entries?completed=true&skip=0&limit=50"
```

Обновить запись:
```
curl -X PUT http://localhost:8000/entries/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Обновлённый заголовок"}'
```

Пометить запись как выполненную:
```
curl -X PATCH http://localhost:8000/entries/1/complete \
  -H "Content-Type: application/json" \
  -d '{"is_completed": true}'
```

Удалить запись:
```
curl -X DELETE http://localhost:8000/entries/1
```

---
