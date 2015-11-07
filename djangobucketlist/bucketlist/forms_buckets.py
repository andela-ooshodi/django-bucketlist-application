from django.forms import ModelForm

from bucketlist.models import BucketList, BucketlistItem


class BaseForm(ModelForm):

    class Meta:
        fields = ['name']


class BucketListForm(BaseForm):

    class Meta(BaseForm.Meta):
        model = BucketList


class BucketlistItemForm(BaseForm):

    class Meta(BaseForm.Meta):
        model = BucketlistItem
