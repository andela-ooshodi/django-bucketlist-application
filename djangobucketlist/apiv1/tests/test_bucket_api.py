from rest_framework.test import APITestCase, APIClient
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from bucketlist.models import BucketList, BucketlistItem
from rest_framework.authtoken.models import Token


class BuckListApiTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.user.set_password('test')
        self.user.save()
        self.bucket = BucketList.objects.create(
            name='test_bucketlist', author=self.user)

        # generate token for the user
        token = Token.objects.get(user_id=self.user.id)
        # Include appropriate 'Authorization:' header on al request
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def tearDown(self):
        User.objects.all().delete()
        BucketList.objects.all().delete()

    # test can get all bucketlist created
    def test_get_bucketlist(self):
        url = reverse('bucketlistapi')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test can create bucket
    def test_post_bucketlist(self):
        url = reverse('bucketlistapi')
        data = {'name': 'This is a test bucketlist'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    # test can create a bucketitem_error
    def test_post_bucketlist_error(self):
        url = reverse('bucketlistapi')
        data = {'nam': 'This is an error'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    # test can get a bucket from bucketlist
    def test_get_a_bucketlist(self):
        url = reverse(
            'bucketlistapidetail', kwargs={'bucketlistid': self.bucket.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test can get a bucket from bucketlist error
    def test_get_a_bucketlist_error(self):
        url = reverse(
            'bucketlistapidetail', kwargs={'bucketlistid': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # test can edit a bucket
    def test_edit_a_bucketlist(self):
        url = reverse(
            'bucketlistapidetail', kwargs={'bucketlistid': self.bucket.id})
        data = {'name': 'I just changed this bucket\'s name'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

    # test can edit a bucket error
    def test_edit_a_bucketlist_error(self):
        url = reverse(
            'bucketlistapidetail', kwargs={'bucketlistid': self.bucket.id})
        data = {'nam': 'This is an error'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 400)

    # test can delete a bucket
    def test_delete_a_bucketlist(self):
        url = reverse(
            'bucketlistapidetail', kwargs={'bucketlistid': self.bucket.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class BucketlistItemApiTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.user.set_password('test')
        self.user.save()
        self.bucket = BucketList.objects.create(
            name='test_bucketlist', author=self.user)
        self.bucketitem = BucketlistItem.objects.create(
            name='test_bucketitem', bucketlist=self.bucket)

        # generate token for the user
        token = Token.objects.get(user_id=self.user.id)
        # Include appropriate 'Authorization:' header on al request
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def tearDown(self):
        User.objects.all().delete()
        BucketList.objects.all().delete()
        BucketlistItem.objects.all().delete()

    # test to create a bucketitem
    def test_post_bucketitem(self):
        url = reverse('bucketitemapi', kwargs={'bucketlistid': self.bucket.id})
        data = {'name': 'This is a test item'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    # test to create a bucketitem_error
    def test_post_bucketitem_error(self):
        url = reverse('bucketitemapi', kwargs={'bucketlistid': self.bucket.id})
        data = {'nam': 'This is an error'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    # test to create a bucketitem_in_wrong_bucket_error
    def test_post_bucketitem_in_wrong_bucket_error(self):
        url = reverse('bucketitemapi', kwargs={'bucketlistid': 100})
        data = {'name': 'This is an error'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

    # test to get a bucketitem
    def test_get_bucketitem(self):
        url = reverse(
            'bucketitemapidetail', kwargs={
                'bucketlistid': self.bucket.id,
                'bucketitemid': self.bucketitem.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test to get a bucketitem error
    def test_get_bucketitem_error(self):
        url = reverse(
            'bucketitemapidetail', kwargs={
                'bucketlistid': self.bucket.id,
                'bucketitemid': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # test edit a bucketitem
    def test_edit_bucketitem(self):
        url = reverse(
            'bucketitemapidetail', kwargs={
                'bucketlistid': self.bucket.id,
                'bucketitemid': self.bucketitem.id})
        data = {'name': 'This is a test bucketitem',
                'done': True}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

    # test edit a bucketitem done field alone
    def test_edit_bucketitem_done(self):
        url = reverse(
            'bucketitemapidetail', kwargs={
                'bucketlistid': self.bucket.id,
                'bucketitemid': self.bucketitem.id})
        data = {'done': True}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

    # test edit a bucketitem error
    def test_edit_bucketitem_error(self):
        url = reverse(
            'bucketitemapidetail', kwargs={
                'bucketlistid': self.bucket.id,
                'bucketitemid': self.bucketitem.id})
        data = {'done': 'done'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 400)

    # test delete a bucketitem
    def test_delete_bucketitem(self):
        url = reverse(
            'bucketitemapidetail', kwargs={
                'bucketlistid': self.bucket.id,
                'bucketitemid': self.bucketitem.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
