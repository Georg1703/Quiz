from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action

from quiz.serializers import (
    QuizSerializer, 
    RetrieveQuizSerializer, 
    QuestionSerializer,
    RetrieveQuestionSerializer,
    AnswerSerializer, 
    UserAnswerSerializer 
)
from quiz.models import Quiz, Question, Answer


class QuizViewSet(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveQuizSerializer
        return QuizSerializer

    @action(detail=True, url_path='user-rank')
    def get_user_rank_per_quiz(self, request, pk=None):
        return Response({'user rank'})

    


class QuestionViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveQuestionSerializer
        return QuestionSerializer

    @action(detail=True, methods=['post'], url_path='answer/(?P<answer_id>\d+)')
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
    permission_classes = [permissions.IsAdminUser]
