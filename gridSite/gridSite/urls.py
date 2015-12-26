from django.conf.urls.static import static
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/gridApp/', permanent=False)),
    url(r'^gridApp/', include('gridApp.urls', namespace='gridApp')),
    url(r'^admin/', include(admin.site.urls)),
] + static(r'^static/(?P<path>.*)$', document_root='trollApp/static')
