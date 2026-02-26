from rest_framework import serializers
from .models import Category, Course, Module, Lesson


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
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"