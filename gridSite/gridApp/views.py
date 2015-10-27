from gridApp.vendorUtil import getVendorInfo, getVendorsForEvent, \
     getUpcomingEvents, getPastEvents
from gridApp.models import gridEvent, gridVendor, gridEventVendor
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Min
from django.views import generic
from datetime import datetime
from pytz import timezone

def updateData(today):
    gridEvent.objects.all().delete()
    gridVendor.objects.all().delete()
    gridEventVendor.objects.all().delete()

    pastEvents = getPastEvents(today)
    vendorInfo = getVendorInfo()

    vendors = [vendorName for (vendorName, vendorImg, vendorLink) in vendorInfo]
    pastEventCountDict = {vendorName : 0 for vendorName in vendors}
    
    for eventName, startDate, eventLocation, eventDescription in pastEvents:      
        eventVendors = getVendorsForEvent(eventDescription, vendors)

        for eventVendor in eventVendors:
            pastEventCountDict[eventVendor] = pastEventCountDict.get( \
                eventVendor, 0) + 1

    for (vendorName, vendorLink, vendorImg) in vendorInfo:
        grid_vendor = gridVendor(vendor_name = vendorName, vendor_link = vendorLink,
                                 vendor_img = vendorImg, event_count = pastEventCountDict[vendorName])
        grid_vendor.save()
        
    upcomingEvents = getUpcomingEvents(today)
    
    for eventName, startDate, eventLocation, eventDescription in upcomingEvents:
        upcomingGridEvent = gridEvent(event_name = eventName.replace( \
            'Off the Grid: ', ''), event_location = eventLocation, start_date = startDate)
        upcomingGridEvent.save()
        eventVendors = getVendorsForEvent(eventDescription, vendors)

        for eventVendor in eventVendors:
            upcomingGridVendor = gridVendor.objects \
            .filter(vendor_name = eventVendor)[0]
            
            upcomingGridEventVendor = gridEventVendor(grid_event = upcomingGridEvent, \
                                                      grid_vendor = upcomingGridVendor)
            upcomingGridEventVendor.save()

def needToUpdate(today):
    return gridEventVendor.objects.count() == 0 or gridEvent.objects.aggregate( \
        min_date = Min('start_date'))['min_date'] < today

def checkAndUpdate():
    today = datetime.now(tz = timezone('US/Pacific'))
    
    if needToUpdate(today):
        updateData(today)

def displayWelcome(request):
    return render(request, 'gridApp/welcomeDisplay.html')

def displayAbout(request):
    return render(request, 'gridApp/aboutDisplay.html')

def displayUpcomingEvents(request):
    checkAndUpdate()
    
    upcomingEvents = gridEvent.objects.order_by('start_date')
    context = {'upcomingEvents' : upcomingEvents}
    
    return render(request, 'gridApp/eventAllDisplay.html', context)

def displayEventVendors(request, event_id):
    checkAndUpdate()

    grid_event = gridEvent.objects.get(pk = event_id)        
    eventVendors = gridEventVendor.objects.filter(grid_event = grid_event)
    eventVendors = eventVendors.order_by('-grid_vendor__event_count')
    context = {'eventName'    : grid_event.event_name,
               'eventLocation': grid_event.event_location,
               'eventTime'    : grid_event.start_date,
               'eventVendors' : eventVendors}
    
    return render(request, 'gridApp/eventVendorDisplay.html', context)

def displayVendorInfo(request, vendor_id):
    checkAndUpdate()

    eventVendor = gridVendor.objects.get(pk = vendor_id)
    context = {'vendorName' : eventVendor.vendor_name,
               'vendorLink' : eventVendor.vendor_link,
               'vendorImg'  : eventVendor.vendor_img,
               'vendorEventCount' : eventVendor.event_count}

    return render(request, 'gridApp/vendorEventDisplay.html', context)

def displayAllVendors(request):
    checkAndUpdate()
    
    eventVendors = gridVendor.objects.order_by('-event_count')
    context = {'eventVendors' : eventVendors}

    return render(request, 'gridApp/vendorAllDisplay.html', context)
