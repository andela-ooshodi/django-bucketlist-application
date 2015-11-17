from rest_framework.test import APITestCase, APIClient
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class UsersTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.user.set_password('test')
        self.user.save()

    def tearDown(self):
        User.objects.all().delete()

    # test can view all registered users through the API
    def test_users_view(self):
        url = reverse('apiusers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test can view a single registered user
    def test_user_view(self):
        url = reverse('apiuser', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test can recceive token
    def test_login(self):
        url = reverse('apilogin')
        data = {'username': 'test', 'password': 'test'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
