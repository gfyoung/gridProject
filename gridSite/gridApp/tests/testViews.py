from gridApp.vendorUtil import getVendorInfo, getStartDate, \
    getUpcomingEvents, getPastEvents, getVendorsForEvent
from gridApp.models import gridEvent, \
    gridVendor, gridEventVendor
from gridApp.views import needToUpdate
from datetime import datetime, timedelta
from django.test import TestCase
from django.conf import settings
from pytz import timezone
from json import dump

import os
import unittest


class BasicUrlAccessTestCase(TestCase):
    missingDataMsg = "Expected data not found"

    def testGetBackSlash(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashGridApp(self):
        response = self.client.get("/gridApp/")
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashGridAppHome(self):
        response = self.client.get("/gridApp/home")
        data = "Welcome to the Off the Grid SF Search Homepage!"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    def testGetBackSlashGridAppAbout(self):
        response = self.client.get("/gridApp/about")
        data = "The purpose of this web application is to facilitate"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    @unittest.skip("need Facebook auth")
    def testGetBackSlashEventId(self):
        response = self.client.get("/gridApp/event/1")
        data = "Participating Vendors"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    @unittest.skip("need Facebook auth")
    def testGetBackSlashEventAll(self):
        response = self.client.get("/gridApp/event/all")
        data = "Upcoming Events"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    @unittest.skip("need Facebook auth")
    def testGetBackSlashVendorId(self):
        response = self.client.get("/gridApp/vendor/1")
        data = "Vendor Information"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    @unittest.skip("need Facebook auth")
    def testGetBackSlashVendorAll(self):
        response = self.client.get("/gridApp/vendor/all")
        data = "List of Current Vendors"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)


class VendorUtilTestCase(unittest.TestCase):
    def testGetVendorInfo(self):
        actualData = getVendorInfo(mockData=True)
        expectedData = [
            ("mockVendorOne", "http://mockVendorOne.com/", "mockVendorOne.jpg"),
            ("mockVendorTwo", "http://mockVendorTwo.com/", "mockVendorTwo.jpg"),
            ("mockVendorThree", "http://mockVendorThree.com/", "mockVendorThree.jpg"),
            ("mockVendorFour", "http://mockVendorFour.com/", "mockVendorFour.jpg"),
            ("mockVendorFive", "http://mockVendorFive.com/", "mockVendorFive.jpg")
        ]

        index = 0
        msg = "{0} != {1}"

        for (vendorName, vendorLink, vendorImg) in actualData:
            try:
                actualVendorName, actualVendorLink, actualVendorImg = expectedData[index]

                self.assertEqual(vendorName, actualVendorName,
                                 msg=msg.format(vendorName, actualVendorName))
                self.assertEqual(vendorLink, actualVendorLink,
                                 msg=msg.format(vendorLink, actualVendorLink))
                self.assertEqual(vendorImg, actualVendorImg,
                                 msg=msg.format(vendorImg, actualVendorImg))

                index += 1

            except IndexError:
                raise Exception("Expected {0} data points but got more"
                                .format(len(expectedData)))

    def testGetStartDate(self):
        now = datetime.now(tz=timezone(settings.TIME_ZONE))
        pacNow = now.astimezone(tz=timezone('US/Pacific'))

        mockEvent = {'start_time': str(now)}
        startDate = getStartDate(mockEvent)

        msg = "{0} != {1}"
        self.assertEqual(startDate, pacNow, msg.format(startDate, pacNow))

    def testGetUpcomingEvents(self):
        now = datetime.now(tz=timezone(settings.TIME_ZONE))

        mockData = {
            'data': [
                {
                    'name': 'eventOne',
                    'start_time': str(now + timedelta(days=5)),
                    'location': 'locOne',
                    'description': 'descrOne'
                },
                {
                    'name': 'eventTwo',
                    'start_time': str(now + timedelta(days=1)),
                    'location': 'locTwo',
                    'description': 'descrTwo'
                },
                {
                    'name': 'eventThree',
                    'start_time': str(now - timedelta(days=5)),
                    'location': 'locThree',
                    'description': 'descrThree'
                }
            ],
            'paging': {
                'next': 'http://www.nextPage.com/'
            }
        }

        mock_upcoming_events_file = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "mockData/mockUpcomingEvents.json"))

        with open(mock_upcoming_events_file, 'w') as f:
            dump(mockData, f)

        expectedData = [
            ('eventOne', str(now + timedelta(days=5)), 'locOne', 'descrOne'),
            ('eventTwo', str(now + timedelta(days=1)), 'locTwo', 'descrTwo')
        ]

        actualData = getUpcomingEvents(now, mockData=True)
        msg = "{0} != {1}"

        self.assertEqual(actualData, expectedData,
                         msg=msg.format(actualData, expectedData))

    def testGetPastEvents(self):
        now = datetime.now(tz=timezone(settings.TIME_ZONE))
        daysAgo = 30

        mockData = {
            'data': [
                {
                    'name': 'eventOne',
                    'start_time': str(now + timedelta(days=5)),
                    'location': 'locOne',
                    'description': 'descrOne'
                },
                {
                    'name': 'eventTwo',
                    'start_time': str(now - timedelta(days=daysAgo - 0)),
                    'location': 'locTwo',
                    'description': 'descrTwo'
                },
                {
                    'name': 'eventThree',
                    'start_time': str(now - timedelta(days=daysAgo - 1)),
                    'location': 'locThree',
                    'description': 'descrThree'
                },
                {
                    'name': 'eventFour',
                    'start_time': str(now - timedelta(days=daysAgo + 5)),
                    'location': 'locFour',
                    'description': 'descrFour'
                }
            ],
            'paging': {
                'next': 'http://www.nextPage.com/'
            }
        }

        mock_upcoming_events_file = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "mockData/mockPastEvents.json"))

        with open(mock_upcoming_events_file, 'w') as f:
            dump(mockData, f)

        expectedData = [
            ('eventTwo', str(now - timedelta(days=daysAgo - 0)), 'locTwo', 'descrTwo'),
            ('eventThree', str(now - timedelta(days=daysAgo - 1)), 'locThree', 'descrThree')
        ]

        actualData = getPastEvents(now, daysAgo=daysAgo, mockData=True)
        msg = "{0} != {1}"

        self.assertEqual(actualData, expectedData,
                         msg=msg.format(actualData, expectedData))

    def testGetVendorsForEvent(self):
        eventDescriptions = [
            'Event Description\nFood vendors: vendorOne\nvendorTwo',
            'Event Description\nFood vendors:\n\n\rvendorOne\nvendorTwo',
            'Event Description\nFood trucks:\n\n\rvendorOne\nvendorTwo',
            'Event Description\nVendor lineup:\n\n\rvendorOne\nvendorTwo',
            'Event Description\nTruck lineup:\n\n\rvendorOne\nvendorTwo',
            'Event Description\nFood vendors:\n\n\rvendorOne\nvendorTo',
            'Event Description\nFood vendors:\n\n\rvendorOne truck\nvendorTwo',
            'Event Description\nFood vendors:\n\n\rvendorOne truck\nvendorTwo',
            'Event Description\nFood vendors:\n\n\rvendorOne vendor\nvendorTwo',
            'Event Description\nFood vendors:\n\n\rvendorOne cart\nvendorTwo',
            'Event Description\nFood vendors:\n\n\rvendorOne trailer\nvendorTwo',
            'Event Description\nFood vendors:\n\n\rvendorOne truck-cart\nvendorTwo',
            'Event Description\nFood vendors:\n\n\rvendorOne\nvendorTo',
            'Event Description\nFood vendors:\n\n\rvendorOne\nvendorTooo',
            'Event Description\nFood vendors:\n\n\rvendorOne\nvendorTooo',
        ]

        eventVendorLists = [
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo', 'vendorToo'],
        ]

        expectedVendorLists = [
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorTwo'],
            ['vendorOne', 'vendorToo'],
        ]
        msg = "{0} --> {1} != {2}"

        for eventDescription, vendorList, expectedVendors in zip(
            eventDescriptions, eventVendorLists, expectedVendorLists
        ):
            actualVendors = getVendorsForEvent(eventDescription, vendorList)
            self.assertEqual(actualVendors, expectedVendors, msg.format(
                eventDescription, actualVendors, expectedVendors))

    def testNeedToUpdateNoEventVendors(self):
        now = datetime.now(tz=timezone(settings.TIME_ZONE))

        event = gridEvent.objects.create(
            event_name='mockEvent',
            event_location='mockLocation',
            start_date=str(now + timedelta(5)))
        event.save()

        self.assertTrue(needToUpdate(now))

    def testNeedToUpdateOldEvent(self):
        now = datetime.now(tz=timezone(settings.TIME_ZONE))

        event = gridEvent.objects.create(
                event_name='mockEvent',
                event_location='mockLocation',
                start_date=str(now - timedelta(5)))
        event.save()

        vendor = gridVendor.objects.create(
            vendor_name='mockVendor',
            vendor_link='mockLink',
            vendor_img='mockImg',
            event_count=999)
        vendor.save()

        eventVendor = gridEventVendor.objects.create(
            grid_event=event,
            grid_vendor=vendor)
        eventVendor.save()

        self.assertTrue(needToUpdate(now))

    def testNeedToUpdateNoUpdateNeed(self):
        now = datetime.now(tz=timezone(settings.TIME_ZONE))

        event = gridEvent.objects.create(
                event_name='mockEvent',
                event_location='mockLocation',
                start_date=str(now + timedelta(5)))
        event.save()

        vendor = gridVendor.objects.create(
                vendor_name='mockVendor',
                vendor_link='mockLink',
                vendor_img='mockImg',
                event_count=999)
        vendor.save()

        eventVendor = gridEventVendor.objects.create(
                grid_event=event,
                grid_vendor=vendor)
        eventVendor.save()

        self.assertFalse(needToUpdate(now))

# TODO: Mock the updateData function in views.py
