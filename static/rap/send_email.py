from django.core.mail import send_mail


def send_confirmation_email(user):
    send_mail(
        'Здравствуйте, вы успешно зарегестрированы!',
        f'Желаем вам поскорее начать работу и изучить что-то новое!', 'dzhylyshpaevbaktiyar@gmail.com',
        [user],
        fail_silently=False
    )


def send_code_password_reset(user):
    code = user.activation_code
    email = user.email
    send_mail(
        'Письмо с кодом для сброса пароля!',
        f'Ваш код для того, чтобы восстановить пароль: {code}\nНикому не передавайте этот код!', 'dzhylyshpaevbaktiyar@gmail.com',
        [email],
        fail_silently=False
    )