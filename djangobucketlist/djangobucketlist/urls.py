from django.conf.urls import include, url
from django.contrib import admin
import bucketlist.urls
import apiv1.urls

urlpatterns = [
    url(r'^', include(bucketlist.urls)),
    url(r'^apiv1/', include(apiv1.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^apiv1-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]
