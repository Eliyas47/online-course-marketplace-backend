from django.db import models
from django.conf import settings
from courses.models import Course


class Payment(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    transaction_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.conf import settings
from courses.models import Course
from enrollments.models import Enrollment


class Payment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, default="completed")
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} paid for {self.course.title}"