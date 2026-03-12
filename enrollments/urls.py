from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import CourseProgressView, EnrollCourseView, MarkLessonCompleteView, MyCoursesView
from .views import EnrollmentViewSet, LessonProgressViewSet

router = DefaultRouter()
# Register with an empty prefix so it maps to /api/enrollments/ directly
router.register(r'', EnrollmentViewSet, basename='enrollment')
router.register(r'lesson-progress', LessonProgressViewSet, basename='lesson-progress')

urlpatterns = [
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('enroll/', EnrollCourseView.as_view(), name='enroll-course'),
    path("progress/", MarkLessonCompleteView.as_view(), name='mark-lesson-complete'),
    path("progress/<uuid:pk>/", CourseProgressView.as_view(), name='course-progress-pk'),
    path("progress/<uuid:course_id>/", CourseProgressView.as_view(), name='course-progress-id'),
]

# Combine the router-generated URLs with the custom paths above
urlpatterns += router.urls
