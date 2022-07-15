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
    # id=serializers.CharField(required=True)
    # first_name=serializers.CharField(required=True)
    # last_name=serializers.CharField(required=True)
    
    class Meta:
        model=DaySchedule
        fields='__all__'
