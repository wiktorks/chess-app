from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_activation_email_task(current_site, uidb64, user_email, token):
    activation_url = f'{current_site}/api/auth/activate/{uidb64}/{token}/'
    send_mail(
        'Account activation mail',
        f'Click on this link to activate Your account: {activation_url}',
        'wiktorks1994@gmail.com',
        [user_email]
    )
