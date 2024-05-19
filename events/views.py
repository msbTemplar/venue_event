from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

# create admin_approval page



# show event
def show_event(request, event_id):
    event =Event.objects.get(pk=event_id)
    context = {'event':event}
    return render(request, 'events/show_event.html', context)
#show events in a avenue 

def venue_events(request, venue_id):
    #grab the venue
    
    venue=Venue.objects.get(id=venue_id)
    #grab event forom that venue
    events=venue.event_set.all()
    if events:
        
        context = {'events':events}
        return render(request, 'events/venue_events.html', context)
    else:
        messages.success(request, "That venue has no events")
        return redirect('admin_approval')

def admin_approval(request):
    #get venues
    venue_list=Venue.objects.all()
    
    
    
    
    #get count
    
    event_count=Event.objects.all().count()
    venue_count=Venue.objects.all().count()
    user_count=User.objects.all().count()
    
    event_list = Event.objects.all().order_by('-event_date')
    
    if request.user.is_superuser:
        if request.method == "POST":
            id_list=request.POST.getlist('boxes')
            print(id_list)
            #Uncheck all event
            
            event_list.update(approved=False)
            
            #updpate DB
            
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            
            
            messages.success(request, "Event list approval has been updated")
            return redirect('list-events')
        
        else:
            context = {'event_list': event_list,'event_count':event_count,'venue_count':venue_count,'user_count':user_count,'venue_list':venue_list}
            return render(request, 'events/admin_approval.html', context)
    else:
        messages.success(request, "You arents authorize to view this page")
        return redirect('home')

    return render(request, 'events/admin_approval.html', context)


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        context = {'me': me, 'events': events}

        return render(request, 'events/my_events.html', context)
    else:
        messages.success(request, "Ypur arent auhtorize to view this page")
        return redirect('home')


def venue_pdf(request):
    # creTE BYTESTREAM BUFFER
    buf = io.BytesIO()
    # creatwe canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    venues = Venue.objects.all()

    lines = []
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append('===============================================')

    for line in lines:
        textob.textLine(line)

    # lines=["This is line 1", "This is line 2", "This is line 3"]
    # for line in lines:
        # textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # create csv writer
    writer = csv.writer(response)
    venues = Venue.objects.all()
    # add column header to csv file

    writer.writerow(['Venue Name', 'Address', 'Zip Code',
                    'Phone', 'Web Address', 'Email Address'])

    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code,
                        venue.phone, venue.web, venue.email_address])

    return response


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all()

    # loop throw

    # lines=["This is line 1\n", "This is line 2\n", "This is line 3\n\n"]
    lines = []
    for venue in venues:
        lines.append(
            f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n')

    response.writelines(lines)
    return response


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, "Event deleted??????")
        return redirect('list-events')
    else:
        messages.success(
            request, "Your arent authorized to delete this event??????")
        return redirect('list-events')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    context = {'event': event, 'form': form}
    return render(request, 'events/update_event.html', context)


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None,
                     request.FILES or None,  instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    context = {'venue': venue, 'form': form}
    return render(request, 'events/update_venue.html', context)


def search_venues(request):

    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        context = {'searched': searched, 'venues': venues}
        return render(request, 'events/search_venues.html', context)
    else:
        context = {}
        return render(request, 'events/search_venues.html', context)

    # return render(request, 'events/search_venues.html', context)


def search_events(request):

    if request.method == "POST":
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)
        context = {'searched': searched, 'events': events}
        return render(request, 'events/search_events.html', context)
    else:
        context = {}
        return render(request, 'events/search_events.html', context)


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    
    #grab event forom that venue
    events=venue.event_set.all()
    
    context = {'venue': venue, 'venue_owner': venue_owner, 'events':events}
    return render(request, 'events/show_venue.html', context)


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "John"
    name = request.user.username
    month = month.capitalize()

    # convert month name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)
    # create current year
    now = datetime.now()
    current_year = now.year

    # query event date

    event_list = Event.objects.filter(
        event_date__year=year, event_date__month=month_number)

    time = now.strftime('%I:%M:%S %p')

    context = {"name": name, "year": year, "month": month,
               "month_number": month_number, "cal": cal, "current_year": current_year, "time": time, 'event_list': event_list}
    return render(request, 'events/home.html', context)


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date', '-name', 'venue')
    context = {'event_list': event_list}
    return render(request, 'events/event_list.html', context)


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('?')
    venue_list = Venue.objects.all()

    # set pagination

    p = Paginator(venue_list, 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages

    context = {'venue_list': venue_list, 'venues': venues, 'nums': nums}
    return render(request, 'events/venue.html', context)


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id  # loggin user
            venue.save()
            # form.save()

            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:

            submitted = True

    return render(request, 'events/add_venue.html', {"form": form, 'submitted': submitted})


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()

                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
               # form.save()
                event = form.save(commit=False)
                event.manager = request.user  # loggin user
                event.save()

                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # just going to the page not submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm

        if 'submitted' in request.GET:

            submitted = True

    return render(request, 'events/add_event.html', {"form": form, 'submitted': submitted})
