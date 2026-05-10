# Kittygram API

Kittygram API — серверная часть учебного проекта на Django REST Framework.

Проект реализует API для работы с котиками, достижениями, котоблогом, комментариями, сезонными событиями и рейтингом пользователей.

## Стек технологий

- Python 3.12
- Django 4.2
- Django REST Framework
- Djoser
- Simple JWT
- django-filter
- drf-yasg
- PostgreSQL
- SQLite
- Docker
- Docker Compose
- Gunicorn
- Nginx

## Функциональность

### Kittygram

- Регистрация и JWT-аутентификация пользователей.
- Создание, просмотр, изменение и удаление котиков.
- Добавление достижений котикам.
- Поиск, фильтрация, сортировка и пагинация.

### Котоблог

- Создание постов про котиков.
- Просмотр списка и детальной страницы поста.
- Добавление комментариев.
- Модерация комментариев.
- Публикация и скрытие постов.

### Сезонные события и рейтинг

- Создание сезонов.
- Активация сезона.
- Начисление очков пользователям.
- Просмотр результатов и таблицы лидеров.

## Структура проекта

```text
kittygram_course/
├── api/                  # API-роуты, viewsets, permissions, pagination
├── blog/                 # Посты и комментарии котоблога
├── cats/                 # Котики и достижения
├── seasons/              # Сезоны, очки и рейтинг
├── kittygram/            # Настройки Django-проекта
├── infra/                # Конфигурация Nginx
│   └── nginx.conf
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .env.docker.example
└── manage.py
```

## Развертывание через Docker

Docker-запуск является основным способом проверки проекта.

Контейнеры:

- `kittygram_db` — PostgreSQL;
- `kittygram_backend` — Django + Gunicorn;
- `kittygram_gateway` — Nginx.

### 1. Требования

Перед запуском должны быть установлены:

- Git;
- Docker;
- Docker Compose.

Проверка установки:

```bash
git --version
docker --version
docker compose version
```

### 2. Клонирование проекта

```bash
git clone https://github.com/USERNAME/kittygram-course.git
cd kittygram-course
```

Вместо `USERNAME` нужно указать имя аккаунта GitHub.

### 3. Подготовка переменных окружения

Создать файл `.env.docker` на основе примера.

Для Windows:

```bash
copy .env.docker.example .env.docker
```

Для Linux/macOS:

```bash
cp .env.docker.example .env.docker
```

Пример содержимого `.env.docker`:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

USE_POSTGRES=True
POSTGRES_DB=kittygram
POSTGRES_USER=kittygram_user
POSTGRES_PASSWORD=kittygram_password
DB_HOST=db
DB_PORT=5432
```

Для учебного запуска значения можно оставить. Для реального сервера нужно заменить `SECRET_KEY`, указать `DEBUG=False` и добавить домен или IP-адрес сервера в `ALLOWED_HOSTS`.

### 4. Сборка и запуск проекта

```bash
docker compose up --build
```

При запуске backend автоматически выполнит миграции, соберет static-файлы и запустит Gunicorn.

После запуска проект доступен по адресу:

```text
http://127.0.0.1:8000/
```

Проверочные адреса:

```text
http://127.0.0.1:8000/api/cats/
http://127.0.0.1:8000/api/blog/posts/
http://127.0.0.1:8000/api/seasons/
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```

Если API возвращает `HTTP 200 OK`, проект развернут успешно.

### 5. Создание суперпользователя

Открыть второй терминал в папке проекта и выполнить:

```bash
docker compose exec backend python manage.py createsuperuser
```

Пример данных для проверки:

```text
Username: admin
Email address: admin@mail.ru
Password: admin1234
```

Если Django предупредит о простом пароле, можно подтвердить создание пользователя.

### 6. Получение JWT-токена

Endpoint:

```http
POST /auth/jwt/create/
```

Тело запроса:

```json
{
  "username": "admin",
  "password": "admin1234"
}
```

Пример через PowerShell:

```powershell
$body = @{
    username = "admin"
    password = "admin1234"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/jwt/create/" -Method POST -ContentType "application/json" -Body $body

$token = $response.access
```

Для защищенных запросов используется заголовок:

```http
Authorization: Bearer <access_token>
```

## Проверка API

### Создание котика

```powershell
$cat = @{
    name = "Barsik"
    color = "ginger"
    birth_year = 2021
    description = "Likes sleeping on the laptop"
    achievements = @(
        @{ name = "Caught a mouse" },
        @{ name = "Woke up the owner" }
    )
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/cats/" -Method POST -ContentType "application/json" -Headers @{Authorization = "Bearer $token"} -Body $cat
```

Проверить список котиков:

```text
http://127.0.0.1:8000/api/cats/
```

### Создание поста котоблога

Если котик имеет `id = 1`:

```powershell
$post = @{
    cat = 1
    title = "Barsik docker blog story"
    text = "This post was created inside Docker with PostgreSQL, Gunicorn and Nginx."
    is_published = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/blog/posts/" -Method POST -ContentType "application/json" -Headers @{Authorization = "Bearer $token"} -Body $post
```

Проверить список постов:

```text
http://127.0.0.1:8000/api/blog/posts/
```

### Добавление комментария

Если пост имеет `id = 1`:

```powershell
$comment = @{
    text = "Docker comment for Barsik blog post."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/blog/posts/1/comments/" -Method POST -ContentType "application/json" -Headers @{Authorization = "Bearer $token"} -Body $comment
```

Проверить детальную страницу поста:

```text
http://127.0.0.1:8000/api/blog/posts/1/
```

### Создание сезона

```powershell
$season = @{
    title = "Spring Kitty Season"
    description = "Season event for active Kittygram users."
    start_date = "2026-05-01"
    end_date = "2026-05-31"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/seasons/" -Method POST -ContentType "application/json" -Headers @{Authorization = "Bearer $token"} -Body $season
```

Проверить список сезонов:

```text
http://127.0.0.1:8000/api/seasons/
```

### Активация сезона

Если сезон имеет `id = 1`:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/seasons/1/activate/" -Method POST -Headers @{Authorization = "Bearer $token"}
```

### Начисление очков пользователю

Если пользователь имеет `id = 1`:

```powershell
$points = @{
    user = 1
    points = 25
    action = "Published cat activity during season"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/seasons/1/add_points/" -Method POST -ContentType "application/json" -Headers @{Authorization = "Bearer $token"} -Body $points
```

### Таблица лидеров

```text
http://127.0.0.1:8000/api/seasons/1/leaderboard/
```

### Проверка ошибки валидации

Нельзя начислить больше 100 очков за одно действие:

```powershell
$badPoints = @{
    user = 1
    points = 150
    action = "Too many points"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/seasons/1/add_points/" -Method POST -ContentType "application/json" -Headers @{Authorization = "Bearer $token"} -Body $badPoints
```

Ожидаемый ответ:

```json
{
  "points": [
    "Ensure this value is less than or equal to 100."
  ]
}
```

## Документация API

Swagger:

```text
http://127.0.0.1:8000/swagger/
```

ReDoc:

```text
http://127.0.0.1:8000/redoc/
```

## Фильтрация, поиск и пагинация

Примеры запросов:

```text
/api/cats/?search=Barsik
/api/cats/?color=ginger
/api/cats/?limit=1
/api/blog/posts/?search=Barsik
/api/blog/posts/?limit=1
/api/seasons/?search=Spring
/api/seasons/?is_active=true
/api/seasons/1/leaderboard/?limit=10
```

## Остановка проекта

Остановить контейнеры:

```bash
docker compose down
```

Остановить контейнеры и удалить данные PostgreSQL:

```bash
docker compose down -v
```

Команда `docker compose down -v` удаляет volume с базой данных. После нее созданные пользователи, котики, посты, комментарии, сезоны и результаты будут удалены.

## Повторный запуск

Если проект уже был собран ранее:

```bash
docker compose up
```

Если изменялись зависимости или настройки Docker:

```bash
docker compose up --build
```

## Полезные команды

Выполнить миграции вручную:

```bash
docker compose exec backend python manage.py migrate
```

Собрать static-файлы вручную:

```bash
docker compose exec backend python manage.py collectstatic --noinput
```

Посмотреть логи всех контейнеров:

```bash
docker compose logs
```

Посмотреть логи backend:

```bash
docker compose logs backend
```

Проверить состояние контейнеров:

```bash
docker compose ps
```

## Возможные ошибки

### Порт 8000 занят

Остановить другой сервер или изменить порт в `docker-compose.yml`:

```yaml
ports:
  - "8001:80"
```

После этого проект будет доступен по адресу:

```text
http://127.0.0.1:8001/
```

### 502 Bad Gateway

Nginx запустился, но backend еще не готов или упал.

Проверить логи backend:

```bash
docker compose logs backend
```

Перезапустить backend:

```bash
docker compose restart backend
```

### JWT token invalid or expired

Access-токен устарел. Нужно заново получить токен через:

```text
POST /auth/jwt/create/
```

### Нет данных после Docker-запуска

Docker использует PostgreSQL, а локальный запуск без Docker использует SQLite. Это разные базы данных.  
Нужно создать суперпользователя и тестовые данные внутри Docker-запуска.