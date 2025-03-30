from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# import eventlet для вопроса наставнику
# eventlet.monkey_patch()
# celery -A config worker -l INFO -P eventlet
# celery -A config worker -l INFO --pool=solo -E - рабочий вариант




# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

app.conf.broker_connection_retry_on_startup = True  # Попробовать убрать и запустить без него. Для вопроса наставнику

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

# Настройка часового пояса
app.conf.timezone = settings.TIME_ZONE
