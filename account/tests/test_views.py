import json

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class AccountViewsTestCase(APITestCase):
    def setUp(self):
        self.no_permission = {'detail': 'You do not have permission to perform this action.'}
        self.super_user = User.objects.create(
            username='admin_test',
            password='1234',
            is_staff=True,
            is_superuser=True
        )
        self.user_1 = User.objects.create(username='user 1', password='1234')

        admin_refresh_token = RefreshToken.for_user(self.super_user)
        user_1_refresh_token = RefreshToken.for_user(self.user_1)

        self.admin_access_token = str(admin_refresh_token.access_token)
        self.user_1_access_token = str(user_1_refresh_token.access_token)

    def api_authentication(self, access_token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_register_account(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'superstrongpass123',
            'email': 'test_user@gmail.com',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(id=3).email, 'test_user@gmail.com')

    def test_login_user(self):
        user = User.objects.create(username='test_user')
        user.set_password('1234')
        user.save()

        url = reverse('login')
        data = {
            'username': 'test_user',
            'password': '1234',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data.keys())
        self.assertIn('refresh', response.data.keys())

    def test_retrieve_user(self):
        url = reverse('accounts-detail', args='1')

        self.api_authentication(self.admin_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'username': 'admin_test', 'password': '1234', 'email': ''})

        # Switch to user how dont have permission to add quiz
        self.api_authentication(self.user_1_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_list_users(self):
        url = reverse('accounts-list')

        self.api_authentication(self.admin_access_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.api_authentication(self.user_1_access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_update_user(self):
        url = reverse('accounts-detail', args='2')
        initial_data = {'username': 'test_username_changed'}

        self.api_authentication(self.admin_access_token)
        response = self.client.patch(url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=2).username, initial_data['username'])

        self.api_authentication(self.user_1_access_token)
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, self.no_permission)

    def test_delete_user(self):
        url = reverse('accounts-detail', args='2')

        self.api_authentication(self.admin_access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)