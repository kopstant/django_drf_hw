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