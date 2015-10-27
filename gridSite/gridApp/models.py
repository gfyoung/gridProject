from django.db import models


class gridEvent(models.Model):
    event_name = models.CharField(max_length=1000)
    event_location = models.CharField(max_length=1000)
    start_date = models.DateTimeField()

    def __unicode__(self):
        return self.event_name


class gridVendor(models.Model):
    vendor_name = models.CharField(max_length=1000)
    vendor_link = models.CharField(max_length=1000)
    vendor_img = models.CharField(max_length=1000)
    event_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.vendor_name


class gridEventVendor(models.Model):
    grid_event = models.ForeignKey(gridEvent)
    grid_vendor = models.ForeignKey(gridVendor)

    def __unicode__(self):
        return "{} for {}".format(self.grid_vendor.vendor_name,
                                  self.grid_event.event_name)
