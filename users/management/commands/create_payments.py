from django.core.management.base import BaseCommand
from users.models import Payment, User
from lms.models import Course, Lesson
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Creates test payment data'

    def handle(self, *args, **options):
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        methods = ['Cash', 'Non_cash']  # Варианты из модели

        for i in range(10):
            user = random.choice(users)
            payment_date = datetime.now() - timedelta(days=random.randint(1, 30))

            # Выбираем курс или урок, но не оба сразу
            if random.random() < 0.5:
                payment_course = random.choice(courses)
                payment_lesson = None
            else:
                payment_course = None
                payment_lesson = random.choice(lessons)

            # Генерируем сумму оплаты
            if payment_course:
                amount = random.randint(10000, 50000)  # Пример диапазона для курсов
            elif payment_lesson:
                amount = random.randint(1000, 5000)  # Пример диапазона для уроков
            else:
                amount = 0  # Если ничего не выбрано

            payment_method = random.choice(methods)

            Payment.objects.create(
                user=user,
                payment_date=payment_date,
                payment_course=payment_course,
                payment_lesson=payment_lesson,
                price=amount,
                payment_method=payment_method
            )

        self.stdout.write(self.style.SUCCESS('Successfully created payments'))
