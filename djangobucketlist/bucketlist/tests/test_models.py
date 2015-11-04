from django.test import TestCase
from bucketlist.models import BucketList, BucketlistItem
from django.contrib.auth.models import User

class BucketlistModelsTestCase(TestCase):

    def setUp(self):
        bucketlist = BucketList()

    def test_bucketlist(self):
        pass