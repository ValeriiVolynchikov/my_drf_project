from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from lms.models import Course, Lesson, Subscription


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            name="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson", course=self.course, owner=self.user
        )
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        url = reverse("lms:course-list")
        data = {"name": "Курс1", "video_url": "https://www.youtube.com/s"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"name": "Курс", "video_url": "https://www.youtube.com/"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Курс")

    def test_course_delete(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)
        data = response.json()
        result = data["results"]
        res = len(result[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(res, 6)

class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            name="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("lms:lessons_create")
        data = {"name": "Урок", "video_url": "https://www.youtube.com/", "course": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lessons_update", args=(self.lesson.pk,))
        data = {"name": "Урок3"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок3")

    def test_lesson_delete(self):
        url = reverse("lms:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = data["results"]
        res = len(result[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(res, 7)

class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@example.com')
        self.course = Course.objects.create(name='Python/git', description='Введение в git.hub', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        url = reverse('lms:subscriptions')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(Subscription.objects.count(), 1)
        subscription = Subscription.objects.first()

        self.assertEqual(
            subscription.course, self.course
        )

    def test_unsubscribe_from_course(self):
        url = reverse('lms:subscriptions')
        Subscription.objects.create(user=self.user, course=self.course)
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)
