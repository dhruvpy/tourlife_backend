from rest_framework import serializers
from .models import *
class CreateUserSerializers(serializers.ModelSerializer):
    username=serializers.CharField(required=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    email=serializers.EmailField(required=True)
    mobile_no=serializers.IntegerField(required=True)
    profile_image=serializers.CharField(required=True)
    is_manager=serializers.BooleanField(required=True)
    is_artist=serializers.BooleanField(required=True)
    class Meta:
        model= User
        fields= ["username","first_name","last_name","password","email","mobile_no","profile_image","is_manager","is_artist"]

class ListUserSerializers(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= "__all__"
class LoginUserSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(required=True)
    class Meta:
        model=User
        fields=["email","password"]

class CreateGigsSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=True)
    title=serializers.CharField(required=True)
    descriptions=serializers.CharField(required=True)
    profile_pic=serializers.CharField(required=True)
    cover_image=serializers.CharField(required=True)
    start_date=serializers.DateTimeField(required=True)
    end_date=serializers.DateTimeField(required=True)
    location = serializers.CharField(required=True)
    show = serializers.CharField(required=True)
    stage = serializers.CharField(required=True)
    visa=serializers.CharField(required=True)
    Equipment =serializers.BooleanField(required=True)
    sound_check_time = serializers.TimeField(required=True)
    class Meta:
        model=Gigs
        fields=["user","title","descriptions","profile_pic","cover_image","start_date","end_date","location","show","stage","visa","Equipment","sound_check_time"]
        # fields="__all__"

class ListGigSerializer(serializers.ModelSerializer):

    # user_id= serializers.ReadOnlyField(source='user.id')
    # user_name= serializers.ReadOnlyField(source='user.username')
    class Meta:
        model= Gigs
        fields=["id","user","title","descriptions","profile_pic","cover_image","start_date","end_date","location","show","stage","visa","Equipment","sound_check_time"]

class FlightSerializer(serializers.ModelSerializer):
    user_id= serializers.ReadOnlyField(source='user.id')
    user_name= serializers.ReadOnlyField(source='user.username')
    gig_id= serializers.ReadOnlyField(source='gig.id')
    gig_title= serializers.ReadOnlyField(source='gig.title')

    class Meta:
        model=FlightBook
        fields=["id","user_id","user_name","gig_id","gig_title","depart_location","depart_lat_long","depart_time","depart_terminal","depart_gate","arrival_location",
        "arrival_lat_long","arrival_time","arrival_terminal","arrival_gate","airlines","flight_number","flight_class","wather"]

class CabSerializer(serializers.ModelSerializer):
    user_id= serializers.ReadOnlyField(source='user.id')
    user_name= serializers.ReadOnlyField(source='user.username')
    gig_id= serializers.ReadOnlyField(source='gig.id')
    gig_title= serializers.ReadOnlyField(source='gig.title')
    class Meta:
        model=CabBook
        fields=["id","user_id","user_name","gig_id","gig_title","depart_location","depart_lat_long","depart_time","arrival_location","arrival_lat_long","arrival_time"
        ,"driver_name","driver_number","wather"]
        

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
    user = serializers.IntegerField(required=True)
    gig = serializers.IntegerField(required=True)
    depart_location = serializers.CharField(required=True)
    depart_lat_long = serializers.CharField(required=True)
    depart_time = serializers.DateTimeField(required=True)
    depart_terminal = serializers.CharField(required=True)
    depart_gate = serializers.CharField(required=True)
    arrival_location = serializers.CharField(required=True)
    arrival_lat_long = serializers.CharField(required=True)
    arrival_time = serializers.DateTimeField(required=True)
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
    user = serializers.IntegerField(required=True)
    gig = serializers.IntegerField(required=True)
    depart_location = serializers.CharField(required=True)
    depart_lat_long = serializers.CharField(required=True)
    depart_time = serializers.DateTimeField(required=True)
    arrival_location = serializers.CharField(required=True)
    arrival_lat_long = serializers.CharField(required=True)
    arrival_time = serializers.DateTimeField(required=True)
    driver_name = serializers.CharField(required=True)
    driver_number = serializers.CharField(required=True)
    wather = serializers.CharField(required=True)
    class Meta:
        model=CabBook
        fields=["user","gig","depart_location","depart_lat_long","depart_time","arrival_location","arrival_lat_long","arrival_time"
        ,"driver_name","driver_number","wather"]

class VenueSerializer(serializers.ModelSerializer):
    user=serializers.IntegerField(required=True)
    gig=serializers.IntegerField(required=True)
    venue_name=serializers.CharField(required=True)
    address=serializers.CharField(required=True)
    direction=serializers.CharField(required=True)
    website=serializers.CharField(required=True)
    number=serializers.CharField(required=True)
    indoor=serializers.BooleanField(required=True)
    covered=serializers.BooleanField(required=True)
    capacity=serializers.IntegerField(required=True)
    wather=serializers.CharField(required=True)
    credential_collection=serializers.CharField(required=True)
    dressing_room=serializers.CharField(required=True)
    hospitality=serializers.BooleanField(required=True)
    hospitality_detail=serializers.CharField(required=True)
    hospitality_email=serializers.CharField(required=True)
    catring=serializers.BooleanField(required=True)
    catring_detail=serializers.CharField(required=True)
    
    class Meta:
        model=Venue
        fields=["user","gig","venue_name","address","direction","website","number","indoor","covered","capacity","wather","credential_collection",
        "dressing_room","hospitality","hospitality_detail","hospitality_email","catring","catring_detail"]

class VenueListSerializer(serializers.ModelSerializer):
    
    user_id= serializers.ReadOnlyField(source='user.id')
    user_name= serializers.ReadOnlyField(source='user.username')
    gig_id= serializers.ReadOnlyField(source='gig.id')
    gig_title= serializers.ReadOnlyField(source='gig.title')
    class Meta:
        model=Venue
        fields=["id","user_id","user_name","gig_id","gig_title","venue_name","address","direction","website","number","indoor","covered","capacity","wather","credential_collection",
        "dressing_room","hospitality","hospitality_detail",'hospitality_email',"catring","catring_detail"]

class HotelSerializer(serializers.ModelSerializer):
    user=serializers.IntegerField(required=True)
    gig=serializers.IntegerField(required=True)
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
    user_id= serializers.ReadOnlyField(source='user.id')
    user_name= serializers.ReadOnlyField(source='user.username')
    gig_id= serializers.ReadOnlyField(source='gig.id')
    gig_title= serializers.ReadOnlyField(source='gig.title')
    class Meta:
        model=Hotel
        fields=["id","user_id","user_name","gig_id","gig_title","hotel_name","address","direction","website","number","wifi_paid_for","room_buyout"]


class ContactSerializer(serializers.ModelSerializer):
    user=serializers.IntegerField(required=True)
    gig=serializers.IntegerField(required=True)
    type=serializers.CharField(required=True)
    name=serializers.CharField(required=True)
    number=serializers.CharField(required=True)
    email=serializers.CharField(required=True)
    travelling_party=serializers.BooleanField(required=True)
    class Meta:
        model=Contacts
        fields=["user","gig","type","name","number","email","travelling_party"]

class ContactListSerializer(serializers.ModelSerializer):
    user_id= serializers.ReadOnlyField(source='user.id')
    user_name= serializers.ReadOnlyField(source='user.username')
    gig_id= serializers.ReadOnlyField(source='gig.id')
    gig_title= serializers.ReadOnlyField(source='gig.title')
    class Meta:
        model=Contacts
        fields=["id","user_id","user_name","gig_id","gig_title","type","name","number","email","travelling_party"]

class GuestListSerializer(serializers.ModelSerializer):
    user=serializers.IntegerField(required=True)
    gig=serializers.IntegerField(required=True)
    guestlist_detail= serializers.CharField(required=True)
    guestlist=serializers.BooleanField(required=True)
    class Meta:
        model=GuestList
        fields=["user","gig","guestlist_detail","guestlist"]

class GuestSerializer(serializers.ModelSerializer):
    user_id= serializers.ReadOnlyField(source='user.id')
    user_name= serializers.ReadOnlyField(source='user.username')
    gig_id= serializers.ReadOnlyField(source='gig.id')
    gig_title= serializers.ReadOnlyField(source='gig.title')
    class Meta:
        model=GuestList
        fields=["id","user_id","user_name","gig_id","gig_title","guestlist_detail","guestlist"]

class SetTimeSerialiazer(serializers.ModelSerializer):
    user=serializers.IntegerField(required=True)
    gig=serializers.IntegerField(required=True)
    venue=serializers.IntegerField(required=True)
    depart_time=serializers.DateTimeField(required=True)
    arrival_time=serializers.DateTimeField(required=True)
    class Meta:
        model=SetTime
        fields= ["user","gig","venue","depart_time","arrival_time"]

class SetTimeListSerializer(serializers.ModelSerializer):
    user_id= serializers.ReadOnlyField(source='user.id')
    user_name= serializers.ReadOnlyField(source='user.username')
    gig_id= serializers.ReadOnlyField(source='gig.id')
    gig_title= serializers.ReadOnlyField(source='gig.title')
    venue_id= serializers.ReadOnlyField(source='venue.id')
    venue_name= serializers.ReadOnlyField(source='venue.venue_name')
    class Meta:
        model=SetTime
        fields= ["id","user_id","user_name","gig_id","gig_title","venue_id","venue_name","depart_time","arrival_time"]


class DocumentSerializer(serializers.ModelSerializer):
    user=serializers.IntegerField(required=True)
    gig=serializers.IntegerField(required=True)
    flight=serializers.IntegerField(required=True)
    type=serializers.CharField(required=True)
    document=serializers.CharField(required=True)
    class Meta:
        model=Document
        fields=["user","gig","flight","type","document"]

class DocumentsListSerializer(serializers.ModelSerializer):
    user_id= serializers.ReadOnlyField(source='user.id')
    user_name= serializers.ReadOnlyField(source='user.username')
    gig_id= serializers.ReadOnlyField(source='gig.id')
    gig_title= serializers.ReadOnlyField(source='gig.title')
    flight_id= serializers.ReadOnlyField(source='flight.id')
    flight_name= serializers.ReadOnlyField(source='flight.airlines')
    class Meta:
        model=Document
        fields=["id","user_id","user_name","gig_id","gig_title","flight_id","flight_name","type","document"]

class ForgotpasswordSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    class Meta:
        model=Emailotp
        fields=["email"]

class SetNewPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model= SetNewPassword
        fields="__all__"