from rest_framework import serializers
from .models import Category, Course, Module, Lesson, LessonProgress


# ----------------------------
# Category Serializer
# ----------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# ----------------------------
# Lesson Serializer
# ----------------------------
class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "content",
            "video_url",
            "module",
        ]


# ----------------------------
# Module Serializer
# ----------------------------
class ModuleSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            "id",
            "title",
            "course",
            "lessons"
        ]


# ----------------------------
# Course Serializer
# ----------------------------
class CourseSerializer(serializers.ModelSerializer):

    modules = ModuleSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "thumbnail",
            "price",
            "level",
            "category",
            "instructor",
            "is_published",
            "created_at",
            "modules",
            "average_rating"
        ]
        read_only_fields = ["instructor"]

    def get_average_rating(self, obj):
        return obj.average_rating()


# ----------------------------
# Course List Serializer (Optimized)
# ----------------------------
class CourseListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "thumbnail",
            "price",
            "level",
            "category",
            "instructor",
            "is_published",
            "created_at",
            "average_rating"
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()


# ----------------------------
# Lesson Progress Serializer
# ----------------------------
class LessonProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonProgress
        fields = "__all__"
        read_only_fields = ["student"]