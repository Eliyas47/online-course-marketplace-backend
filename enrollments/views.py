from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer
from accounts.permissions import IsStudent
from rest_framework.exceptions import ValidationError


class EnrollCourseView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)