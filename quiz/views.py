from rest_framework import viewsets, mixins
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


class QuizViewSet(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_permissions(self):
        if self.action in ACTIONS_FOR_ADMIN:
            return (IsAdminUser(),)
        return (IsAuthenticated(),)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveQuizSerializer
        return QuizSerializer

    # NEED OPTIMIZATION
    @action(detail=True, url_path='users-rank')
    def get_user_top_per_quiz(self, request, pk=None):
        dct = {}

        for user in User.objects.exclude(is_superuser=True):
            user_answers = UserAnswer.objects.filter(user=user)
            dct[user.username] = 0
            if user_answers:
                for user_answer in user_answers:
                    right_answers = Answer.objects.filter(is_right=True).filter(id=user_answer.answer.id)
                    for answer in right_answers:
                        if answer.question.quiz.id == int(pk):
                            dct[user.username] += answer.question.points

        return Response({k: v for k, v in sorted(dct.items(), key=lambda item: item[1], reverse=True)})


    # NEED OPTIMIZATION
    @action(detail=False, url_path='users-rank')
    def get_user_global_top(self, request, pk=None):
        dct = {}

        for user in User.objects.exclude(is_superuser=True):
            user_answers = UserAnswer.objects.filter(user=user)
            dct[user.username] = 0
            if user_answers:
                for user_answer in user_answers:
                    right_answers = Answer.objects.filter(is_right=True).filter(id=user_answer.answer.id)
                    for answer in right_answers:
                        dct[user.username] += answer.question.points

        return Response({k: v for k, v in sorted(dct.items(), key=lambda item: item[1], reverse=True)})

    
class QuestionViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ACTIONS_FOR_ADMIN:
            return (IsAdminUser(),)
        return (IsAuthenticated(),)

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


class AnswerViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdminUser,)
