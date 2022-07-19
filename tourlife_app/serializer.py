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
    is_manager=serializers.CharField(required=False)
    is_artist=serializers.CharField(required=False)

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
    id=serializers.CharField(required=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    
    class Meta:
        model=User
        fields=["id","first_name","last_name"]

class DayScheduleSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=True)
    descriptions=serializers.CharField(required=True)
    start_time=serializers.CharField(required=True)
    end_time=serializers.CharField(required=True)
    type=serializers.CharField(required=True)
    venue=serializers.CharField(required=True)
    
    class Meta:
        model=DaySchedule
        fields=["user","descriptions","start_time","end_time","type","venue"]

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
    indoor=serializers.CharField(required=True)
    covered=serializers.CharField(required=True)
    capacity=serializers.CharField(required=True)
    wather=serializers.CharField(required=True)
    credential_collection=serializers.CharField(required=True)
    dressing_room=serializers.CharField(required=True)
    hospitality=serializers.CharField(required=True)
    hospitality_detail=serializers.CharField(required=True)
    catring=serializers.CharField(required=True)
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
    wifi_paid_for = serializers.CharField(required=True)
    room_buyout = serializers.CharField(required=True)
    class Meta:
        model=Hotel
        fields=["user","gig","hotel_name","address","direction","website","number","wifi_paid_for","room_buyout"]

class HotelListSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Hotel
        fields='__all__'

class ContactSerializer(serializers.ModelSerializer):
    gig=serializers.CharField(required=True)
    type=serializers.CharField(required=True)
    name=serializers.CharField(required=True)
    number=serializers.CharField(required=True)
    email=serializers.CharField(required=True)
    travelling_party=serializers.CharField(required=True)
    class Meta:
        model=Contacts
        fields=["gig","type","name","number","email","travelling_party"]

class DocumentSerializer(serializers.ModelSerializer):
    gig=serializers.CharField(required=True)

    boarding_passes = serializers.CharField(required=True)
    flight_confirmation_ticket = serializers.CharField(required=True)
    hotel_voucher = serializers.CharField(required=True)
    class Meta:
        model=Documents
        fields=["gig","boarding_passes","flight_confirmation_ticket","hotel_voucher"]

class GuestListSerializer(serializers.ModelSerializer):
    gig=serializers.CharField(required=True)

    guestlist_detail= serializers.CharField(required=True)
    guestlist=serializers.CharField(required=True)
    class Meta:
        model=GuestList
        fields=["gig","guestlist_detail","guestlist"]

class SetTimeSerialiazer(serializers.ModelSerializer):

    class Meta:
        model=SetTime
        fields= '__all__'