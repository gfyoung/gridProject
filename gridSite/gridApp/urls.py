from django.views.generic.base import RedirectView
from django.conf.urls import patterns, url
from gridApp import views

urlpatterns = patterns('',
    url(r'^$', views.displayWelcome, name = 'home'),
    url(r'^about$', views.displayAbout, name = 'about'),
    url(r'^event/(?P<event_id>\d+$)', views.displayEventVendors, name = 'eventVendors'),
    url(r'^event/all$', views.displayUpcomingEvents, name = 'eventsAll'),
    url(r'^vendor/(?P<vendor_id>\d+)$', views.displayVendorInfo, name = 'vendorEvents'),
    url(r'^vendor/all$', views.displayAllVendors, name = 'vendorsAll'),
)
