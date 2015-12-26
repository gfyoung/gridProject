from difflib import get_close_matches
from bs4 import BeautifulSoup
from dateutil import parser
from pytz import timezone
from json import loads

# Python 3 compatibility
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

import os
import re

html_parser = 'html.parser'

events_link = "https://graph.facebook.com/v2.0/129511477069092/events?" \
              "access_token={0}&fields=name,location,description"
oauth_access_token = '1576169779295502|gO5N6nnuHe3m-RQBNKsOKO6xzt8'
vendor_link = "http://offthegridsf.com/vendors#food"

mock_vendor_link = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "tests/mockData/mockVendors.html"))
mock_upcoming_events_file = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "tests/mockData/mockUpcomingEvents.json"))
mock_past_events_file = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "tests/mockData/mockPastEvents.json"))


def getVendorInfo(mockData=False):
    if mockData:
        with open(mock_vendor_link, 'r') as html:
            soup = BeautifulSoup(html, html_parser)
    else:
        conn = urlopen(vendor_link, None)
        html = conn.read()
        soup = BeautifulSoup(html, html_parser)

    foodVendors = soup.find_all(**{'id': 'food-tab'})
    vendorNames = foodVendors[0].find_all(**{'class': 'otg-vendor-logo'})
    vendorLinks = foodVendors[0].find_all(**{'class': 'otg-vendor-logo-link'})

    return zip([vendorName.get('alt').strip() for vendorName in vendorNames],
               [vendorLink.get('href').strip() for vendorLink in vendorLinks],
               [vendorName.get('src').strip() for vendorName in vendorNames])


def getStartDate(event):
    dateString = parser.parse((event['start_time']))
    return dateString.astimezone(tz=timezone('US/Pacific'))


def getUpcomingEvents(today, mockData=False):
    currentEventsLink = events_link.format(oauth_access_token)
    upcomingEvents = []
    eventsData = None

    while True:
        if mockData:
            if eventsData is None:
                with open(mock_upcoming_events_file, 'r') as f:
                    eventsData = loads(f.read())
                    eventsInfo = eventsData['data']

        else:
            conn = urlopen(currentEventsLink, None)
            eventsData = loads(conn.read())
            eventsInfo = eventsData['data']

        for event in eventsInfo:
            if getStartDate(event) > today:
                upcomingEvents.append((
                    event['name'], event['start_time'],
                    event['location'], event['description']
                ))

            else:
                return upcomingEvents

        currentEventsLink = eventsData['paging']['next']


def getPastEvents(today, daysAgo=30, mockData=False):
    currentEventsLink = events_link.format(oauth_access_token)
    pastEvents = []
    eventsData = None

    while True:
        if mockData:
            if eventsData is None:
                with open(mock_past_events_file, 'r') as f:
                    eventsData = loads(f.read())
                    eventsInfo = eventsData['data']

        else:
            conn = urlopen(currentEventsLink, None)
            eventsData = loads(conn.read())
            eventsInfo = eventsData['data']

        for event in eventsInfo:
            if getStartDate(event) <= today and \
               (today - getStartDate(event)).days <= daysAgo:
                pastEvents.append((
                    event['name'], event['start_time'],
                    event['location'], event['description']
                ))

            elif (today - getStartDate(event)).days > daysAgo:
                return pastEvents

        currentEventsLink = eventsData['paging']['next']


# This function was written to be very attuned to the
# event descriptions provided from the Facebook API and
# attempts to clean-up the data as best as possible based
# on sampled descriptions. This algorithm may break in the
# future in the event that new types of typing or spelling
# errors are introduced into the data.
def getVendorsForEvent(eventDescription, vendorList):
    pattern = re.compile('.*vendor.*:|.*truck.*:|.*lineup.*:',
                         flags=re.IGNORECASE)
    target = pattern.findall(eventDescription)[-1]

    eventDescription = re.sub(target, 'SPLIT HERE', eventDescription)
    eventDescription = eventDescription.split('SPLIT HERE')[1].strip()

    eventDescription = re.sub('\r', '', eventDescription)
    eventDescription = re.sub('\n+\n', 'SPLIT HERE', eventDescription)

    eventDescription = eventDescription.split('SPLIT HERE')[0]
    eventDescription = eventDescription.split('\n')

    pattern = re.compile('\W+.?truck.?|\W+.?vendor.?|\W+.?cart.?|'
                         '\W+.?trailer.?', flags=re.IGNORECASE)
    eventVendors = []

    for eventVendor in eventDescription:
        eventVendor = eventVendor.strip()

        if eventVendor:
            matches = pattern.findall(eventVendor)

            for match in matches:
                eventVendor = eventVendor.replace(match, '')

            eventVendor = get_close_matches(eventVendor, vendorList, 1)

            if eventVendor:
                eventVendors.append(eventVendor[0])

    return eventVendors
