from .celery import app
from rap.send_email import send_confirmation_email
from django.core.mail import send_mail
from rap.models import Spam_Contacts


@app.task
def send_email_task(user):
    send_confirmation_email(user)


@app.task
def send_spam_email():
    for user in Spam_Contacts.objects.all():
        send_mail('Spam Spam Spam', 'This is spam letter for you by Baktiyar!',
                  'dzhylyshpaevbaktiyar@gmail.com',
                  [user.email], fail_silently=False,)



