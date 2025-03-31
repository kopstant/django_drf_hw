FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /lms

# Копируем файлы зависимостей
COPY poetry.lock pyproject.toml ./

# Устанавливаем Poetry и зависимости
RUN python -m pip install --no-cache-dir poetry && \
    apt-get update && \
    apt-get install -y gcc libpq-dev && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root && \
    apt-get remove -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем весь проект
COPY . .

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Открываем порт для веб-сервера
EXPOSE 8000

# Запускаем Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]