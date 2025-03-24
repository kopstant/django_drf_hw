from venv import logger

import stripe
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from lms.models import Course, Lesson


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
        ('stripe', 'Stripe'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.PositiveIntegerField(verbose_name='Сумма платежа', help_text='Укажите сумму платежа')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии',
                                  help_text='Укажите ID сессии')
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name='Ссылка на оплату',
                           help_text='Укажите ссылку на оплату')
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.payment_method})"

    def create_stripe_payment(self, request):
        """Создание платежа в Stripe"""
        if not self.course and not self.lesson:
            raise ValueError("Платеж должен быть привязан к курсу или уроку")

        # Определяем название и описание продукта
        if self.course:
            product_name = self.course.title
            product_description = self.course.description or "Оплата курса"
        else:
            product_name = self.lesson.title
            product_description = self.lesson.description or "Оплата урока"

        try:
            # Создаем продукт в Stripe
            product = stripe.Product.create(
                name=product_name,
                description=product_description,
            )
            self.stripe_product_id = product.id

            # Создаем цену (умножаем на 100 для перевода в копейки/центы)
            price = stripe.Price.create(
                product=self.stripe_product_id,
                unit_amount=int(self.amount * 100),
                currency="rub",
            )
            self.stripe_price_id = price.id

            # Создаем URL для редиректа после оплаты
            success_url = request.build_absolute_uri(
                reverse('users:payment_success', kwargs={'pk': self.pk})
            )
            cancel_url = request.build_absolute_uri(
                reverse('users:payment_cancel', kwargs={'pk': self.pk})
            )

            # Создаем сессию оплаты
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': self.stripe_price_id,
                    'quantity': int(1),
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=self.user.email if self.user else None,
                metadata={
                    'payment_id': str(self.id),
                }
            )

            # Сохраняем данные сессии
            self.session_id = session.id
            self.link = session.url
            self.payment_method = 'stripe'
            self.save()

            return self.link, self.session_id

        except stripe.error.StripeError as e:
            # Логируем ошибку Stripe
            logger.error(f"Stripe error: {e}")
            raise ValueError(f"Ошибка при создании платежа: {e.user_message}")

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class SubscriptionForCourse(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Подписка на курс')
    created_at = models.DateTimeField(auto_now_add=True)

    # stripe

    def __str__(self):
        return f"{self.owner} - {self.course} - {self.created_at}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['created_at', 'owner', 'course']
