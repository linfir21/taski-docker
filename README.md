# Taski — сервис для создания задач

Пет-проект-учебный сервис для управления списком задач (todo-лист): пользователь может создавать, редактировать и удалять задачи, отмечать их выполненными.

## Стек технологий

- **Backend:** Python 3.12, Django, Django REST Framework, Gunicorn
- **Frontend:** React 18, Bootstrap, Reactstrap, Axios
- **База данных:** PostgreSQL 13
- **Веб-сервер / шлюз:** Nginx
- **Контейнеризация:** Docker, Docker Compose
- **CI/CD:** GitHub Actions (flake8, Django-тесты, пуш образов в DockerHub, деплой на сервер по SSH, уведомление в Telegram)

## Архитектура проекта

```
├── backend/          # Django-приложение (API задач)
│   ├── api/          # Приложение: модель Task, views, serializers
│   ├── backend/      # Настройки Django, urls, wsgi
│   └── Dockerfile
├── frontend/         # React-приложение (интерфейс задач)
│   └── Dockerfile
├── gateway/          # Nginx-шлюз (маршрутизация /api, /admin, /static)
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml              # Локальный запуск
├── docker-compose.production.yml   # Продакшн-запуск (готовые образы)
└── .github/workflows/main.yml      # CI/CD пайплайн
```

Работу контейнеров обслуживает Nginx-шлюз:
- `/api/` → проксирование на backend;
- `/admin/` → панель администратора Django;
- `/static/` → статика (раздаёт из общего volume);
- `/` → статика React-приложения.

## Запуск локально

1. Создайте файл `.env` в корне проекта:

```env
POSTGRES_DB=taski
POSTGRES_USER=taski_user
POSTGRES_PASSWORD=taski_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost,backend
```

2. Запустите все контейнеры:

```bash
docker compose up
```

3. Приложение будет доступно по адресу: http://127.0.0.1:8000

При первом запуске выполните миграции:

```bash
docker compose exec backend python manage.py migrate
```

## Запуск в продакшне

Файл `docker-compose.production.yml` использует готовые образы из DockerHub и запускается на удалённом сервере:

```bash
docker compose -f docker-compose.production.yml up -d
```

## CI/CD

При пуше в ветку `main` GitHub Actions автоматически:

1. Запускает `flake8` и юнит-тесты Django (приложен поднимается тестовый PostgreSQL).
2. Собирает и публикует в DockerHub три образа: `taski_backend`, `taski_frontend`, `taski_gateway`.
3. Подключается к продакшн-серверу по SSH, обновляет `docker-compose.production.yml`, скачивает свежие образы и перезапускает контейнеры.
4. Выполняет миграции и собирает статику.
5. Отправляет уведомление о результате деплоя в Telegram.

Для работы пайплайна нужны секреты в настройках репозитория:

- `DOCKER_USERNAME`, `DOCKER_PASSWORD` — доступ к DockerHub;
- `HOST`, `USER`, `SSH_KEY` — доступ к серверу по SSH;
- `TELEGRAM_TO`, `TELEGRAM_TOKEN` — Telegram-уведомления.

## Автор

[linfir21](https://github.com/linfir21)
