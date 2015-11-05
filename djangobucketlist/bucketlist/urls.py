"""
URL config for accessing views of the bucketlist app
"""

from django.conf.urls import url
from bucketlist import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register$', views.RegistrationView.as_view(), name='register'),
    url(r'^home$', views.HomeView.as_view(), name='home'),
]
