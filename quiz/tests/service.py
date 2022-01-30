from quiz.models import Quiz, Question, Answer, UserAnswer


def create_quizzes(nr: int):
    return Quiz.objects.bulk_create([
        Quiz(title=f'Test quiz {i + 1}') for i in range(nr)
    ])


def create_questions(nr: int, points: int, question_type: int, quiz: Quiz):
    return Question.objects.bulk_create([
        Question(
            question=f'Test question {i + 1}',
            points=points,
            question_type=question_type,
            quiz=quiz
        ) for i in range(nr)
    ])


def create_answers(nr: int, is_right: bool, question: Question):
    return Answer.objects.bulk_create([
        Answer(
            answer=f'Test answer {i + 1}',
            is_right=is_right,
            question=question,
        ) for i in range(nr)
    ])

# def populate_before_rank_test(self):
#     quizzes = QuizViewsTestCase.create_quizzes(2)
#     QuizViewsTestCase.create_questions(nr=1, data={'points': 15, 'question_type': 1, 'quiz': quizzes[1]})
    # user_1 = User.objects.get(id=2)
    # user_2 = User.objects.get(id=3)
    #
    # question_1 = Question.objects.create(question='Test question 1', points=15, question_type=1, quiz=quizzes[1])
    # answer_1 = Answer.objects.create(answer='Test answer 1 for question 1', is_right=True, question=question_1)
    # answer_2 = Answer.objects.create(answer='Test answer 2 for question 1', is_right=False, question=question_1)
    #
    # user_answer = UserAnswer.objects.create(answer=answer_1, user=user_1)
    # user_answer = UserAnswer.objects.create(answer=answer_2, user=user_2)
    #
    # question_2 = Question.objects.create(question='Test question 2', points=35, question_type=2, quiz=quizzes[1])
    # answer_3 = Answer.objects.create(answer='Test answer 3 for question 2', is_right=False, question=question_2)
    # answer_4 = Answer.objects.create(answer='Test answer 4 for question 2', is_right=False, question=question_2)
    # answer_5 = Answer.objects.create(answer='Test answer 5 for question 2', is_right=True, question=question_2)
    # answer_6 = Answer.objects.create(answer='Test answer 6 for question 2', is_right=False, question=question_2)
    #
    # user_answer = UserAnswer.objects.create(answer=answer_4, user=user_1)
    # user_answer = UserAnswer.objects.create(answer=answer_5, user=user_2)