from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ObjectDoesNotExist

from quiz.models import Quiz, Question, Answer, UserAnswer


class QuizSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'created_at')


class RetrieveQuizSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'created_at', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ('id', 'question', 'points', 'question_type', 'quiz', 'created_at')


class RetrieveQuestionSerializer(serializers.ModelSerializer):
    answer = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Question
        fields = ('id', 'question', 'points', 'question_type', 'quiz', 'created_at', 'answer')


class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = ('id', 'answer', 'is_right', 'question', 'created_at')

    def validate(self, data):
        if 'question' in data:
            question = Question.objects.get(id=data['question'].id)

            if question.question_type == 1:
                if Answer.objects.filter(question=question.id).count() >= 2:
                    raise serializers.ValidationError("For that type of question are allowed only 2 answers")
        return data


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = ('id', 'answer', 'user')

        validators = [
            UniqueTogetherValidator(
                queryset=UserAnswer.objects.all(),
                fields=['user', 'answer']
            )
        ]

    def validate(self, data):
        try:
            Answer.objects.get(id=data['answer'].id, question=self.context['question'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Question with that answer does not exist")

        answers = Answer.objects.filter(question=self.context['question']).values_list('id', flat=True)
        for answer in answers:
            if answer in UserAnswer.objects.filter(user=data['user']).values_list('answer', flat=True):
                raise serializers.ValidationError("Only one answer per question is allowed")

        return data
