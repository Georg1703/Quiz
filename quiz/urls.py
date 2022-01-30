from django.urls import path
from rest_framework import routers

from quiz.views import QuizViewSet, QuestionViewSet, AnswerViewSet

router = routers.SimpleRouter()

router.register(r'quizzes', QuizViewSet, 'quizzes')
router.register(r'questions', QuestionViewSet, 'questions')
router.register(r'answers', AnswerViewSet, 'answers')

urlpatterns = router.urls
