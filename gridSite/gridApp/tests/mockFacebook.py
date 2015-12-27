from gridApp.vendorUtil import getVendorInfo, \
    getUpcomingEvents, getPastEvents, getVendorsForEvent
from gridApp.models import gridEvent, \
    gridVendor, gridEventVendor
from datetime import datetime, timedelta
from django.conf import settings
from pytz import timezone


class MockFacebook:
    def __init__(self):
        self.now = datetime.now(
            tz=timezone(settings.TIME_ZONE))

        gridEvent.objects.all().delete()
        gridVendor.objects.all().delete()
        gridEventVendor.objects.all().delete()

        self.vendors = []
        self.pastEvents = []
        self.upcomingEvents = []
        self.pastEventCounts = {}
        self.upcomingEventCounts = {}
        self.upcomingEventsVendorCount = 0

        self.initData()

    def initData(self):
        vendorName = "vendor{0}"
        vendorLink = "link{0}"
        vendorImg = "img{0}"
        vendorCount = 3

        for index in range(vendorCount):
            vendor = (
                vendorName.format(index),
                vendorLink.format(index),
                vendorImg.format(index)
            )

            self.vendors.append(vendor)

        pastEventDescr = "pastDescr{0}\nVendors: {1}"
        pastEventName = "pastEvent{0}"
        pastEventLoc = "pastLoc{0}"
        pastVendors = [
            (-5, ('vendor1',)),
            (-3, ('vendor2',)),
            (-6, ('vendor0', 'vendor2',)),
            (-2, ('vendor2', 'vendor1',)),
            (0, ('vendor2', 'vendor0', 'vendor1')),
        ]

        for index, (timeDelta, eventVendors) in enumerate(pastVendors):
            if timeDelta > 0:
                raise ValueError(("Timedelta for a past "
                                  "event must be non-positive!"))
            pastEvent = (
                pastEventName.format(index),
                str(self.now + timedelta(timeDelta)),
                pastEventLoc.format(index),
                pastEventDescr.format(
                    index, '\n'.join(eventVendors))
            )

            for vendor in eventVendors:
                self.pastEventCounts[vendor] = \
                    self.pastEventCounts.get(vendor, 0) + 1

            self.pastEvents.append(pastEvent)

        futureEventDescr = "futureDescr{0}\nVendors: {1}"
        futureEventName = "Off the Grid: futureEvent{0}"
        futureEventLoc = "futureLoc{0}"
        futureVendors = [
            (1, ('vendor0',)),
            (7, ('vendor1',)),
            (3, ('vendor2', 'vendor0',)),
            (5, ('vendor1', 'vendor2',)),
            (8, ('vendor1', 'vendor2', 'vendor0')),
        ]

        for index, (timeDelta, eventVendors) in enumerate(futureVendors):
            if timeDelta <= 0:
                raise ValueError(("Timedelta for a future "
                                  "event must be positive!"))
            futureEvent = (
                futureEventName.format(index),
                str(self.now + timedelta(timeDelta)),
                futureEventLoc.format(index),
                futureEventDescr.format(
                        index, '\n'.join(eventVendors))
            )

            for vendor in eventVendors:
                self.upcomingEventCounts[vendor] = \
                    self.upcomingEventCounts.get(vendor, 0) + 1

            self.upcomingEvents.append(futureEvent)
            self.upcomingEventsVendorCount += len(eventVendors)

    def getVendorInfo(self):
        return self.vendors

    def getPastEvents(self):
        return self.pastEvents

    def getUpcomingEvents(self):
        return self.upcomingEvents

    def updateData(self):
        gridEvent.objects.all().delete()
        gridVendor.objects.all().delete()
        gridEventVendor.objects.all().delete()

        pastEvents = self.getPastEvents()
        vendorInfo = self.getVendorInfo()

        vendors = [vendorName for (vendorName, vendorImg,
                                   vendorLink) in vendorInfo]
        pastEventCountDict = {vendorName: 0 for vendorName in vendors}

        for eventName, startDate, eventLocation, eventDescription in pastEvents:
            eventVendors = getVendorsForEvent(eventDescription, vendors)

            for eventVendor in eventVendors:
                pastEventCountDict[eventVendor] = pastEventCountDict.get(
                        eventVendor, 0) + 1

        for (vendorName, vendorLink, vendorImg) in vendorInfo:
            grid_vendor = gridVendor(
                    vendor_name=vendorName, vendor_link=vendorLink,
                    vendor_img=vendorImg, event_count=pastEventCountDict[vendorName])
            grid_vendor.save()

        upcomingEvents = self.getUpcomingEvents()

        for (eventName, startDate, eventLocation,
             eventDescription) in upcomingEvents:
            upcomingGridEvent = gridEvent(
                    event_name=eventName.replace(
                            'Off the Grid: ', ''),
                    event_location=eventLocation,
                    start_date=startDate)
            upcomingGridEvent.save()
            eventVendors = getVendorsForEvent(eventDescription, vendors)

            for eventVendor in eventVendors:
                upcomingGridVendor = gridVendor.objects.filter(
                        vendor_name=eventVendor)[0]

                upcomingGridEventVendor = gridEventVendor(
                        grid_event=upcomingGridEvent,
                        grid_vendor=upcomingGridVendor)
                upcomingGridEventVendor.save()
