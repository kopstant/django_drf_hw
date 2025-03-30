import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(course):
    """Создание продукта в Stripe"""
    product = stripe.Product.create(
        name=course.title,
        description=course.description,
    )
    return product.id


def create_stripe_price(product_id, amount):
    """Создание цены в Stripe"""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,
        currency='rub',
    )
    return price.id


def create_stripe_session(price_id):
    """Создание сессии оплаты в Stripe"""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/',
    )
    return {
        'session_id': session.id,
        'payment_link': session.url
    }
