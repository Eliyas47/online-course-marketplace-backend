from django.urls import path
from .views import UserCertificatesView

urlpatterns = [
    path("my-certificates/", UserCertificatesView.as_view()),
]