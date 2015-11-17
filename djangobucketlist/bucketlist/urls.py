"""
URL config for accessing views of the bucketlist app
"""

from django.conf.urls import url
from bucketlist.views import view_authentication, view_buckets

urlpatterns = [
    url(r'^$', view_authentication.IndexView.as_view(), name='index'),
    url(r'^login$', view_authentication.LoginView.as_view(), name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register$', view_authentication.RegistrationView.as_view(),
        name='register'),
    url(r'^bucketlist$', view_buckets.BucketListView.as_view(),
        name='bucketlist'),
    url(r'^bucketlist/(?P<bucketlistid>[0-9]+)/edit$',
        view_buckets.BucketListEditView.as_view(), name='bucketlistedit'),
    url(r'^bucketlist/(?P<bucketlistid>[0-9]+)/delete$',
        view_buckets.BucketListDeleteView.as_view(),
        name='bucketlistdelete'),
    url(r'^bucketlist/(?P<bucketlistid>[0-9]+)/bucketitems$',
        view_buckets.BucketItemView.as_view(), name='bucketitem'),
    url(r'^bucketitem/(?P<bucketitemid>[0-9]+)/edit$',
        view_buckets.BucketItemEditView.as_view(), name='bucketitemedit'),
    url(r'^bucketitem/(?P<bucketitemid>[0-9]+)/delete$',
        view_buckets.BucketItemDeleteView.as_view(), name='bucketitemdelete'),
]
