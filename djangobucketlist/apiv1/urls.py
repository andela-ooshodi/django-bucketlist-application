from django.conf.urls import url
from apiv1 import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
