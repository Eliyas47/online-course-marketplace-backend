from rest_framework import serializers
from .models import Enrollment
from courses.models import LessonProgress


from courses.serializers import CourseSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['student']


class MyEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'progress']
        read_only_fields = ['student', 'course', 'enrolled_at', 'progress']


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = '__all__'
        read_only_fields = ['student']
