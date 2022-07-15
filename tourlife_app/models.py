# from pyexpat import model
from time import time
from django.db import models
from django.contrib.auth.models import AbstractUser

# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class User(AbstractUser):
    
    username=models.CharField(max_length=20, null=True,blank=True,unique= True)
    first_name=models.CharField(max_length=20, null=True,blank=True)
    last_name=models.CharField(max_length=20, null=True,blank=True)
    email=models.EmailField(max_length=20,unique=True)
    password=models.CharField(max_length=200,null=True,blank=True)
    mobile_no=models.CharField(max_length=10,null=True,blank=True)
    profile_image=models.CharField(max_length=200,null=True,blank=True)
    is_manager=models.BooleanField(default=False)
    is_artist=models.BooleanField(default=False)
    
    def __str__ (self):
        return f"{self.first_name}"



class Usertoken(models.Model):
    user=models.ForeignKey(User,related_name='token',on_delete=models.CASCADE)
    token=models.CharField(max_length=500,null=True,blank=True)

class Person(models.Model):
    name=models.CharField(max_length=20)

class Gigs(models.Model):
    user=models.ForeignKey(User,related_name='gig_user',on_delete=models.CASCADE)
    title=models.CharField(max_length=20,null=True,blank=True)
    descriptions=models.CharField(max_length=100,null=True,blank=True)
    profile_pic=models.CharField(max_length=200,null=True,blank=True)
    cover_image=models.CharField(max_length=200,null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    show=models.CharField(max_length=200,null=True,blank=True)
    stage=models.CharField(max_length=200,null=True,blank=True)
    visa=models.CharField(max_length=200,null=True,blank=True)
    Equipment = models.BooleanField(default=False)
    date=models.DateTimeField(null=True,blank=True)
    sound_check_time = models.TimeField(null=True,blank=True)

    def __str__ (self):
        return f"{self.title}"

SEMESTER_CHOICES = (
    ("FLIGHT", "FLIGHT"),
    ("CAB", "CAB"),
    ("HOTEL", "HOTEL"),
    ("OTHER", "OTHER"),
)

class DaySchedule(models.Model):
    user=models.ForeignKey(User,related_name='schedule_user',on_delete=models.CASCADE)
    descriptions=models.CharField(max_length=100,null=True,blank=True)
    start_time=models.TimeField(null=True,blank=True)
    end_time=models.TimeField(null=True,blank=True)
    type = models.CharField(choices = SEMESTER_CHOICES,max_length = 20,default = 'OTHER')
    venue = models.CharField(max_length=100,null=True,blank=True)

    def __str__ (self):
        return f"{self.descriptions}"
    

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


