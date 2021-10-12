from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_email_task():
    send_mail(
        'My Django mailer worked!', 
        'This is a proof that Django mailer works!!!',
        'wiktorks1994@gmail.com',
        ['atkt1haj1i@dispostable.com']
    )
    return None
