"""This module contains urls for Interview application."""
from rest_framework import routers
from .views import QuestionViewSet
from .views import TestViewSet
from .views import UserViewSet
from .views import CandidateTestMappingViewSet
from .views import CandidateSolutionViewSet

router = routers.DefaultRouter()  # pylint: disable=invalid-name
router.register(r'question', QuestionViewSet)
router.register(r'user', UserViewSet)
router.register(r'test', TestViewSet)
router.register(r'schedule_test', CandidateTestMappingViewSet)
router.register(r'execute', CandidateSolutionViewSet)

app_name = 'interview'
urlpatterns = []
urlpatterns += router.urls
