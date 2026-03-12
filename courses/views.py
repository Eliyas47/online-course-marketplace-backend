from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Sum, Q  # Added Q
from .models import Course, Module, Lesson
from .serializers import CourseSerializer, CourseListSerializer, ModuleSerializer, LessonSerializer
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
    "modules__lessons",
    "reviews"
).order_by("-id")   # ✅ FIX pagination warning


# =====================================
# Public Course List
# =====================================
class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer  # Use optimized serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if getattr(user, 'role', None) == "admin":
            return optimized_course_queryset
            
        if getattr(user, 'role', None) == "instructor":
            return optimized_course_queryset.filter(
                Q(instructor=user) | Q(is_published=True)
            )
            
        return optimized_course_queryset.filter(is_published=True)


# =====================================
# Course Detail
# =====================================
class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if getattr(user, 'role', None) == "admin":
            return optimized_course_queryset
            
        if getattr(user, 'role', None) == "instructor":
            return optimized_course_queryset.filter(
                Q(instructor=user) | Q(is_published=True)
            )
            
        return optimized_course_queryset.filter(is_published=True)


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
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsEnrolledOrInstructor]

class CourseLearnView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsEnrolledOrInstructor]

    def get_queryset(self):
        user = self.request.user
        
        if getattr(user, 'role', None) == "admin":
            return optimized_course_queryset
            
        if getattr(user, 'role', None) == "instructor":
            return optimized_course_queryset.filter(
                Q(instructor=user) | Q(is_published=True)
            )
            
        return optimized_course_queryset.filter(is_published=True)


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


class CreateModuleView(generics.CreateAPIView):
    queryset = Module.objects.select_related("course")
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.instructor != self.request.user:
            raise PermissionDenied("You do not own this course.")
        serializer.save()


# =====================================
# Create Lesson
# =====================================
class CreateLessonView(generics.CreateAPIView):
    queryset = Lesson.objects.select_related("module", "module__course")
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        module = serializer.validated_data['module']
        if module.course.instructor != self.request.user:
            raise PermissionDenied("You do not own this course.")
        serializer.save()


# =====================================
# Lesson Detail
# =====================================
class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.select_related(
        "module",
        "module__course"
    )
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsEnrolledOrInstructor]


# =====================================
# Instructor Dashboard
# =====================================
class InstructorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        courses = Course.objects.filter(instructor=request.user)

        total_students = Enrollment.objects.filter(
            course__in=courses
        ).count()

        total_revenue = Payment.objects.filter(
            course__in=courses,
            status="completed"
        ).aggregate(total=Sum("amount"))["total"] or 0

        return Response({
            "total_courses": courses.count(),
            "total_students": total_students,
            "total_revenue": total_revenue
        })