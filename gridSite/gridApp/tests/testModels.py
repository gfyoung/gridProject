from pytz import timezone
from datetime import datetime
from django.conf import settings
from django.test import TestCase
from gridApp.models import gridEvent, gridVendor, gridEventVendor


class GridEventTestCase(TestCase):
    def setUp(self):
        gridEvent.objects.all().delete()
        gridEvent.objects.create(event_name="testEvent",
                                 event_location="testLoc",
                                 start_date=str(
                                     datetime.now(tz=timezone(
                                             settings.TIME_ZONE)
                                     )
                                 ))

    def testUnicode(self):
        testEvent = gridEvent.objects.get(event_name="testEvent")
        self.assertEqual(unicode(testEvent), "testEvent")


class GridVendorTestCase(TestCase):
    def setUp(self):
        gridVendor.objects.all().delete()
        gridVendor.objects.create(vendor_name="testVendor",
                                  vendor_link="testLink.com",
                                  vendor_img="testImg.png",
                                  event_count=30)

    def testUnicode(self):
        testVendor = gridVendor.objects.get(vendor_name="testVendor")
        self.assertEqual(unicode(testVendor), "testVendor")


class GridEventVendorTestCase(TestCase):
    def setUp(self):
        gridEvent.objects.all().delete()
        gridVendor.objects.all().delete()
        gridEventVendor.objects.all().delete()

        testGridEvent = gridEvent.objects.create(
            event_name="testEvent",
            event_location="testLoc",
            start_date=str(
                    datetime.now(tz=timezone(
                            settings.TIME_ZONE)
                    )
            )
        )
        testGridVendor = gridVendor.objects.create(
            vendor_name="testVendor",
            vendor_link="testLink.com",
            vendor_img="testImg.png",
            event_count=30
        )
        gridEventVendor.objects.create(
            grid_event=testGridEvent,
            grid_vendor=testGridVendor
        )

    def testUnicode(self):
        testEventVendor = gridEventVendor.objects.get(pk=1)
        self.assertEqual(unicode(testEventVendor), "testVendor for testEvent")
