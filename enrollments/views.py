from urllib import request

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from certificates.models import Certificate
from courses import permissions
from .models import Enrollment
from .serializers import EnrollmentSerializer, LessonProgressSerializer
from accounts.permissions import IsStudent
from rest_framework.exceptions import ValidationError
from courses.models import LessonProgress
from courses.permissions import IsEnrolledOrInstructor
from rest_framework.response import Response


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from courses.models import Course, Lesson
from .models import Enrollment
from courses.models import LessonProgress



class EnrollCourseView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class MarkLessonCompleteView(generics.CreateAPIView):
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class CourseProgressView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, pk):
        from courses.models import Course
        course = Course.objects.get(pk=pk)

        total_lessons = course.modules.all().values_list("lessons", flat=True).count()

        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__module__course=course,
            completed=True
        ).count()

        percentage = 0
        if total_lessons > 0:
            percentage = (completed_lessons / total_lessons) * 100
        from certificates.models import Certificate  # put this at the top

        if percentage == 100:
           Certificate.objects.get_or_create(
              user=request.user,
              course=course
            )
        return Response({
            "course": course.title,
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
            "progress_percentage": round(percentage, 2)
        })
from rest_framework import viewsets, permissions

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
class LessonProgressViewSet(viewsets.ModelViewSet):
    queryset = LessonProgress.objects.all()
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LessonProgress.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from courses.models import Course, Lesson
from courses.models import LessonProgress

class CourseProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        total_lessons = Lesson.objects.filter(
            section__course=course
        ).count()

        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__section__course=course,
            completed=True
        ).count()

        percentage = 0
        if total_lessons > 0:
            percentage = (completed_lessons / total_lessons) * 100

        return Response({
            "course": course.title,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "progress_percentage": round(percentage, 2)
        })