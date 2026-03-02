import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from courses.models import Course
from enrollments.models import Enrollment
from .models import Payment


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        # prevent duplicate
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response({"error": "Already enrolled."}, status=400)

        payment = Payment.objects.create(
            student=request.user,
            course=course,
            amount=course.price,
            status="completed",
            transaction_id=uuid.uuid4()
        )

        Enrollment.objects.create(
            student=request.user,
            course=course
        )

        return Response({
            "message": "Payment successful",
            "transaction_id": payment.transaction_id
        }, status=status.HTTP_201_CREATED)