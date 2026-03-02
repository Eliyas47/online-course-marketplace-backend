from rest_framework import generics, permissions
from .models import Certificate
from .serializers import CertificateSerializer


class UserCertificatesView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user)