from django.urls import path
from .views import CreatePaymentView

urlpatterns = [
    path("pay/", CreatePaymentView.as_view(), name="course-payment"),
]
