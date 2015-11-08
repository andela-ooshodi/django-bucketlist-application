"""Test bucketlist models"""
from django.test import TestCase
from bucketlist.models import BucketList, BucketlistItem
from django.contrib.auth.models import User


class BucketModelsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='test')
        self.bucketlist = BucketList.objects.create(
            name='test_bucketlist', author=self.user)
        self.bucketitem = BucketlistItem.objects.create(
            name='test_bucketitem', bucketlist=self.bucketlist)

    def tearDown(self):
        User.objects.all().delete()
        BucketList.objects.all().delete()
        BucketlistItem.objects.all().delete()

    def test_user_created_successfully(self):
        self.assertEqual(self.user.get_username(), 'test')

    def test_get_bucketlist_from_db(self):
        self.assertTrue(BucketList.objects.all())

    def test_get_bucketitem_from_db(self):
        self.assertTrue(BucketlistItem.objects.all())
