from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"  # Включаем все поля модели Course, включая lesson_count


class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    def get_lesson_count(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = (
            "name",
            "preview",
            "description",
            "lesson_count",
            "lessons",
        )  # Включаем поле lessons
