import re

from rest_framework.serializers import ValidationError


class YouTubeUrlValidator:
    # Выносим компиляцию regex в константу класса
    YOUTUBE_REGEX = re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/")

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)

        if not value:
            return

        if not self.YOUTUBE_REGEX.match(value.lower()):
            raise ValidationError(
                "Разрешены только ссылки на YouTube. Пример: "
                "https://www.youtube.com/watch?v=... или https://youtu.be/..."
            )
