""" Unit test for bucklist and bucketitem routes"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from bucketlist.models import BucketList, BucketlistItem


class BucketlistViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.user.set_password('test')
        self.user.save()
        self.login = self.client.login(
            username='test', password='test')
        self.bucketlist = BucketList.objects.create(
            name='test_bucketlist', author=self.user)

    def tearDown(self):
        User.objects.all().delete()
        BucketList.objects.all().delete()

    def test_can_reach_bucketlist_page(self):
        self.assertEqual(self.login, True)
        response = self.client.get(
            reverse('bucketlist', kwargs={'username': 'test'}))
        self.assertEqual(response.status_code, 200)

    def test_request_for_empty_bucketlist_page(self):
        response = self.client.get(
            '/bucketlist/test?page=100000')
        # returns the last page available
        self.assertEqual(response.status_code, 200)

    def test_request_for_unauthorized_bucketlist_page(self):
        response = self.client.get(
            '/bucketlist/anotheruser')
        # returns the error page
        self.assertEqual(response.template_name[0], 'bucketlist/errors.html')

    def test_can_make_a_bucketlist(self):
        response = self.client.post(
            reverse('bucketlist', kwargs={'username': 'test'}), {
                'name': 'A new bucketlist'
            })
        self.assertEqual(response.status_code, 302)

    def test_error_creating_bucketlist(self):
        response = self.client.post(
            reverse('bucketlist', kwargs={'username': 'test'}))
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist(self):
        response = self.client.delete(reverse(
            'bucketlist', kwargs={'username': 'test'}),
            'pk={}'.format(self.bucketlist.id))
        self.assertEqual(response.status_code, 200)


class BucketItemViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.user.set_password('test')
        self.user.save()
        self.login = self.client.login(
            username='test', password='test')
        self.bucketlist = BucketList.objects.create(
            name='test_bucketlist', author=self.user)
        self.bucketitem = BucketlistItem.objects.create(
            name='test_bucketitem', bucketlist=self.bucketlist)

    def tearDown(self):
        User.objects.all().delete()
        BucketList.objects.all().delete()
        BucketlistItem.objects.all().delete()

    def test_can_reach_bucketitems_page(self):
        self.assertEqual(self.login, True)
        response = self.client.get(
            reverse('bucketitem', kwargs={'bucketlistid': self.bucketlist.id}))
        self.assertEqual(response.status_code, 200)

    def test_request_for_empty_bucketitem_page(self):
        response = self.client.get(
            '/bucketlist/{}/bucketitem?page=100000'.format(self.bucketlist.id))
        # returns the last page available
        self.assertEqual(response.status_code, 200)

    def test_request_for_unauthorized_bucketitem_page(self):
        # request for bucketlist id not associated with current user id
        response = self.client.get(
            '/bucketlist/2/bucketitem')
        # returns the error page
        self.assertEqual(response.template_name[0], 'bucketlist/errors.html')

    def test_can_add_bucketitem(self):
        response = self.client.post(
            reverse(
                'bucketitem', kwargs={'bucketlistid': self.bucketlist.id}),
            {
                'name': 'A new bucketitem'
            })
        self.assertEqual(response.status_code, 200)

    def test_can_mark_a_task_as_done(self):
        response = self.client.put(
            reverse(
                'bucketitem', kwargs={'bucketlistid': self.bucketlist.id}),
            'pk={}'.format(self.bucketitem.id))
        self.assertEqual(response.status_code, 200)

    def test_can_delete_a_bucketitem(self):
        response = self.client.delete(
            reverse(
                'bucketitem', kwargs={'bucketlistid': self.bucketlist.id}),
            'pk={}'.format(self.bucketitem.id))
        self.assertEqual(response.status_code, 200)
