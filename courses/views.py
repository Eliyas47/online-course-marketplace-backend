from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Sum

from .models import Course, Module, Lesson
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer
from .permissions import IsEnrolledOrInstructor
from accounts.permissions import IsInstructor
from enrollments.models import Enrollment
from payments.models import Payment


# =====================================
# Optimized Base Queryset for Courses
# =====================================
optimized_course_queryset = Course.objects.select_related(
    "instructor",
    "category"
).prefetch_related(
    "sections",
    "reviews"
)


# =====================================
# Public Course List
# =====================================
class CourseListView(generics.ListAPIView):
    queryset = optimized_course_queryset.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =====================================
# Course Detail
# =====================================
class CourseDetailView(generics.RetrieveAPIView):
    queryset = optimized_course_queryset.filter(is_published=True)
    serializer_class = CourseSerializer


# =====================================
# Instructor Create Course
# =====================================
class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


# =====================================
# Learn Course (Only Enrolled or Instructor)
# =====================================
class CourseLearnView(generics.RetrieveAPIView):
    queryset = optimized_course_queryset.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsEnrolledOrInstructor]


# =====================================
# Update Course
# =====================================
class CourseUpdateView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
    queryset = Course.objects.all()

    def perform_update(self, serializer):
        course = self.get_object()

        if course.instructor != self.request.user:
            raise PermissionDenied("You do not own this course.")

        serializer.save()


# =====================================
# Create Module
# =====================================
class CreateModuleView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsInstructor]


# =====================================
# Create Lesson
# =====================================
class CreateLessonView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


# =====================================
# Lesson Detail
# =====================================
class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsEnrolledOrInstructor]


# =====================================
# Instructor Dashboard
# =====================================
class InstructorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = request.user.courses.all()

        total_students = Enrollment.objects.filter(
            course__in=courses
        ).count()

        total_revenue = Payment.objects.filter(
            course__in=courses,
            status="completed"
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        return Response({
            "total_courses": courses.count(),
            "total_students": total_students,
            "total_revenue": total_revenue
        })