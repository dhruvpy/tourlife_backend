from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(User)
admin.site.register(Usertoken)
# admin.site.register(Gigs)
# admin.site.register(GigMaster)
# admin.site.register(FlightBook)
# admin.site.register(CabBook)
# admin.site.register(Venue)
# admin.site.register(Hotel)
# admin.site.register(Contacts)
# admin.site.register(GuestList)
# admin.site.register(SetTime)
# admin.site.register(Document)
admin.site.register(Emailotp)
admin.site.register(SetNewPassword)



class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','email','password','mobile_no','is_manager','is_artist','profile_image')
admin.site.register(User, UserAdmin)

class GigAdmin(admin.ModelAdmin):
    list_display = ('title','descriptions','location','start_date','end_date','sound_check_time')
admin.site.register(Gigs, GigAdmin)

class GigMsterAdmin(admin.ModelAdmin):
    list_display = ('user','gig')
admin.site.register(GigMaster, GigMsterAdmin)

class FlightBookAdmin(admin.ModelAdmin):
    list_display = ('user','gig','depart_location','depart_lat_long','depart_time','depart_terminal','depart_gate'
    ,'arrival_location','arrival_lat_long','arrival_time','arrival_terminal','arrival_gate')
admin.site.register(FlightBook, FlightBookAdmin)

class CabBookAdmin(admin.ModelAdmin):
    list_display = ('user','gig','depart_location','depart_lat_long','depart_time'
    ,'arrival_location','arrival_lat_long','arrival_time')
admin.site.register(CabBook, CabBookAdmin)

class VenueAdmin(admin.ModelAdmin):
    list_display = ('user','gig','venue_name','address','direction','website')
admin.site.register(Venue, VenueAdmin)

class HotelAdmin(admin.ModelAdmin):
    list_display = ('user','gig','hotel_name','address','direction','website')
admin.site.register(Hotel, HotelAdmin)

class ContactsAdmin(admin.ModelAdmin):
    list_display = ('user','gig','type','name','number')
admin.site.register(Contacts, ContactsAdmin)

class GuestListAdmin(admin.ModelAdmin):
    list_display = ('user','gig')
admin.site.register(GuestList, GuestListAdmin)

class SetTimeAdmin(admin.ModelAdmin):
    list_display = ('user','gig','venue','depart_time','arrival_time')
admin.site.register(SetTime, SetTimeAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user','gig','flight','type','document')
admin.site.register(Document, DocumentAdmin)