from rest_framework import serializers
from .models import Category, Course, Module, Lesson, LessonProgress

# ----------------------------
# Lesson Serializer
# ----------------------------
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "content", "video_url", "order"]


# ----------------------------
# Module Serializer
# ----------------------------
class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ["id", "title", "order", "lessons"]


# ----------------------------
# Course Serializer
# ----------------------------
class CourseSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_average_rating(self, obj):
        return obj.average_rating()


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = "__all__"
        read_only_fields = ["student"]