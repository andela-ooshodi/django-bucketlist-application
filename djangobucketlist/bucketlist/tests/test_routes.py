from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse


class AuthenticationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username='lade',
            password='lade',
        )

    def test_can_reach_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_right_view_for_index_is_returned(self):
        match = resolve('/')
        self.assertEqual(match.url_name, 'index')

    def test_login(self):
        response = self.client.post('/login', {
            'username': 'lade',
            'password': 'lade'
        })
        self.assertEqual(response.status_code, 302)

    def test_registration(self):
        response = self.client.post('/register', {
            'username': 'laddeos',
            'password': 'laddeos',
            'verify_password': 'laddeos',
        })
        self.assertEqual(response.status_code, 302)
