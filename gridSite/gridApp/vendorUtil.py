from difflib import get_close_matches
from bs4 import BeautifulSoup
from urllib2 import urlopen
from dateutil import parser
from pytz import timezone
from json import loads

import re

events_link = "https://graph.facebook.com/v2.0/129511477069092/events?" \
              "access_token={0}&fields=name,location,description"
oauth_access_token = '1576169779295502|gO5N6nnuHe3m-RQBNKsOKO6xzt8'
vendor_link = "http://offthegridsf.com/vendors#food"


def getVendorInfo():
    conn = urlopen(vendor_link, None)
    html = conn.read()
    soup = BeautifulSoup(html, 'html.parser')

    foodVendors = soup.find_all(**{'id': 'food-tab'})
    vendorNames = foodVendors[0].find_all(**{'class': 'otg-vendor-logo'})
    vendorLinks = foodVendors[0].find_all(**{'class': 'otg-vendor-logo-link'})

    return zip([vendorName.get('alt').strip() for vendorName in vendorNames],
               [vendorLink.get('href').strip() for vendorLink in vendorLinks],
               [vendorName.get('src').strip() for vendorName in vendorNames])


def getStartDate(event):
    dateString = parser.parse((event['start_time']))
    return dateString.astimezone(tz=timezone('US/Pacific'))


def getUpcomingEvents(today):
    currentEventsLink = events_link.format(oauth_access_token)
    upcomingEvents = []

    while True:
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


def getPastEvents(today, daysAgo=30):
    currentEventsLink = events_link.format(oauth_access_token)
    pastEvents = []

    while True:
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
