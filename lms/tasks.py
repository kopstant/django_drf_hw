import os
from datetime import timedelta, timezone

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
import logging

from lms.models import Course
from users.models import SubscriptionForCourse, CustomUser
from celery import shared_task
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


@shared_task
def send_course_update_mail(course_id):
    """
    Асинхронная рассылка. При обновлении курса, подписчикам курса приходит уведомление об изменении на почту.
    """
    try:
        course = Course.objects.get(id=course_id)
    except ObjectDoesNotExist:
        logger.error(f"Курс с ID {course_id} не найден!")
        return

    # Получаем всех подписчиков на курс.
    subscriptions = SubscriptionForCourse.objects.filter(course_id=course_id)

    # Формируем список email адресов подписчиков
    recipient_email = [subscribers.owner.email for subscribers in subscriptions]

    # Отправляем письмо всем подписчикам
    send_mail(
        subject="Курс обновлен!",
        message=f"Курс с ID {course_id} был обновлен. Проверьте его обновления!",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=recipient_email,
    )


@shared_task
def deactivate_inactive_users():
    """
    Задача для деактивации пользователей, которые не заходили более месяца
    """
    # Вычисляем дату, которая была месяц назад
    one_month_ago = timezone.now() - timedelta(days=30)

    # Находим пользователей, которые не заходили более месяца и еще активны.
    inactive_users = CustomUser.objects.filter(last_login__it=one_month_ago, is_active=True)

    count = inactive_users.update(is_active=False)

    return f"Деактивировано {count} неактивных пользователей"
