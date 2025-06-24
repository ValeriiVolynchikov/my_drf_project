from rest_framework import serializers

from lms.serializer import CourseSerializer
from users.models import Payment, User


class PaymentSerializers(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},  # Делаем поле только для чтения
            "price": {"read_only": True},  # Цена будет вычисляться автоматически
            "payment_course": {"required": False},  # Так как берем из URL
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
