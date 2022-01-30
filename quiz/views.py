from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from django.contrib.auth.models import User

from quiz.serializers import (
    QuizSerializer,
    RetrieveQuizSerializer,
    QuestionSerializer,
    RetrieveQuestionSerializer,
    AnswerSerializer,
    UserAnswerSerializer
)
from quiz.models import Quiz, Question, Answer, UserAnswer


ACTIONS_FOR_ADMIN = ['create', 'update', 'partial_update', 'destroy']


class QuizViewSet(viewsets.ModelViewSet):

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_permissions(self):
        if self.action in ACTIONS_FOR_ADMIN:
            return IsAdminUser(),
        return IsAuthenticated(),

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveQuizSerializer
        return QuizSerializer

    @action(detail=True, url_path='users-rank')
    def get_user_top_per_quiz(self, request, pk=None):
        dct = {}

        for elem in UserAnswer.objects.all().select_related('answer', 'user'):
            dct[elem.user.username] = 0
            if elem.answer.is_right and elem.answer.question.id == int(pk):
                dct[elem.user.username] += elem.answer.question.points

        return Response({k: v for k, v in sorted(dct.items(), key=lambda item: item[1], reverse=True)})

    @action(detail=False, url_path='users-rank')
    def get_user_global_top(self, request, pk=None):
        dct = {}

        for elem in UserAnswer.objects.all().select_related('answer', 'user'):
            dct[elem.user.username] = 0
            if elem.answer.is_right:
                dct[elem.user.username] += elem.answer.question.points

        return Response({k: v for k, v in sorted(dct.items(), key=lambda item: item[1], reverse=True)})


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ACTIONS_FOR_ADMIN:
            return IsAdminUser(),
        return IsAuthenticated(),

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveQuestionSerializer
        return QuestionSerializer

    @action(detail=True, methods=['post'], url_path='answers/(?P<answer_id>\d+)')
    def select_answer(self, request, pk=None, answer_id=None):
        data = {'user': request.user.id, 'answer': answer_id}
        serializer = UserAnswerSerializer(data=data, context={'question': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdminUser,)
