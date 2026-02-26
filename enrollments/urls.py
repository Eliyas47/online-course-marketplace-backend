from django.urls import path
from .views import EnrollCourseView
from enrollments import views
urlpatterns = [
    path('enroll/', views.EnrollCourseView.as_view(), name='enroll-course'),
]