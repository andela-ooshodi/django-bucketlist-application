""" Unit test for authentication routes"""

from django.test import TestCase, Client
from django.contrib.auth.models import User


class AuthenticationTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='test',
            password='test',
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_can_reach_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/login', {
            'username': 'test',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 302)

    def test_empty_login_form(self):
        response = self.client.post('/login')
        # should not redirect but return the same page
        self.assertEqual(response.status_code, 200)

    def test_login_error(self):
        response = self.client.post('/login', {
            'username': 'wrong_name',
            'password': 'wrong_password'
        })
        # should redirect back to index page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login')

    def test_redirect_logged_in_user(self):
        self.client.login(
            username='test', password='test')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_registration(self):
        response = self.client.post('/register', {
            'username': 'new_test',
            'password': 'test',
            'verify_password': 'test'
        })
        self.assertEqual(response.status_code, 302)

    def test_register_already_registered_user(self):
        response = self.client.post('/register', {
            'username': 'test',
            'password': 'test',
            'verify_password': 'test'
        })
        # redirect to index page with an error message
        self.assertEqual(response.status_code, 302)

    def test_registration_error(self):
        response = self.client.post('/register', {
            'username': 'test_user',
            'password': 'password',
            'verify_password': 'different'
        })
        # redirect to index page with an error message
        self.assertEqual(response.status_code, 302)
