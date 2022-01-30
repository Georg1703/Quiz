import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import Quiz, Question, Answer, UserAnswer
from quiz.tests import service


class BaseTestCase(APITestCase):

    def setUp(self):
        self.no_permission = {'detail': 'You do not have permission to perform this action.'}
        self.super_user = User.objects.create(
            username='admin_test',
            password='1234',
            is_staff=True,
            is_superuser=True
        )
        self.user_1 = User.objects.create(username='user 1', password='1234')
        self.user_2 = User.objects.create(username='user 2', password='1234')

        admin_refresh_token = RefreshToken.for_user(self.super_user)
        user_1_refresh_token = RefreshToken.for_user(self.user_1)
        user_2_refresh_token = RefreshToken.for_user(self.user_2)

        self.admin_access_token = str(admin_refresh_token.access_token)
        self.user_1_access_token = str(user_1_refresh_token.access_token)
        self.user_2_access_token = str(user_2_refresh_token.access_token)

    def api_authentication(self, access_token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)


class QuizViewsTestCase(BaseTestCase):

    def test_create_quiz(self):
        url = reverse("quizzes-list")
        initial_data = {'title': 'Test quiz'}

        self.api_authentication(self.admin_access_token)
        response = self.client.post(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertEqual(response.data['title'], initial_data['title'])
        self.assertTrue(len(response.data) == 3)

        # Switch to user how dont have permission to add quiz
        self.api_authentication(self.user_1_access_token)
        response = self.client.post(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_retrieve_quiz(self):
        service.create_quizzes(2)
        url = reverse("quizzes-detail", args='2')

        self.api_authentication(self.admin_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 4)
        self.assertTrue(response.data['id'] == 2)

        self.api_authentication(self.user_1_access_token)
        url = reverse("quizzes-detail", args='1')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 4)
        self.assertTrue(response.data['id'] == 1)

    def test_list_quizzes(self):
        service.create_quizzes(2)
        url = reverse("quizzes-list")

        self.api_authentication(self.admin_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)
        self.assertEqual(len(response.data[0]), 3)

        self.api_authentication(self.user_1_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)
        self.assertEqual(len(response.data[1]), 3)

    def test_update_quiz(self):
        service.create_quizzes(2)
        url = reverse("quizzes-detail", args='1')
        initial_data = {'title': 'Test quiz changed'}

        self.api_authentication(self.admin_access_token)
        response = self.client.patch(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 3)
        self.assertEqual(response.data['title'], initial_data['title'])

        self.api_authentication(self.user_1_access_token)
        response = self.client.patch(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_delete_quiz(self):
        service.create_quizzes(2)
        url = reverse("quizzes-detail", args='1')

        self.api_authentication(self.admin_access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quiz.objects.count(), 1)

        self.api_authentication(self.user_1_access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)


class QuestionViewsTestCase(BaseTestCase):

    def test_create_question(self):
        quizzes = service.create_quizzes(2)
        url = reverse("questions-list")
        initial_data = {'question': 'Test question', 'points': 35, 'quiz': quizzes[0].id}

        self.api_authentication(self.admin_access_token)
        response = self.client.post(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(response.data['question'], initial_data['question'])
        self.assertTrue(len(response.data) == 6)

        # Switch to user how dont have permission to add question
        self.api_authentication(self.user_1_access_token)
        response = self.client.post(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_retrieve_question(self):
        quizzes = service.create_quizzes(2)
        service.create_questions(2, 35, 2, quizzes[0])
        url = reverse("questions-detail", args='2')

        self.api_authentication(self.admin_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 7)
        self.assertTrue(response.data['id'] == 2)

        self.api_authentication(self.user_1_access_token)
        url = reverse("questions-detail", args='1')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 7)
        self.assertTrue(response.data['id'] == 1)

    def test_list_question(self):
        quizzes = service.create_quizzes(2)
        service.create_questions(2, 35, 2, quizzes[0])
        url = reverse("questions-list")

        self.api_authentication(self.admin_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)
        self.assertEqual(len(response.data[1]), 6)

        self.api_authentication(self.user_1_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)
        self.assertEqual(len(response.data[0]), 6)

    def test_update_question(self):
        quizzes = service.create_quizzes(2)
        service.create_questions(2, 35, 2, quizzes[0])
        url = reverse("questions-detail", args='1')
        initial_data = {'question': 'Test question changed'}

        self.api_authentication(self.admin_access_token)
        response = self.client.patch(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 6)
        self.assertEqual(Question.objects.get(id=1).question, initial_data['question'])

        self.api_authentication(self.user_1_access_token)
        response = self.client.patch(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_delete_question(self):
        quizzes = service.create_quizzes(2)
        service.create_questions(2, 35, 2, quizzes[0])
        url = reverse("questions-detail", args='2')

        self.api_authentication(self.admin_access_token)
        self.client.delete(url)
        response = self.client.delete(reverse("questions-detail", args='1'))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Question.objects.count() == 0)

        self.api_authentication(self.user_1_access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_create_answer_for_question(self):
        quizzes = service.create_quizzes(2)
        questions = service.create_questions(2, 35, 2, quizzes[0])
        service.create_answers(2, False, questions[0])
        url = reverse('questions-detail', args='1') + 'answers/1/'

        self.api_authentication(self.user_1_access_token)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'answer': 1, 'user': 2})
        self.assertEqual(UserAnswer.objects.count(), 1)

    def test_allowed_one_answer_per_question(self):
        quizzes = service.create_quizzes(1)
        questions = service.create_questions(2, 35, 2, quizzes[0])
        service.create_answers(2, False, questions[0])
        url = reverse('questions-detail', args='1')

        self.api_authentication(self.user_1_access_token)
        self.client.post(url + 'answers/1/')
        response = self.client.post(url + 'answers/2/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {
            "non_field_errors": ["Only one answer per question is allowed"]
        })


class AnswerViewsTestCase(BaseTestCase):

    def test_create_answer(self):
        quizzes = service.create_quizzes(2)
        questions = service.create_questions(2, 35, 2, quizzes[0])
        url = reverse("answers-list")
        initial_data = {'answer': 'Test answer', 'question': questions[0].id}

        self.api_authentication(self.admin_access_token)
        response = self.client.post(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(response.data['answer'], initial_data['answer'])
        self.assertEqual(len(response.data), 5)

        # Switch to user how dont have permission to add question
        self.api_authentication(self.user_1_access_token)
        response = self.client.post(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_allowed_2_answer_for_question_type_1(self):
        quizzes = service.create_quizzes(1)
        questions = service.create_questions(2, 35, 1, quizzes[0])
        url = reverse("answers-list")
        initial_data = {'answer': 'Test answer', 'question': questions[0].id}

        self.api_authentication(self.admin_access_token)
        self.client.post(url, initial_data)
        self.client.post(url, initial_data)
        response = self.client.post(url, initial_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'non_field_errors': ['For that type of question are allowed only 2 answers']
        })

    def test_retrieve_answer(self):
        quizzes = service.create_quizzes(2)
        questions = service.create_questions(2, 35, 2, quizzes[0])
        service.create_answers(2, False, questions[0])
        url = reverse("answers-detail", args='2')

        self.api_authentication(self.admin_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 5)
        self.assertTrue(response.data['id'] == 2)

        self.api_authentication(self.user_1_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_list_answers(self):
        quizzes = service.create_quizzes(2)
        questions = service.create_questions(2, 35, 2, quizzes[0])
        service.create_answers(2, False, questions[0])
        url = reverse("answers-list")

        self.api_authentication(self.admin_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)
        self.assertEqual(len(response.data[1]), 5)

        self.api_authentication(self.user_1_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_update_answer(self):
        quizzes = service.create_quizzes(2)
        questions = service.create_questions(2, 35, 2, quizzes[0])
        service.create_answers(2, False, questions[0])
        url = reverse("answers-detail", args='1')
        initial_data = {'answer': 'Test answer changed'}

        self.api_authentication(self.admin_access_token)
        response = self.client.patch(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 5)
        self.assertEqual(Answer.objects.get(id=1).answer, initial_data['answer'])

        self.api_authentication(self.user_1_access_token)
        response = self.client.patch(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_delete_answer(self):
        quizzes = service.create_quizzes(2)
        questions = service.create_questions(2, 35, 2, quizzes[0])
        service.create_answers(2, False, questions[0])
        url = reverse("answers-detail", args='1')

        self.api_authentication(self.admin_access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Answer.objects.count() == 1)

        self.api_authentication(self.user_1_access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)
