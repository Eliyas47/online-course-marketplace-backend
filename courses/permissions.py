from rest_framework.permissions import BasePermission
from enrollments.models import Enrollment


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


class IsEnrolledOrInstructor(BasePermission):
    """
    - Admin can access everything
    - Instructor who owns the course can access
    - Student enrolled in the course can access (if verified)
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Must be authenticated
        if not user.is_authenticated:
            return False

        # Admin can access everything
        if getattr(user, 'role', None) == "admin":
            return True

        # Determine the course object depending on if obj is a Course or a Lesson
        if hasattr(obj, 'module'):
            course = obj.module.course
        else:
            course = obj

        # Instructor who owns the course
        if course.instructor == user:
            return True

        # Student enrolled in course
        enrollment = Enrollment.objects.filter(
            student=user,
            course=course
        ).first()
        
        if enrollment:
            return user.is_active  # Only active (verified) users can access
            
        return False