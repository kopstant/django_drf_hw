from rest_framework import serializers

from users.models import SubscriptionForCourse

from .models import Course, Lesson
from .validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

        validators = [
            VideoUrlValidator(field="video_url"),
        ]


class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("title", "description")


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_count_subscriptions(self, obj):
        return f"Подписок: {obj.subscriptions.count()}"

    def get_subscriptions(self, obj):
        user = self.context["request"].user
        if SubscriptionForCourse.objects.filter(owner=user, course=obj).exists():
            return "У вас есть подписка на данный курс."
        return "У вас нет подписки на данный курс"
