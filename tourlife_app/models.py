from time import time
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username=models.CharField(max_length=20, null=True,blank=True,unique= True)
    first_name=models.CharField(max_length=20, null=True,blank=True)
    last_name=models.CharField(max_length=20, null=True,blank=True)
    email=models.EmailField(max_length=100,unique=True)
    password=models.CharField(max_length=200,null=True,blank=True)
    mobile_no=models.CharField(max_length=10,null=True,blank=True)
    profile_image=models.CharField(max_length=200,null=True,blank=True)
    is_manager=models.BooleanField(default=False)
    is_artist=models.BooleanField(default=False)

    def __str__ (self):
        return f"{self.id}"
class Usertoken(models.Model):
    user=models.ForeignKey(User,related_name='token',on_delete=models.CASCADE)
    token=models.CharField(max_length=500,null=True,blank=True)

class Gigs(models.Model):
    user=models.ManyToManyField(User)
    title=models.CharField(max_length=20,null=True,blank=True)
    descriptions=models.CharField(max_length=100,null=True,blank=True)
    profile_pic=models.CharField(max_length=200,null=True,blank=True)
    cover_image=models.CharField(max_length=200,null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    show=models.CharField(max_length=200,null=True,blank=True)
    stage=models.CharField(max_length=200,null=True,blank=True)
    visa=models.CharField(max_length=200,null=True,blank=True)
    Equipment = models.BooleanField(default=False)
    start_date=models.DateTimeField(null=True,blank=True)
    end_date=models.DateTimeField(null=True,blank=True)
    sound_check_time = models.TimeField(null=True,blank=True)

    # def save(self, *args, **kwargs):
    #     print(self,'--------------')

    def __str__ (self):
        return f"{self.title}"

class GigMaster(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    gig = models.ForeignKey(Gigs,on_delete=models.CASCADE)

    def __str__ (self):
        return f"{self.gig.title}"

class FlightBook(models.Model):
    user = models.ForeignKey(User,related_name='flight_user',on_delete=models.CASCADE)
    gig = models.ForeignKey(Gigs,related_name='flight_gig',on_delete=models.CASCADE)
    depart_location = models.CharField(max_length=100,null=True,blank=True)
    depart_lat_long = models.CharField(max_length=100,null=True,blank=True)
    depart_time = models.DateTimeField(null=True,blank=True)
    depart_terminal = models.CharField(max_length=100,null=True,blank=True)
    depart_gate = models.CharField(max_length=100,null=True,blank=True)
    arrival_location = models.CharField(max_length=100,null=True,blank=True)
    arrival_lat_long = models.CharField(max_length=100,null=True,blank=True)
    arrival_time = models.DateTimeField(null=True,blank=True)
    arrival_terminal = models.CharField(max_length=100,null=True,blank=True)
    arrival_gate = models.CharField(max_length=100,null=True,blank=True)
    airlines = models.CharField(max_length=100,null=True,blank=True)
    flight_number = models.CharField(max_length=100,null=True,blank=True)
    flight_class = models.CharField(max_length=100,null=True,blank=True)
    wather = models.CharField(max_length=100,null=True,blank=True)

    def __str__ (self):
        return f"{self.flight_number}"

class CabBook(models.Model):
    user = models.ForeignKey(User,related_name='cab_user',on_delete=models.CASCADE)
    gig = models.ForeignKey(Gigs,related_name='cab_gig',on_delete=models.CASCADE)
    depart_location = models.CharField(max_length=100,null=True,blank=True)
    depart_lat_long = models.CharField(max_length=100,null=True,blank=True)
    depart_time = models.DateTimeField(null=True,blank=True)
    arrival_location = models.CharField(max_length=100,null=True,blank=True)
    arrival_lat_long = models.CharField(max_length=100,null=True,blank=True)
    arrival_time = models.DateTimeField(null=True,blank=True)
    driver_name = models.CharField(max_length=100,null=True,blank=True)
    driver_number = models.CharField(max_length=100,null=True,blank=True)
    wather = models.CharField(max_length=100,null=True,blank=True)

    def __str__ (self):
        return f"{self.arrival_location}"

    # 1d416dd6f1f006195c0aa4bd9685b88d
class Venue(models.Model):
    user = models.ForeignKey(User,related_name='venue_user',on_delete=models.CASCADE)
    gig = models.ForeignKey(Gigs,related_name='venue_gig',on_delete=models.CASCADE)
    venue_name=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    direction=models.CharField(max_length=50,null=True,blank=True)
    website=models.CharField(max_length=100,null=True,blank=True)
    number=models.CharField(max_length=100,null=True,blank=True)
    indoor=models.BooleanField(null=True,blank=True)
    covered=models.BooleanField(null=True,blank=True)
    capacity=models.IntegerField(null=True,blank=True)
    wather=models.CharField(max_length=100,null=True,blank=True)
    credential_collection=models.CharField(max_length=100,null=True,blank=True)
    dressing_room=models.CharField(max_length=100,null=True,blank=True)
    hospitality=models.BooleanField(default=False)
    hospitality_detail=models.CharField(max_length=100,null=True,blank=True)
    hospitality_email=models.CharField(max_length=100,null=True,blank=True)
    catring=models.BooleanField(default=False)
    catring_detail=models.CharField(max_length=100,null=True,blank=True)

    def __str__ (self):
        return f"{self.venue_name}"
class Hotel(models.Model):
    user = models.ForeignKey(User,related_name='h_user',on_delete=models.CASCADE)
    gig = models.ForeignKey(Gigs,related_name='h_gig',on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    direction = models.CharField(max_length=100,null=True,blank=True)
    website =models.CharField(max_length=100,null=True,blank=True)
    number =models.CharField(max_length=100,null=True,blank=True)
    wifi_paid_for = models.BooleanField(null=True,blank=True)
    room_buyout = models.CharField(max_length=100,null=True,blank=True)

CONTACT_CHOICES=(
    ("EMERGANCY","EMERGANCY"),
    ("TRANSPORT_CORDINATOR","TRANSPORT_CORDINATOR"),
    ("ARTIST_LIAISON","ARTIST_LIAISON"),
    ("MANAGER","MANAGER"),
    ("TM","TM")
)
class Contacts(models.Model):
    user = models.ForeignKey(User,related_name='contact_user',on_delete=models.CASCADE)
    gig = models.ForeignKey(Gigs,related_name='contact_gig',on_delete=models.CASCADE)
    type= models.CharField(max_length=100,choices=CONTACT_CHOICES,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    number = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    travelling_party=models.BooleanField(null=True,blank=True)
class GuestList(models.Model):
    user = models.ForeignKey(User,related_name='guest_user',on_delete=models.CASCADE)
    gig = models.ForeignKey(Gigs,related_name='guest_gig',on_delete=models.CASCADE)
    guestlist_detail=models.TextField(null=True,blank=True)
    guestlist= models.BooleanField(null=True,blank=True)

class SetTime(models.Model):
    user = models.ForeignKey(User,related_name='settime_user',on_delete=models.CASCADE)
    gig = models.ForeignKey(Gigs,related_name='settime_gig',on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue,related_name='settime_venue',on_delete=models.CASCADE)
    depart_time=models.DateTimeField(null=True,blank=True)
    arrival_time=models.DateTimeField(null=True,blank=True)

DOCUMENT_CHOICES=(
    ('BOARDING_PASSES','BOARDING_PASSES'),
    ('FLIGHT_CONFIRMATIONS','FLIGHT_CONFIRMATIONS'),
    ('HOTEL_VOUCHER','HOTEL_VOUCHER')
)
class Document(models.Model):
    user = models.ForeignKey(User,related_name='passes_user',on_delete=models.CASCADE)
    gig = models.ForeignKey(Gigs,related_name='passes_gig',on_delete=models.CASCADE)
    flight= models.ForeignKey(FlightBook,related_name='flight_passes',on_delete=models.CASCADE)
    type= models.CharField(max_length=100,choices=DOCUMENT_CHOICES,null=True,blank=True)
    document = models.CharField(max_length=1000,null=True,blank=True)

class Emailotp(models.Model):
    email=models.EmailField(max_length=100)
    otp=models.CharField(max_length=4,null=True,blank=True)

class SetNewPassword(models.Model):
    email=models.EmailField(max_length=100)
    new_password= models.CharField(max_length=10)
