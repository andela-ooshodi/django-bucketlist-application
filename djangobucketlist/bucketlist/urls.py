"""
URL config for accessing views of the bucketlist app
"""

from django.conf.urls import url
from bucketlist.views import view_authentication, view_bucketlist

urlpatterns = [
    url(r'^$', view_authentication.IndexView.as_view(), name='index'),
    url(r'^login$', view_authentication.LoginView.as_view(), name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register$', view_authentication.RegistrationView.as_view(),
        name='register'),
    url(r'^bucketlist$', view_bucketlist.BucketListView.as_view(),
        name='bucketlist'),
    url(r'^bucketlist/(?P<bucketlistid>[0-9]+)/bucketitem$',
        view_bucketlist.BucketItemView.as_view(), name='bucketitem'),
]
