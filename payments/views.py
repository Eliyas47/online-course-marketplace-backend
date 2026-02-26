from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Payment
from .serializers import PaymentSerializer
from courses.models import Course
from enrollments.models import Enrollment
from accounts.permissions import IsStudent


class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        # Prevent duplicate enrollment
        if Enrollment.objects.filter(
            student=self.request.user,
            course=course
        ).exists():
            raise ValidationError("Already enrolled.")

        # Create payment
        payment = serializer.save(
            student=self.request.user,
            amount=course.price
        )

        # Auto create enrollment
        Enrollment.objects.create(
            student=self.request.user,
            course=course
        )