from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Course
from .serializers import CourseSerializer
from accounts.permissions import IsInstructor

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsEnrolledOrInstructor

# Public course list
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Course detail
class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer


# Instructor create course
class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsInstructor]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)



class CourseLearnView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsEnrolledOrInstructor]

from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsInstructor
from .models import Module
from .serializers import ModuleSerializer


class CreateModuleView(generics.CreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Module, Lesson
from .serializers import ModuleSerializer, LessonSerializer


# ----------------------------
# Create Module
# ----------------------------
class CreateModuleView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]


# ----------------------------
# Create Lesson
# ----------------------------
class CreateLessonView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
from .permissions import IsEnrolledOrInstructor


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsEnrolledOrInstructor]

from rest_framework.exceptions import PermissionDenied

class CourseUpdateView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
    queryset = Course.objects.all()

    def perform_update(self, serializer):
        course = self.get_object()

        if course.instructor != self.request.user:
            raise PermissionDenied("You do not own this course.")

        serializer.save()
from rest_framework.exceptions import PermissionDenied

class CourseUpdateView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
    queryset = Course.objects.all()

    def perform_update(self, serializer):
        course = self.get_object()

        if course.instructor != self.request.user:
            raise PermissionDenied("You do not own this course.")

        serializer.save()
