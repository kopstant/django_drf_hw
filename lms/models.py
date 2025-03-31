from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="courses/", blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses", blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to="lessons/", blank=True, null=True)
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lessons", blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
