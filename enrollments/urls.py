from django.urls import path
from .views import CourseProgressView, EnrollCourseView
from enrollments import views
from .views import MarkLessonCompleteView
urlpatterns = [
    path('enroll/', views.EnrollCourseView.as_view(), name='enroll-course'),
    path("progress/", MarkLessonCompleteView.as_view()),
    path("progress/<int:pk>/", CourseProgressView.as_view()),
]

from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, LessonProgressViewSet

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'lesson-progress', LessonProgressViewSet)

urlpatterns = router.urls