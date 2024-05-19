from django.contrib import admin
from . import models
from django.contrib.auth.models import Group

# Register your models here.

#remove groups

#admin.site.unregister(Group)

#admin.site.register(models.Event)
admin.site.register(models.MyClubUser)
#admin.site.register(models.Venue)

@admin.register(models.Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display=('name','address','phone',)
    ordering=('name',)
    search_fields=('name','address',)
    

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    fields=(('name', 'venue'), 'event_date', 'description', 'manager','approved')
    list_display=('name','event_date','venue',)
    list_filter=('name','event_date','venue',)
    ordering=('-event_date',)
    search_fields=('name','event_date',)