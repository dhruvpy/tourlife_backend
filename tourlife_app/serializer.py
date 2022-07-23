from lib2to3.pgen2 import token
from pyexpat import model
from rest_framework import serializers
from .models import *
# from django.contrib.auth.models import User

class CreateUserSerializers(serializers.ModelSerializer):
    username=serializers.CharField(required=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    email=serializers.EmailField(required=True)
    mobile_no=serializers.IntegerField(required=False)
    profile_image=serializers.CharField(required=False)
    is_manager=serializers.BooleanField(required=False)
    is_artist=serializers.BooleanField(required=False)

    class Meta:
        model= User
        fields= ["username","first_name","last_name","password","email","mobile_no","profile_image","is_manager","is_artist"]


class LoginUserSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(required=True)

    class Meta:
        model=User
        fields=["email","password"]

class GigsSerializer(serializers.ModelSerializer):
    # user=serializers.CharField(required=True)
    # title=serializers.CharField(required=True)
    # descriptions=serializers.CharField(required=True)
    # profile_pic=serializers.CharField(required=True)
    # cover_image=serializers.CharField(required=True)
    # date=serializers.DateField(required=True)
    class Meta:
        model=Gigs
        # fields=["user","title","descriptions","profile_pic","cover_image","date"]
        fields="__all__"


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model=FlightBook
        # fields=["user","title","descriptions","profile_pic","cover_image","date"]
        fields="__all__"

class CabBookSerializer(serializers.ModelSerializer):

    class Meta:
        model=CabBook
        # fields=["user","title","descriptions","profile_pic","cover_image","date"]
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(required=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    
    class Meta:
        model=User
        fields=["id","first_name","last_name"]


class UserListSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    
    class Meta:
        model=User
        fields=["id","first_name","last_name","is_manager"]                                                                 

class FlightBookSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    gig = serializers.CharField(required=True)
    depart_location = serializers.CharField(required=True)
    depart_lat_long = serializers.CharField(required=True)
    depart_time = serializers.CharField(required=True)
    depart_terminal = serializers.CharField(required=True)
    depart_gate = serializers.CharField(required=True)
    arrival_location = serializers.CharField(required=True)
    arrival_lat_long = serializers.CharField(required=True)
    arrival_time = serializers.CharField(required=True)
    arrival_terminal = serializers.CharField(required=True)
    arrival_gate = serializers.CharField(required=True)
    airlines = serializers.CharField(required=True)
    flight_number = serializers.CharField(required=True)
    flight_class = serializers.CharField(required=True)
    wather = serializers.CharField(required=True)

    class Meta:
        model=FlightBook
        fields=["user","gig","depart_location","depart_lat_long","depart_time","depart_terminal","depart_gate","arrival_location",
        "arrival_lat_long","arrival_time","arrival_terminal","arrival_gate","airlines","flight_number","flight_class","wather"]

class CabBookSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    gig = serializers.CharField(required=True)
    depart_location = serializers.CharField(required=True)
    depart_lat_long = serializers.CharField(required=True)
    depart_time = serializers.CharField(required=True)
    arrival_location = serializers.CharField(required=True)
    arrival_lat_long = serializers.CharField(required=True)
    arrival_time = serializers.CharField(required=True)
    driver_name = serializers.CharField(required=True)
    driver_number = serializers.CharField(required=True)
    wather = serializers.CharField(required=True)
    class Meta:
        model=CabBook
        fields=["user","gig","depart_location","depart_lat_long","depart_time","arrival_location","arrival_lat_long","arrival_time"
        ,"driver_name","driver_number","wather"]

class VenueSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=True)
    gig=serializers.CharField(required=True)

    address=serializers.CharField(required=True)
    direction=serializers.CharField(required=True)
    website=serializers.CharField(required=True)
    number=serializers.CharField(required=True)
    indoor=serializers.BooleanField(required=True)
    covered=serializers.BooleanField(required=True)
    capacity=serializers.CharField(required=True)
    wather=serializers.CharField(required=True)
    credential_collection=serializers.CharField(required=True)
    dressing_room=serializers.CharField(required=True)
    hospitality=serializers.BooleanField(required=True)
    hospitality_detail=serializers.CharField(required=True)
    catring=serializers.BooleanField(required=True)
    catring_detail=serializers.CharField(required=True)
    class Meta:
        model=Venue
        fields=["user","gig","address","direction","website","number","indoor","covered","capacity","wather","credential_collection",
        "dressing_room","hospitality","hospitality_detail","catring","catring_detail"]

class VenueListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Venue
        fields='__all__'

class HotelSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=True)
    gig=serializers.CharField(required=True)
    hotel_name=serializers.CharField(required=True)
    address=serializers.CharField(required=True)
    direction = serializers.CharField(required=True)
    website = serializers.CharField(required=True)
    number = serializers.CharField(required=True)
    wifi_paid_for = serializers.BooleanField(required=True)
    room_buyout = serializers.CharField(required=True)
    class Meta:
        model=Hotel
        fields=["user","gig","hotel_name","address","direction","website","number","wifi_paid_for","room_buyout"]

class HotelListSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Hotel
        fields='__all__'

class ContactSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=True)
    gig=serializers.CharField(required=True)
    type=serializers.CharField(required=True)
    name=serializers.CharField(required=True)
    number=serializers.CharField(required=True)
    email=serializers.CharField(required=True)
    travelling_party=serializers.BooleanField(required=True)
    class Meta:
        model=Contacts
        fields=["user","gig","type","name","number","email","travelling_party"]

class GuestListSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=True)
    gig=serializers.CharField(required=True)
    guestlist_detail= serializers.CharField(required=True)
    guestlist=serializers.BooleanField(required=True)
    class Meta:
        model=GuestList
        fields=["user","gig","guestlist_detail","guestlist"]

class SetTimeSerialiazer(serializers.ModelSerializer):
    user=serializers.CharField(required=True)
    gig=serializers.CharField(required=True)
    venue=serializers.CharField(required=True)
    depart_time=serializers.CharField(required=True)
    arrival_time=serializers.CharField(required=True)
    class Meta:
        model=SetTime
        fields= ["user","gig","venue","depart_time","arrival_time"]

class PassesSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=True)
    gig=serializers.CharField(required=True)
    flight=serializers.CharField(required=True)
    passes=serializers.CharField(required=False)
    class Meta:
        model=Passes
        fields=["user","gig","flight","passes"]

class LogoutSerializer(serializers.ModelSerializer):
    token=serializers.CharField(required=True)

    class Meta:
        model=Usertoken
        fields=["token"]