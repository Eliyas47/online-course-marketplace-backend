from rest_framework import serializers
from .models import Review
from enrollments.models import Enrollment


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["student"]
    

    def validate(self, data):
        user = self.context["request"].user
        course = data["course"]

        # Check enrollment
        if not Enrollment.objects.filter(student=user, course=course).exists():
            raise serializers.ValidationError(
                "You must enroll in this course before reviewing."
            )

        return data
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value