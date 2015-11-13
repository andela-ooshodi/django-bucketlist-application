from django.conf.urls import url
from apiv1 import views

urlpatterns = [
    url(r'^bucketlists$', views.BucketListView.as_view(),
        name='bucketlistapi'),
    url(r'^bucketlists/(?P<bucketlistid>[0-9]+)$',
        views.BucketListEditView.as_view(),
        name='bucketlistedit'),
    url(r'^bucketlists/(?P<bucketlistid>[0-9]+)/items$',
        views.BucketItemView.as_view(),
        name='bucketitemapi'),
    url(r'^bucketlists/(?P<bucketlistid>[0-9]+)/items/(?P<bucketitemid>[0-9]+)$',
        views.BucketItemEditView.as_view(),
        name='bucketitemedit'),
]
