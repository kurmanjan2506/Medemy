from django.core.mail import send_mail
from buy_course.models import UsersCourse


def send_confirmation_email(user, course_title):
    send_mail(
        f'Здравствуйте, поздравляем вас с приобретением курса {course_title}!',
        f'Вас приветствует учебная платформа Medemy. Желаем вам поскорее начать работу и изучить что-то новое!',
        'dzhylyshpaevbaktiyar@gmail.com',
        [user],
        fail_silently=False
    )