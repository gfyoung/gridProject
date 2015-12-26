from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import gridEvent, gridVendor, gridEventVendor


class GridAdminSite(AdminSite):
    site_header = "GridSite Administration"
    site_title = "GridSite Admin"
    index_title = "Grid Admin Home"
    index_template = "gridSiteAdmin/index.html"
    login_template = "gridSiteAdmin/login.html"
    logout_template = "gridSiteAdmin/logout.html"
    password_change_template = "gridSiteAdmin/passwordChangeForm.html"
    password_change_done_template = "gridSiteAdmin/passwordChangeDone.html"


# Abstract base class
class GridModelAdmin(admin.ModelAdmin):
    change_form_template = "gridSiteAdmin/changeForm.html"
    change_list_template = "gridSiteAdmin/changeList.html"
    delete_confirmation_template = "gridSiteAdmin/deleteConfirmation.html"
    delete_selected_confirmation_template = \
        "gridSiteAdmin/deleteSelectedConfirmation.html"
    object_history_template = "trollSiteAdmin/objectHistory.html"


class GridEventAdmin(GridModelAdmin):
    list_display = ('event_name', 'event_location', 'start_date')
    list_filter = ['event_name', 'event_location', 'start_date']


class GridVendorAdmin(GridModelAdmin):
    list_display = ('vendor_name', 'event_count')
    list_filter = ('vendor_name', 'event_count')


class GridEventVendorAdmin(GridModelAdmin):
    list_display = ('grid_event', 'grid_vendor')
    list_filter = ('grid_event', 'grid_vendor')

adminSite = GridAdminSite(name="admin")
adminSite.register(gridEvent, GridEventAdmin)
adminSite.register(gridVendor, GridVendorAdmin)
adminSite.register(gridEventVendor, GridEventVendorAdmin)
