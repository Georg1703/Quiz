from django.urls import path
from rest_framework import routers

from quiz.views import QuizViewSet, QuestionViewSet, AnswerViewSet

router = routers.SimpleRouter()

router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = router.urls