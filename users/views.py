from rest_framework import filters, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from lms.models import Course
from users.models import Payment, User
from users.serializer import PaymentSerializers, UserSerializer
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializers
    queryset = Payment.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_id")
        course = Course.objects.get(id=course_id)

        course_name = course.name
        course_price = course.price or 0

        stripe_product_id = create_stripe_product(course_name)
        stripe_price = create_stripe_price(course_price, stripe_product_id)
        session_id, payment_link = create_stripe_session(stripe_price)

        payment = serializer.save(
            user=self.request.user,
            payment_course=course,
            price=course_price,
            session_id=session_id,
            link=payment_link,
        )
        payment.save()
