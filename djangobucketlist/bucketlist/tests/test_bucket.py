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
            reverse('bucketlist'))
        self.assertEqual(response.status_code, 200)

    def test_request_for_empty_bucketlist_page(self):
        response = self.client.get(
            '/bucketlist?page=100000')
        # returns the last page available
        self.assertEqual(response.status_code, 200)

    def test_can_make_a_bucketlist(self):
        response = self.client.post(
            reverse('bucketlist'), {
                'name': 'A new bucketlist'
            })
        self.assertEqual(response.status_code, 302)

    def test_error_creating_bucketlist(self):
        response = self.client.post(
            reverse('bucketlist'))
        # should not redirect
        self.assertEqual(response.templates[0].name, 'bucketlist/errors.html')

    def test_edit_bucketlist(self):
        response = self.client.post(
            reverse(
                'bucketlistedit', kwargs={'bucketlistid': self.bucketlist.id}),
            {
                'name': 'This is a changed name'
            })
        self.assertEqual(response.status_code, 302)

    def test_edit_bucketlist_error(self):
        response = self.client.post(
            reverse(
                'bucketlistedit', kwargs={'bucketlistid': self.bucketlist.id}),
            {
                'name': ''
            })
        self.assertEqual(response.templates[0].name, 'bucketlist/errors.html')

    def test_delete_bucketlist(self):
        response = self.client.get(reverse(
            'bucketlistdelete', kwargs={'bucketlistid': self.bucketlist.id}))
        self.assertEqual(response.status_code, 302)

    def test_delete_bucketlist_error(self):
        response = self.client.get(reverse(
            'bucketlistdelete', kwargs={'bucketlistid': 2}))
        self.assertEqual(response.templates[0].name, 'bucketlist/errors.html')


class BucketItemViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.user.set_password('test')
        self.user.save()
        self.user2 = User.objects.create_user(
            username='test2',
            password='test2'
        )
        self.user2.set_password('test2')
        self.user2.save()
        self.login = self.client.login(
            username='test', password='test')
        self.bucketlist = BucketList.objects.create(
            name='test_bucketlist', author=self.user)
        self.bucketlist2 = BucketList.objects.create(
            name='test_bucketlist2', author=self.user2)
        self.bucketitem = BucketlistItem.objects.create(
            name='test_bucketitem', bucketlist=self.bucketlist)
        self.bucketitem2 = BucketlistItem.objects.create(
            name='test_bucketitem', bucketlist=self.bucketlist2)

    def tearDown(self):
        User.objects.all().delete()
        BucketList.objects.all().delete()
        BucketlistItem.objects.all().delete()

    def test_can_add_bucketitem(self):
        response = self.client.post(
            reverse(
                'bucketitem', kwargs={'bucketlistid': self.bucketlist.id}),
            {
                'name': 'A new bucketitem'
            })
        self.assertEqual(response.status_code, 302)

    def test_add_bucketitem_error(self):
        response = self.client.post(
            reverse(
                'bucketitem', kwargs={'bucketlistid': self.bucketlist.id}),
            {
                'name': ''
            })
        self.assertEqual(response.templates[0].name, 'bucketlist/errors.html')

    def test_can_mark_a_task_as_done(self):
        response = self.client.get(
            reverse(
                'bucketitemedit', kwargs={'bucketitemid': self.bucketitem.id}))
        self.assertEqual(response.status_code, 302)

    def test_edit_bucketitem(self):
        response = self.client.post(
            reverse(
                'bucketitemedit', kwargs={'bucketitemid': self.bucketitem.id}),
            {
                'name': 'This is a changed name'
            })
        self.assertEqual(response.status_code, 302)

    def test_edit_bucketitem_error(self):
        response = self.client.post(
            reverse(
                'bucketitemedit', kwargs={'bucketitemid': self.bucketitem.id}),
            {
                'name': ''
            })
        self.assertEqual(response.templates[0].name, 'bucketlist/errors.html')

    def test_edit_unauthorized_bucketitem(self):
        response = self.client.get(
            reverse(
                'bucketitemedit', kwargs={
                    'bucketitemid': self.bucketitem2.id
                }))

        self.assertEqual(response.templates[0].name, 'bucketlist/errors.html')

    def test_can_delete_a_bucketitem(self):
        response = self.client.get(
            reverse(
                'bucketitemdelete', kwargs={
                    'bucketitemid': self.bucketitem.id}))
        self.assertEqual(response.status_code, 302)

    def test_delete_unauthorized_bucketitem(self):
        response = self.client.get(
            reverse(
                'bucketitemdelete', kwargs={
                    'bucketitemid': self.bucketitem2.id
                }))

        self.assertEqual(response.templates[0].name, 'bucketlist/errors.html')
