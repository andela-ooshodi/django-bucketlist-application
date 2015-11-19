from django.conf.urls import url
from apiv1.views import view_buckets, view_users

urlpatterns = [
    url(r'^login$', view_users.LoginView.as_view(), name='apilogin'),
    url(r'^bucketlists$', view_buckets.BucketListView.as_view(),
        name='bucketlistapi'),
    url(r'^bucketlists/(?P<bucketlistid>[0-9]+)$',
        view_buckets.BucketListDetailView.as_view(),
        name='bucketlistapidetail'),
    url(r'^bucketlists/(?P<bucketlistid>[0-9]+)/items$',
        view_buckets.BucketItemView.as_view(),
        name='bucketitemapi'),
    url(r'^bucketlists/(?P<bucketlistid>[0-9]+)/items/(?P<bucketitemid>[0-9]+)$',
        view_buckets.BucketItemDetailView.as_view(),
        name='bucketitemapidetail'),
    url(r'^users$', view_users.UsersView.as_view(), name='apiusers'),
    url(r'^users/(?P<pk>[0-9]+)$',
        view_users.UsersDetailView.as_view(), name='apiuser'),
]
