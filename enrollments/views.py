from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from courses import permissions
from .models import Enrollment
from .serializers import EnrollmentSerializer, LessonProgressSerializer
from accounts.permissions import IsStudent
from rest_framework.exceptions import ValidationError
from courses.models import LessonProgress
from courses.permissions import IsEnrolledOrInstructor
from rest_framework.response import Response


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