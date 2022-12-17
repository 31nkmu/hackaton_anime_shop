from django.core.mail import send_mail

from config.celery import app


@app.task
def send_confirm_link(email, confirm_code):
    full_link = f'http://localhost:8000/api/v1/order/confirm/{confirm_code}'
    send_mail(
        'Ссылка для подтверждения заказа',
        full_link,
        'karimovbillal20002@gmailcom',
        [email]
    )
