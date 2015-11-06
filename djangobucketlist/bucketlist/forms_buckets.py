from django.forms import ModelForm

from bucketlist.models import BucketList, BucketlistItem


class BucketListForm(ModelForm):

    class Meta:
        model = BucketList
        fields = ['name']


class BucketlistItemForm(ModelForm):

    class Meta:
        model = BucketlistItem
        fields = ['name', 'done']
