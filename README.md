# Django DRF Project Deployment Guide

## Содержание
1. [Настройка сервера](#настройка-сервера)
2. [Настройка проекта](#настройка-проекта)
3. [Настройка GitHub Actions](#настройка-github-actions)
4. [Мониторинг и обслуживание](#мониторинг-и-обслуживание)

## Настройка сервера

### 1. Подключение к серверу
```bash
ssh test-user@your-server-ip
```

### 2. Установка необходимых пакетов
```bash
# Обновление пакетов
sudo apt update
sudo apt upgrade -y

# Установка необходимых зависимостей
sudo apt install -y docker.io docker-compose git

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Настройка прав доступа к Docker
sudo chown root:docker /var/run/docker.sock
sudo chmod 666 /var/run/docker.sock

# Перезапуск Docker
sudo systemctl restart docker
```

### 3. Настройка директории проекта
```bash
# Создание директории проекта
sudo mkdir -p /var/www/django_drf_hw
sudo chown -R $USER:$USER /var/www/django_drf_hw
cd /var/www/django_drf_hw
```

### 4. Настройка SSH для GitHub Actions
```bash
# На локальном компьютере:
ssh-keygen -t rsa -b 4096 -C "github-actions"
# Сохраните приватный ключ (id_rsa) для GitHub Secrets

# На сервере:
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys
# Вставьте публичный ключ (id_rsa.pub)
chmod 600 ~/.ssh/authorized_keys
```

## Настройка проекта

### 1. Клонирование репозитория
```bash
cd /var/www/django_drf_hw
git clone https://github.com/<your-username>/django_drf_hw.git .
```

### 2. Настройка переменных окружения
```bash
# Создание и редактирование .env файла
nano .env

# Необходимые переменные окружения:
SECRET_KEY='your-secret-key'
DEBUG=False
POSTGRES_NAME=django_drf_hw
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 3. Запуск проекта
```bash
# Запуск контейнеров
docker-compose up -d --build
```

## Настройка GitHub Actions

### 1. Добавление секретов в GitHub
В репозитории перейдите в Settings -> Secrets and variables -> Actions и добавьте:
- `SERVER_HOST`: IP адрес вашего сервера
- `SERVER_USERNAME`: имя пользователя на сервере (test-user)
- `SSH_PRIVATE_KEY`: содержимое приватного SSH ключа (id_rsa)

### 2. Структура workflow
Файл `.github/workflows/main.yml` настроен на:
- Автоматический запуск тестов при push и pull request
- Автоматический деплой при push в main ветку
- Использование Docker для изоляции окружения

## Мониторинг и обслуживание

### Полезные команды
```bash
# Просмотр логов
docker-compose logs -f

# Перезапуск сервисов
docker-compose restart

# Остановка сервисов
docker-compose down

# Проверка статуса сервисов
docker-compose ps

# Очистка неиспользуемых ресурсов
docker system prune -a
```

### Обновление проекта
Автоматическое обновление происходит через GitHub Actions при push в main ветку.

Для ручного обновления:
```bash
cd /var/www/django_drf_hw
git pull origin main
docker-compose down
docker-compose up -d --build
```

### Бэкап данных
```bash
# Бэкап базы данных
docker-compose exec db pg_dump -U postgres django_drf_hw > backup.sql

# Восстановление базы данных
docker-compose exec db psql -U postgres django_drf_hw < backup.sql
```

## Безопасность
- Убедитесь, что все секретные данные хранятся в .env файле
- Регулярно обновляйте пакеты и зависимости
- Используйте сложные пароли
- Настройте файрвол и ограничьте доступ к портам
- Регулярно делайте бэкапы данных

## Устранение неполадок
1. Если контейнеры не запускаются:
   ```bash
   docker-compose logs
   ```

2. Если нет доступа к Docker:
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

3. Если не работает CI/CD:
   - Проверьте секреты в GitHub
   - Проверьте права доступа к директории проекта
   - Проверьте логи в GitHub Actions

# Запуск проекта через Docker Compose

Для запуска проекта с использованием Docker Compose выполните следующие шаги:

1. Клонируйте репозиторий:
   ```bash
   git clone https://your-repository-url.git
   cd django_drf_hw
   ```

2. Создайте файл `.env` в корне проекта с данными для подключения к базе данных и другим сервисам:
   ```bash
   cp .env.example .env
   ```

3. Запустите проект с использованием Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. После того как все сервисы будут запущены, вы сможете проверить работу каждого из них:
   - **Django (backend)**: Перейдите по адресу [http://localhost:8000](http://localhost:8000) для проверки работы веб-приложения.
   - **PostgreSQL (db)**: Используйте команду `docker-compose exec db psql -U myuser -d mydatabase` для входа в базу данных.
   - **Redis**: Проверить работу Redis можно с помощью утилиты командной строки `redis-cli`.
   - **Celery**: Логи Celery можно просмотреть с помощью команды `docker-compose logs celery` или `docker-compose logs celery_beat`.

5. Для остановки сервисов используйте:
   ```bash
   docker-compose down
   ```

### 4. **Dockerfile для Django и Celery**
Убедитесь, что в корне проекта есть файл `Dockerfile` для настройки вашего Django-приложения и Celery. Пример:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]