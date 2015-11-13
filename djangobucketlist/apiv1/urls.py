from django.conf.urls import url
from apiv1 import views_buckets, views_users

urlpatterns = [
    url(r'^bucketlists$', views_buckets.BucketListView.as_view(),
        name='bucketlistapi'),
    url(r'^bucketlists/(?P<bucketlistid>[0-9]+)$',
        views_buckets.BucketListEditView.as_view(),
        name='bucketlistedit'),
    url(r'^bucketlists/(?P<bucketlistid>[0-9]+)/items$',
        views_buckets.BucketItemView.as_view(),
        name='bucketitemapi'),
    url(r'^bucketlists/(?P<bucketlistid>[0-9]+)/items/(?P<bucketitemid>[0-9]+)$',
        views_buckets.BucketItemEditView.as_view(),
        name='bucketitemedit'),
    url(r'^users$', views_users.UsersView.as_view(), name='users'),
    url(r'^users/(?P<pk>[0-9]+)$',
        views_users.UsersDetailView.as_view(), name='user')
]
