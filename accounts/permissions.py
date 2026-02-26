from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "instructor"


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsInstructorOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "instructor":
            return True

        return False