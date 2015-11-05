from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve


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

    def test_login(self):
        response = self.client.post('/login', {
            'username': 'lade',
            'password': 'lade'
        })
        self.assertEqual(response.status_code, 302)
