# Простая система задач (FastAPI)

В этом репозитории находится минимальное API для управления задачами, реализованное с использованием FastAPI. Оно поддерживает создание, получение, выполнение, отмену выполнения и удаление задач с автоматической генерацией ID и времени создания.

## Функционал

- **GET** `/tasks` — получить все задачи
- **GET** `/tasks/pending` — получить только задачи со статусом `pending`
- **GET** `/tasks/{task_id}` — получить задачу по её UUID
- **POST** `/tasks` — создать новую задачу (ID, статус и метка времени генерируются автоматически)
- **POST** `/tasks/{task_id}/complete` — пометить задачу как выполненную (`done`)
- **POST** `/tasks/{task_id}/uncomplete` — вернуть задаче статус `pending`
- **DELETE** `/tasks/{task_id}` — удалить задачу по её UUID

## Требования к окружению

Предполагается, что разработка и запуск происходят на **Ubuntu Linux 24.04 LTS** с минимальной стандартной установкой.

- **Python** версии **3.10** или выше (рекомендуется 3.11)
- **pip** — менеджер пакетов для Python
- **virtualenv** (рекомендуется для изоляции окружения)


## Установка и настройка

### Ubuntu Linux 24.04 LTS

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-org/fastapi-task-manager.git
   cd fastapi-task-manager
   ```

2. (Опционально) Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Обновите pip и установите зависимости:
   ```bash
   pip install --upgrade pip
   pip install fastapi uvicorn pydantic
   ```

### Windows 10/11

1. Клонируйте репозиторий:
   ```powershell
   git clone https://github.com/your-org/fastapi-task-manager.git
   cd fastapi-task-manager
   ```

2. Создайте и активируйте виртуальное окружение:
   ```powershell
   python -m venv venv
   venv\Scripts\activate  # для CMD
   ```

3. Обновите pip и установите зависимости:
   ```powershell
   pip install fastapi uvicorn pydantic
   ```

## Запуск приложения

```bash
uvicorn main:app --reload --port 8000
```

- Сервер будет доступен по адресу: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Примеры использования

### Создание задачи
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
      "title": "Написать тесты",
      "description": "Добавить unit-тесты",
      "priority": 3
  }'
```

### Пометить задачу как выполненную
```bash
curl -X POST http://127.0.0.1:8000/tasks/<TASK_UUID>/complete
```

### Вернуть задачу обратно в состояние pending
```bash
curl -X POST http://127.0.0.1:8000/tasks/<TASK_UUID>/uncomplete
```

### Удаление задачи
```bash
curl -X DELETE http://127.0.0.1:8000/tasks/<TASK_UUID>
```

## Обоснование дополнительных эндпоинтов

В дополнение к исходному ТЗ были добавлены следующие ручки для обеспечения удобства и целостности API:

- **POST /tasks/{task_id}/complete**: явно помечает задачу как выполненную (`done`).
- **POST /tasks/{task_id}/uncomplete**: возвращает задаче статус `pending`, что даёт возможность корректировать ошибочный статус.

Без этих эндпоинтов эндпоинт get tasks pending не имела бы смысл, так как без изменения статуса задачи получение невыполненных задач ничем не отличается от получения всех задач

