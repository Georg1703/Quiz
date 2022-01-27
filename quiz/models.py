from django.db import models
from django.contrib.auth.models import User

class BasedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Quiz(BasedModel):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

class Question(BasedModel):
    TYPE = (
        (1, 'Yes/No'),
        (2, 'Multiple choice'),
    )
    question = models.CharField(max_length=255)
    points = models.IntegerField()
    question_type = models.IntegerField(choices=TYPE, default=1)
    quiz = models.ForeignKey(Quiz, related_name='question', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.question}'
   
    
class Answer(BasedModel):
    answer = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='answer', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.answer}'


class UserAnswer(BasedModel):
    answer = models.ForeignKey(Answer, related_name='user_answer', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, related_name='user_answer', on_delete=models.DO_NOTHING)