from rest_framework.permissions import BasePermission


class IsInstructorOrReadOnly(BasePermission):
    """
    - Students can only read (GET)
    - Instructors can create (POST)
    - Admin can do everything
    """

    def has_permission(self, request, view):

        # SAFE METHODS = GET, HEAD, OPTIONS
        if request.method in ['GET','HEAD', 'OPTIONS']:
            return True

        # If not authenticated
        if not request.user.is_authenticated:
            return False

        # Admin always allowed
        if request.user.role == "admin":
            return True

        # Instructor allowed to create
        if request.user.role == "instructor":
            return True

        # Students cannot POST
        return False
    
from rest_framework.permissions import BasePermission
from enrollments.models import Enrollment


class IsEnrolledOrInstructor(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin can access everything
        if user.role == "admin":
            return True

        # Instructor who owns the course
        if obj.instructor == user:
            return True

        # Student enrolled in course
        return Enrollment.objects.filter(
            student=user,
            course=obj
        ).exists()
from rest_framework.permissions import BasePermission
from enrollments.models import Enrollment


class IsEnrolledOrInstructor(BasePermission):
    """
    - Instructor who owns the course can access
    - Student enrolled in the course can access
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Must be authenticated
        if not user.is_authenticated:
            return False

        course = obj.module.course

        # Instructor who owns the course
        if course.instructor == user:
            return True

        # Student enrolled
        return Enrollment.objects.filter(
            student=user,
            course=course
        ).exists()