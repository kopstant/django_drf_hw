from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson
from users.models import SubscriptionForCourse

User = get_user_model()


class LessonCRUDTests(APITestCase):
    def setUp(self):
        # Создаём тестового пользователя (владельца)
        self.owner = User.objects.create_user(email="owner@example.com", password="testpassword", username="owner")
        self.owner_client = APIClient()
        self.owner_client.force_authenticate(user=self.owner)

        # Создаём тестового пользователя (модератора)
        self.moderator = User.objects.create_user(
            email="moderator@example.com", password="testpassword", username="moderator", is_staff=True  # Модератор
        )
        self.moderator_client = APIClient()
        self.moderator_client.force_authenticate(user=self.moderator)

        # Создаём тестовый курс
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.owner)

        # Создаём тестовый урок
        self.lesson = Lesson.objects.create(
            title="Test Lesson", description="Test Lesson Description", course=self.course, owner=self.owner
        )

    def test_create_lesson_by_owner(self):
        """
        Тест создания урока владельцем.
        """
        url = reverse("lms:lesson-create")
        data = {
            "title": "New Lesson",
            "description": "New Lesson Description",
            "course": self.course.id,
            "video_url": "https://youtube.com/video",
        }
        response = self.owner_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_by_moderator(self):
        """
        Тест создания урока модератором (должен быть запрещён)
        """
        url = reverse("lms:lesson-create")
        data = {
            "title": "New Lesson",
            "description": "New Lesson Description",
            "course": self.course.id,
            "video_url": "https://youtube.com/video",
        }
        response = self.moderator_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_lesson(self):
        """
        Тест получения урока.
        """
        url = reverse("lms:lesson-get", args=[self.lesson.id])
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")

    def test_update_lesson_by_owner(self):
        """
        Тест обновления урока владельцем.
        """
        url = reverse("lms:lesson-update", args=[self.lesson.id])
        data = {
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "course": self.course.id,
            "video_url": "https://youtube.com/video",
        }
        response = self.owner_client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_by_moderator(self):
        """
        Тест обновления урока модератором.
        """
        url = reverse("lms:lesson-update", args=[self.lesson.id])
        data = {
            "title": "Updated Lesson",
            "description": "Updated Lesson Description",
            "course": self.course.id,
            "video_url": "https://youtube.com/video",
        }
        response = self.moderator_client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson_by_owner(self):
        """
        Тест удаления урока владельцем.
        """
        url = reverse("lms:lesson-delete", args=[self.lesson.id])
        response = self.owner_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_by_moderator(self):
        """
        Тест удаления урока модератором (должен быть запрещён).
        """
        url = reverse("lms:lesson-delete", args=[self.lesson.id])
        response = self.moderator_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTests(APITestCase):
    def setUp(self):
        # Создаём тестового пользователя
        self.user = User.objects.create_user(email="testuser@example.com", password="testpassword", username="testuser")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создаём тестовый курс
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)

    def test_subscribe_to_course(self):
        """
        Тест подписки на курс.
        """
        url = reverse("lms:subscriptions")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(SubscriptionForCourse.objects.filter(owner=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        """
        Тест отписки от курса.
        """
        # Сначала подписываемся на курс
        SubscriptionForCourse.objects.create(owner=self.user, course=self.course)

        url = reverse("lms:subscriptions")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(SubscriptionForCourse.objects.filter(owner=self.user, course=self.course).exists())

    def test_subscribe_to_nonexistent_course(self):
        """
        Тест попытки подписки на несуществующий курс.
        """
        url = reverse("lms:subscriptions")
        data = {"course_id": 999}  # Несуществующий ID курса
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Course does not find.")
