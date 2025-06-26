from django.db import models


class Course(models.Model):
    """
    Хранит информацию о курсе.

    Связанные модели:
    - :model:`lms.Lesson` - уроки, принадлежащие этому курсу
    """

    name = models.CharField(
        max_length=50, verbose_name="Название курса", help_text="Введите название курса"
    )
    preview = models.ImageField(upload_to="lms/preview_course", blank=True, null=True)
    description = models.CharField(
        max_length=50,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Создатель курса",
        null=True,
        blank=True,
    )
    price = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name="Цена курса"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Хранит информацию об уроке, принадлежащем курсу.

    Связанные модели:
    - :model:`lms.Course` - курс, к которому принадлежит урок
    """

    name = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="Введите название урока"
    )
    preview = models.ImageField(upload_to="lms/preview_lesson", blank=True, null=True)
    description = models.CharField(
        max_length=50,
        verbose_name="Описание урока",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )
    video_url = models.CharField(
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видеоурок",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", help_text="Выберите курс"
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Создатель урока",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (курс: {self.course.name})"


class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")  # Запрет дублирования подписок

    def __str__(self):
        return f"{self.user} -> {self.course}"
