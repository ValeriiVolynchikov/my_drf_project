from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    """
    Кастомная модель пользователя с email в качестве идентификатора.

    Наследуется от :model:`auth.AbstractUser` и переопределяет стандартное поведение.
    Связанные модели:
    - :model:`users.Payment` - платежи пользователя
    """

    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email} ({self.get_full_name() or 'без имени'})"


class Payment(models.Model):
    """
    Модель для хранения информации о платежах пользователей.

    Связанные модели:
    - :model:`users.User` - пользователь, совершивший платеж
    - :model:`lms.Course` - оплаченный курс (если применимо)
    - :model:`lms.Lesson` - оплаченный урок (если применимо)
    """

    PAYMENT_OPTIONS = (
        ("Cash", "Наличные"),
        ("Non_cash", "Безналичные"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты",
        help_text="Введите дату оплаты",
        blank=True,
        null=True,
    )
    payment_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True,
    )
    payment_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True,
    )
    price = models.IntegerField(verbose_name="Стоимость", default=0)
    payment_method = models.CharField(
        choices=PAYMENT_OPTIONS, verbose_name="Способ оплаты", blank=True, null=True
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
