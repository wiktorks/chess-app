from django.core.mail import send_mail
from django.core.mail import EmailMessage
from celery import shared_task

@shared_task
def send_email_task_test():
    send_mail(
        'My Django mailer worked!', 
        'This is the proof that my mailer works!!!!',
        'wiktorks1994@gmail.com',
        ['atkt1haj1i@dispostable.com']
    )

@shared_task
def send_activation_email_task(current_site, uidb64, token, receiver_email):
    activation_url = f'{current_site}/api/auth/activate/{uidb64}/{token}/'
    send_mail(
        'Account activation mail',
        f'Click on this link to activate Your account: {activation_url}',
        'wiktorks1994@gmail.com',
        [receiver_email]
    )
