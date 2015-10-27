from django.views.generic.base import RedirectView
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', RedirectView.as_view(url = '/gridApp/', permanent = False)),
    url(r'^gridApp/', include('gridApp.urls', namespace = 'gridApp')),
    url(r'^admin/', include(admin.site.urls)),
]
