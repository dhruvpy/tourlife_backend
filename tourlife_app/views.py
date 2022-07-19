from dis import show_code
from genericpath import exists
from resource import struct_rusage
from urllib import request
from xml.dom.minidom import Document
from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import boto3
import jwt
from django.conf import settings
# from jwt import PyJWT
# from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth import authenticate


class UserCreateAPIView(GenericAPIView):
    # permission_classes = [AllowAny]
    serializer_class = CreateUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        if not request.user.is_superuser:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        username = request.data["username"]
        last_name = request.data["last_name"]
        email = request.data["email"]
        password = request.data["password"]
        mobile_no = request.data["mobile_no"]
        profile_image=request.data["profile_image"]

        user = User.objects.create(username=username, last_name=last_name, password=password, email=email, mobile_no=mobile_no,
                                profile_image=profile_image)
        response_data = {
            "id": user.id,
            "username": user.username,
            "last_name": user.last_name,
            "password": user.password,
            "email": user.email,
            "mobile_no": str(user.mobile_no),
            "profile_image": str(user.profile_image),
        }
        return Response(data={"status": status.HTTP_200_OK,
                            "message": 'add new user',
                            "result": {'data': response_data}},
                        status=status.HTTP_200_OK)

class UserUpdateAPIView(CreateAPIView):
    serializer_class=CreateUserSerializers
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        username=request.data["username"]
        first_name=request.data["first_name"]
        last_name=request.data["last_name"]
        password=request.data["password"]
        email=request.data["email"]
        mobile_no=request.data["mobile_no"]
        profile_image=request.data["profile_image"]

        id=self.kwargs["pk"]

        if not User.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user {} is not exists".format(id)},
                            status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.get(id=id)
        user.username=username
        user.first_name=first_name
        user.last_name=last_name
        user.password=password
        user.email=email
        user.mobile_no= mobile_no
        user.profile_image=profile_image
        user.save()

        response_data = {
            "id": user.id,
            "username":user.username,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "password":user.password,
            "email":user.email,
            "mobile_no":user.mobile_no,
            "profile_image":str(user.profile_image)
        }
        return Response(data={"status": status.HTTP_200_OK,
                            "message": "user updated",
                            "results": {'data': response_data}},
                        status=status.HTTP_200_OK)

class UserListAPIView(ListAPIView):
    serializer_class=CreateUserSerializers
    queryset=User.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Users list",
                                 "result": serializer.data},
                                status=status.HTTP_200_OK)

class UserDeleteAPIView(DestroyAPIView):
    serializer_class = CreateUserSerializers

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        if User.objects.filter(id=id).exists():
            user = User.objects.get(id=id)
            user.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializers
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error':True, 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.get(email=email,password=password)

        if user is not None:
            if not user.password == password:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid username or password"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid username or password"},status=status.HTTP_400_BAD_REQUEST)

        if user:
            payload={"email":user.email,"password":user.password}

            print(payload)
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "User Login Successfully.",
                                 "result": {'id': user.id,
                                            'first_name':user.first_name, 
                                            'last_name':user.last_name, 
                                            'token': jwt_token,
                                            'is_manager': user.is_superuser}},
                                status=status.HTTP_200_OK)

class AdminLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error':True, 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
    
        user = User.objects.get(email=email)

        if not user.is_manager==True:
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error':True, 
            'message':"is_manage is not allow"}, status=status.HTTP_400_BAD_REQUEST)

        if user is not None:
            if not user.password == password:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid username or password"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid username or password"},status=status.HTTP_400_BAD_REQUEST)

        if user:
            payload={"email":user.email,"password":user.password}

            print(payload)
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Admin User Login Successfully.",
                                "result": {'id': user.id,
                                            'first_name':user.first_name, 
                                            'last_name':user.last_name, 
                                            'token': jwt_token,
                                            'is_manager': user.is_superuser}},
                                status=status.HTTP_200_OK)
    
class GigsCreateAPIView(CreateAPIView):
    serializer_class = GigsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user= User.objects.get(id=request.data["user"])
        title = request.data["title"]
        descriptions = request.data["descriptions"]
        profile_pic = request.data["profile_pic"]
        cover_image=request.data["cover_image"]
        location=request.data["location"]
        show=request.data["show"]
        stage =request.data["stage"]
        visa =request.data["visa"]
        Equipment=request.data["Equipment"]
        date=request.data["date"]
        sound_check_time=request.data["sound_check_time"]

        gigs=Gigs.objects.create(user=user,title=title,descriptions=descriptions,
        profile_pic=profile_pic,cover_image=cover_image,location=location,show=show,stage=stage,visa=visa,Equipment=Equipment
        ,sound_check_time=sound_check_time,date=date)

        response_data = {
            "id":gigs.id,
            "user":  str(gigs.user),
            "title": gigs.title,
            "descriptions": gigs.descriptions,
            "profile_pic": str(gigs.profile_pic),
            "cover_image":str(gigs.cover_image),
            "location":gigs.location,
            "show":gigs.show,
            "stage":gigs.stage,
            "visa":gigs.visa,
            "Equipment":gigs.Equipment,
            "date":str(gigs.date),
            "sound_check_time":gigs.sound_check_time        
            }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "gigs created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)

class GigsUpdateAPIView(CreateAPIView):
    serializer_class=GigsSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user=User.objects.get(id=request.data["user"])
        title=request.data["title"]
        descriptions=request.data["descriptions"]
        profile_pic=request.data["profile_pic"]
        cover_image=request.data["cover_image"]
        location=request.data["location"]
        show=request.data["show"]
        stage =request.data["stage"]
        visa =request.data["visa"]
        Equipment=request.data["Equipment"]
        date=request.data["date"]
        sound_check_time=request.data["sound_check_time"]

        id=self.kwargs["pk"]
        if not Gigs.objects.filter(id=id).exists():
        # if not User.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gigs {} is not exists".format(id)},
                            status=status.HTTP_400_BAD_REQUEST)
        gigs=Gigs.objects.get(id=id)
        gigs.user=user
        gigs.title=title
        gigs.descriptions=descriptions
        gigs.profile_pic=profile_pic
        gigs.cover_image=cover_image
        gigs.location=location
        gigs.show=show
        gigs.stage=stage
        gigs.visa=visa
        gigs.Equipment=Equipment
        gigs.date= date
        gigs.sound_check_time=sound_check_time
        gigs.save()

        response_data = {
            "id": gigs.id,
            "user":str(gigs.user),
            "title":gigs.title,
            "descriptions":gigs.descriptions,
            "profile_pic":str(gigs.profile_pic),
            "cover_image":str(gigs.cover_image),
            "location":gigs.location,
            "show":gigs.show,
            "stage":gigs.stage,
            "visa":gigs.visa,
            "Equipment":gigs.Equipment,
            "date":gigs.date,
            "sound_check_time":gigs.sound_check_time
        }
        return Response(data={"status": status.HTTP_200_OK,
                            "message": "gigs updated",
                            "results": {'data': response_data}},
                        status=status.HTTP_200_OK)
class GigsListAPIView(ListAPIView):
    serializer_class =GigsSerializer
    queryset=Gigs.objects.all()
    
    def get(self, request, *args, **kwargs):
        # print(request.user,"------------------")
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Gigs list",
                                 "result": serializer.data},
                                status=status.HTTP_200_OK)

class GigsDeleteAPIView(DestroyAPIView):
    serializer_class = GigsSerializer

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        if Gigs.objects.filter(id=id).exists():
            gigs = Gigs.objects.get(id=id)
            gigs.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)
                                
class ScheduleCreateAPIView(CreateAPIView):
    serializer_class = DayScheduleSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user= User.objects.get(id=request.data["user"])
        descriptions = request.data["descriptions"]
        start_time = request.data["start_time"]
        end_time=request.data["end_time"]
        type=request.data["type"]
        venue=request.data["venue"]

        schedule=DaySchedule.objects.create(user=user,descriptions=descriptions,
        start_time=start_time,end_time=end_time,type=type,venue=venue)

        response_data = {
            "id":schedule.id,
            "user":  str(schedule.user),
            "descriptions": schedule.descriptions,
            "start_time":schedule.start_time,
            "end_time":schedule.end_time,
            "type":schedule.type,
            "venue":schedule.venue,
                   
            }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "Schedule created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)

class ScheduleUpdateAPIView(CreateAPIView):
    serializer_class=DayScheduleSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user=User.objects.get(id=request.data["user"])
        descriptions=request.data["descriptions"]
        start_time=request.data["start_time"]
        end_time=request.data["end_time"]
        type=request.data["type"]
        venue=request.data["venue"]
        
        id=self.kwargs["pk"]

        if not DaySchedule.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Schedule is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        schedule=DaySchedule.objects.get(id=id)
        schedule.user=user
        schedule.descriptions=descriptions
        schedule.start_time=start_time
        schedule.end_time=end_time
        schedule.type=type
        schedule.venue=venue
        schedule.save()

        response_data = {
            "id": schedule.id,
            "user":str(schedule.user),
            "descriptions":schedule.descriptions,
            "start_time":schedule.start_time,
            "end_time":schedule.end_time,
            "type":schedule.type,
            "venue":schedule.venue,
        }
        return Response(data={"status": status.HTTP_200_OK,
                            "message": "Schedule Updated",
                            "results": {'data': response_data}},
                        status=status.HTTP_200_OK)
    
class ScheduleListAPIView(ListAPIView):
    serializer_class =DayScheduleSerializer
    queryset=DaySchedule.objects.all()
    
    def get(self, request, *args, **kwargs):
        # print(request.user,"------------------")
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Schedule list",
                                 "result": serializer.data},
                                status=status.HTTP_200_OK)

class ScheduleDeleteAPIView(DestroyAPIView):
    serializer_class = DayScheduleSerializer

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        if DaySchedule.objects.filter(id=id).exists():
            schedule = DaySchedule.objects.get(id=id)
            schedule.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

class FlightBookCreateAPIView(CreateAPIView):
    serializer_class = FlightBookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user= User.objects.get(id=request.data["user"])
        gig= Gigs.objects.get(id=request.data["gig"])
        depart_location = request.data["depart_location"]
        depart_lat_long = request.data["depart_lat_long"]
        depart_time = request.data["depart_time"]
        depart_terminal=request.data["depart_terminal"]
        depart_gate=request.data["depart_gate"]
        arrival_location=request.data["arrival_location"]
        arrival_lat_long =request.data["arrival_lat_long"]
        arrival_time =request.data["arrival_time"]
        arrival_terminal=request.data["arrival_terminal"]
        arrival_gate=request.data["arrival_gate"]
        airlines=request.data["airlines"]
        flight_number=request.data["flight_number"]
        flight_class=request.data["flight_class"]
        wather=request.data["wather"]

        flightbook=FlightBook.objects.create(user=user,gig=gig,depart_location=depart_location,depart_lat_long=depart_lat_long,
        depart_time=depart_time,depart_terminal=depart_terminal,depart_gate=depart_gate,arrival_location=arrival_location,
        arrival_lat_long=arrival_lat_long,arrival_time=arrival_time,arrival_terminal=arrival_terminal,
        airlines=airlines,arrival_gate=arrival_gate,flight_number=flight_number,flight_class=flight_class,wather=wather)

        response_data = {
            "id":flightbook.id,
            "user":  str(flightbook.user),
            "gig":str(flightbook.gig),
            "depart_location": flightbook.depart_location,
            "depart_lat_long": flightbook.depart_lat_long,
            "depart_time": flightbook.depart_time,
            "depart_terminal":flightbook.depart_terminal,
            "depart_gate":flightbook.depart_gate,
            "arrival_location":flightbook.arrival_location,
            "arrival_lat_long":flightbook.arrival_lat_long,
            "arrival_time":flightbook.arrival_time,
            "arrival_terminal":flightbook.arrival_terminal,
            "arrival_gate":flightbook.arrival_gate,
            "airlines":flightbook.airlines  ,
            "flight_number":flightbook.flight_number,
            "flight_class":flightbook.flight_class,
            "wather":flightbook.wather,
            }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "flightbook created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)

class FlightBookUpdateAPIView(CreateAPIView):
    serializer_class=FlightBookSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user= User.objects.get(id=request.data["user"])
        gig= Gigs.objects.get(id=request.data["gig"])
        depart_location = request.data["depart_location"]
        depart_lat_long = request.data["depart_lat_long"]
        depart_time = request.data["depart_time"]
        depart_terminal=request.data["depart_terminal"]
        depart_gate=request.data["depart_gate"]
        arrival_location=request.data["arrival_location"]
        arrival_lat_long =request.data["arrival_lat_long"]
        arrival_time =request.data["arrival_time"]
        arrival_terminal=request.data["arrival_terminal"]
        arrival_gate=request.data["arrival_gate"]
        airlines=request.data["airlines"]
        flight_number=request.data["flight_number"]
        flight_class=request.data["flight_class"]
        wather=request.data["wather"]
        
        id=self.kwargs["pk"]

        if not FlightBook.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "flightbook id is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        flightbook=FlightBook.objects.get(id=id)
        flightbook.user=user
        flightbook.gig=gig
        flightbook.depart_location=depart_location
        flightbook.depart_lat_long=depart_lat_long
        flightbook.depart_time=depart_time
        flightbook.depart_terminal=depart_terminal
        flightbook.depart_gate=depart_gate
        flightbook.arrival_location=arrival_location
        flightbook.arrival_lat_long=arrival_lat_long
        flightbook.arrival_time=arrival_time
        flightbook.arrival_terminal=arrival_terminal
        flightbook.arrival_gate=arrival_gate
        flightbook.airlines=airlines
        flightbook.flight_number=flight_number
        flightbook.flight_class=flight_class
        flightbook.wather=wather
        flightbook.save()

        response_data = {
            "id":flightbook.id,
            "user":  str(flightbook.user),
            "gig":str(flightbook.gig),
            "depart_location": flightbook.depart_location,
            "depart_lat_long": flightbook.depart_lat_long,
            "depart_time": flightbook.depart_time,
            "depart_terminal":flightbook.depart_terminal,
            "depart_gate":flightbook.depart_gate,
            "arrival_location":flightbook.arrival_location,
            "arrival_lat_long":flightbook.arrival_lat_long,
            "arrival_time":flightbook.arrival_time,
            "arrival_terminal":flightbook.arrival_terminal,
            "arrival_gate":flightbook.arrival_gate,
            "airlines":flightbook.airlines  ,
            "flight_number":flightbook.flight_number,
            "flight_class":flightbook.flight_class,
            "wather":flightbook.wather,
            }
        return Response(data={"status": status.HTTP_200_OK,
                            "message": "flightbook Updated",
                            "results": {'data': response_data}},
                        status=status.HTTP_200_OK)
class FlightBookListAPIView(ListAPIView):
    serializer_class =FlightBookSerializer
    queryset=FlightBook.objects.all()
    
    def get(self, request, *args, **kwargs):
        # print(request.user,"------------------")
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Flightbook list",
                                 "result": serializer.data},
                                status=status.HTTP_200_OK)

class FlightBookDeleteAPIView(DestroyAPIView):
    serializer_class = FlightBookSerializer

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        if FlightBook.objects.filter(id=id).exists():
            flightbook = FlightBook.objects.get(id=id)
            flightbook.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

class CabBookCreateAPIView(CreateAPIView):
    serializer_class = CabBookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user= User.objects.get(id=request.data["user"])
        gig= Gigs.objects.get(id=request.data["gig"])
        depart_location = request.data["depart_location"]
        depart_lat_long = request.data["depart_lat_long"]
        depart_time = request.data["depart_time"]
        arrival_location=request.data["arrival_location"]
        arrival_lat_long =request.data["arrival_lat_long"]
        arrival_time =request.data["arrival_time"]
        driver_name=request.data["driver_name"]
        driver_number=request.data["driver_number"]
        wather=request.data["wather"]

        cabbook=CabBook.objects.create(user=user,gig=gig,depart_location=depart_location,depart_lat_long=depart_lat_long,
        depart_time=depart_time,arrival_location=arrival_location,
        arrival_lat_long=arrival_lat_long,arrival_time=arrival_time,
        driver_name=driver_name,driver_number=driver_number,wather=wather)

        response_data = {
            "id":cabbook.id,
            "user":  str(cabbook.user),
            "gig":str(cabbook.gig),
            "depart_location": cabbook.depart_location,
            "depart_lat_long": cabbook.depart_lat_long,
            "depart_time": cabbook.depart_time,
            "arrival_location":cabbook.arrival_location,
            "arrival_lat_long":cabbook.arrival_lat_long,
            "arrival_time":cabbook.arrival_time,
            "driver_name":cabbook.driver_name,
            "driver_number":cabbook.driver_number,
            "wather":cabbook.wather,
            }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "cabbook created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)

class CabBookUpdateAPIView(CreateAPIView):
    serializer_class=CabBookSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user= User.objects.get(id=request.data["user"])
        gig= Gigs.objects.get(id=request.data["gig"])
        depart_location = request.data["depart_location"]
        depart_lat_long = request.data["depart_lat_long"]
        depart_time = request.data["depart_time"]
        arrival_location=request.data["arrival_location"]
        arrival_lat_long =request.data["arrival_lat_long"]
        arrival_time =request.data["arrival_time"]
        driver_name=request.data["driver_name"]
        driver_number=request.data["driver_number"]
        wather=request.data["wather"]
        
        id=self.kwargs["pk"]

        if not CabBook.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "cabbook id is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        cabbook=CabBook.objects.get(id=id)
        cabbook.user=user
        cabbook.gig=gig
        cabbook.depart_location=depart_location
        cabbook.depart_lat_long=depart_lat_long
        cabbook.depart_time=depart_time
        cabbook.arrival_location=arrival_location
        cabbook.arrival_lat_long=arrival_lat_long
        cabbook.arrival_time=arrival_time
        cabbook.driver_name=driver_name
        cabbook.driver_number=driver_number
        cabbook.wather=wather
        cabbook.save()

        response_data = {
            "id":cabbook.id,
            "user":  str(cabbook.user),
            "gig":str(cabbook.gig),
            "depart_location": cabbook.depart_location,
            "depart_lat_long": cabbook.depart_lat_long,
            "depart_time": cabbook.depart_time,
            "arrival_location":cabbook.arrival_location,
            "arrival_lat_long":cabbook.arrival_lat_long,
            "arrival_time":cabbook.arrival_time,
            "driver_name":cabbook.driver_name,
            "driver_number":cabbook.driver_number,
            "wather":cabbook.wather,
            }

        return Response(data={"status": status.HTTP_200_OK,
                            "message": "cabbook Updated",
                            "results": {'data': response_data}},
                        status=status.HTTP_200_OK)

class CabBookListAPIView(ListAPIView):
    serializer_class =CabBookSerializer
    queryset=CabBook.objects.all()
    
    def get(self, request, *args, **kwargs):
        # print(request.user,"------------------")
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "cabbook list",
                                 "result": serializer.data},
                                status=status.HTTP_200_OK)

class CabBookDeleteAPIView(DestroyAPIView):
    serializer_class = CabBookSerializer

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        if CabBook.objects.filter(id=id).exists():
            cabbook = CabBook.objects.get(id=id)
            cabbook.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)


class VenueCreateAPIView(CreateAPIView):
    serializer_class = VenueSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user= User.objects.get(id=request.data["user"])
        gig= Gigs.objects.get(id=request.data["gig"])
        address = request.data["address"]
        direction = request.data["direction"]
        website = request.data["website"]
        number=request.data["number"]
        indoor =request.data["indoor"]
        covered =request.data["covered"]
        capacity=request.data["capacity"]
        wather=request.data["wather"]
        credential_collection=request.data["credential_collection"]
        dressing_room=request.data["dressing_room"]
        hospitality=request.data["hospitality"]
        hospitality_detail=request.data["hospitality_detail"]
        catring=request.data["catring"]
        catring_detail=request.data["catring_detail"]

        venue=Venue.objects.create(user=user,gig=gig,address=address,direction=direction,website=website,number=number,
        indoor=indoor,covered=covered,
        capacity=capacity,credential_collection=credential_collection,dressing_room=dressing_room,hospitality=hospitality
        ,hospitality_detail=hospitality_detail,catring=catring,catring_detail=catring_detail,wather=wather)

        response_data = {
            "user":str(venue.user),
            "gig":str(venue.gig),
            "id":venue.id,
            "address": venue.address,
            "direction": venue.direction,
            "website": venue.website,
            "number": venue.number,
            "indoor": venue.indoor,
            "covered":venue.covered,
            "capacity":venue.capacity,
            "credential_collection":venue.credential_collection,
            "dressing_room":venue.dressing_room,
            "hospitality":venue.hospitality,
            "hospitality_detail":venue.hospitality_detail,
            "catring":venue.catring,
            "catring_detail":venue.catring_detail,
            "wather":venue.wather,

            }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "Venue created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)  

class VenueUpdateAPIView(CreateAPIView):
    serializer_class=VenueSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        user= User.objects.get(id=request.data["user"])
        gig= Gigs.objects.get(id=request.data["gig"])
        address = request.data["address"]
        direction = request.data["direction"]
        website = request.data["website"]
        number=request.data["number"]
        indoor =request.data["indoor"]
        covered =request.data["covered"]
        capacity=request.data["capacity"]
        wather=request.data["wather"]
        credential_collection=request.data["credential_collection"]
        dressing_room=request.data["dressing_room"]
        hospitality=request.data["hospitality"]
        hospitality_detail=request.data["hospitality_detail"]
        catring=request.data["catring"]
        catring_detail=request.data["catring_detail"]
        
        id=self.kwargs["pk"]

        if not Venue.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "venue id is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        vanue=Venue.objects.get(id=id)
        vanue.user=user
        vanue.gig=gig
        vanue.address=address
        vanue.direction=direction
        vanue.website=website
        vanue.number=number
        vanue.indoor=indoor
        vanue.covered=covered
        vanue.capacity=capacity
        vanue.wather=wather
        vanue.credential_collection=credential_collection
        vanue.dressing_room=dressing_room
        vanue.hospitality=hospitality
        vanue.hospitality_detail=hospitality_detail
        vanue.catring=catring
        vanue.catring_detail=catring_detail
        vanue.save()

        response_data = {
            "id":vanue.id,
            "user":str(vanue.user),
            "gig":str(vanue.gig),
            "address": vanue.address,
            "direction": vanue.direction,
            "website": vanue.website,
            "number": vanue.number,
            "indoor": vanue.indoor,
            "covered":vanue.covered,
            "capacity":vanue.capacity,
            "wather":vanue.wather,
            "credential_collection":vanue.credential_collection,
            "dressing_room":vanue.dressing_room,
            "hospitality":vanue.hospitality,
            "hospitality_detail":vanue.hospitality_detail,
            "catring":vanue.catring,
            "catring_detail":vanue.catring_detail
            }

        return Response(data={"status": status.HTTP_200_OK,
                            "message": "Venue Updated",
                            "results": {'data': response_data}},
                        status=status.HTTP_200_OK)

class VenueListAPIView(ListAPIView):
    serializer_class =VenueSerializer
    queryset=Venue.objects.all()
    
    def get(self, request, *args, **kwargs):
        # print(request.user,"------------------")
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Venue list",
                                 "result": serializer.data},
                                status=status.HTTP_200_OK)

class VenueDeleteAPIView(DestroyAPIView):
    serializer_class = VenueSerializer

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        if Venue.objects.filter(id=id).exists():
            venue = Venue.objects.get(id=id)
            venue.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

class HotelCreateAPIView(CreateAPIView):
    serializer_class = HotelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        user= User.objects.get(id=request.data["user"])
        gig= Gigs.objects.get(id=request.data["gig"])
        hotel_name=request.data["hotel_name"]
        address = request.data["address"]
        direction = request.data["direction"]
        website = request.data["website"]
        number=request.data["number"]
        wifi_paid_for =request.data["wifi_paid_for"]
        room_buyout =request.data["room_buyout"]
        

        hotel=Hotel.objects.create(user=user,gig=gig,hotel_name=hotel_name,address=address,direction=direction,website=website,number=number,
        wifi_paid_for=wifi_paid_for,room_buyout=room_buyout,)

        response_data = {
            "id":hotel.id,
            "user":str(hotel.user),
            "gig":str(hotel.gig),
            "hotel_name":hotel.hotel_name,
            "address": hotel.address,
            "direction": hotel.direction,
            "website": hotel.website,
            "number": hotel.number,
            "wifi_paid_for": hotel.wifi_paid_for,
            "room_buyout":hotel.room_buyout,
            }

        return Response(data={"status": status.HTTP_200_OK,
                              "message": "Hotel created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)  

class HotelUpdateAPIView(CreateAPIView):
    serializer_class=HotelSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        user= User.objects.get(id=request.data["user"])
        gig= Gigs.objects.get(id=request.data["gig"])
        address = request.data["address"]
        direction = request.data["direction"]
        website = request.data["website"]
        number=request.data["number"]
        wifi_paid_for =request.data["wifi_paid_for"]
        room_buyout =request.data["room_buyout"]
        
        id=self.kwargs["pk"]

        if not Hotel.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
             "message": "hotel {} id is not exists".format(id)},status=status.HTTP_400_BAD_REQUEST)

        hotel=Hotel.objects.get(id=id)
        hotel.user=user
        hotel.gig=gig
        hotel.address=address
        hotel.direction=direction
        hotel.website=website
        hotel.number=number
        hotel.wifi_paid_for=wifi_paid_for
        hotel.room_buyout=room_buyout
        hotel.save()

        response_data = {
            "id":hotel.id,
            "user":str(hotel.user),
            "gig":str(hotel.gig),
            "address": hotel.address,
            "direction": hotel.direction,
            "website": hotel.website,
            "number": hotel.number,
            "wifi_paid_for": hotel.wifi_paid_for,
            "room_buyout":hotel.room_buyout,
            }

        return Response(data={"status": status.HTTP_200_OK,
                            "message": "Hotel Updated",
                            "results": {'data': response_data}},
                        status=status.HTTP_200_OK)

class HotelListAPIView(ListAPIView):
    serializer_class =HotelSerializer
    queryset=Hotel.objects.all()
    
    def get(self, request, *args, **kwargs):
        # print(request.user,"------------------")
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Hotel list",
                                 "result": serializer.data},
                                status=status.HTTP_200_OK)

class HotelDeleteAPIView(DestroyAPIView):
    serializer_class = HotelSerializer

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        if Hotel.objects.filter(id=id).exists():
            hotel = Hotel.objects.get(id=id)
            hotel.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

class ContactCreateAPIView(CreateAPIView):
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        gig=Gigs.objects.get(id=request.data["gig"])
        type = request.data["type"]
        name = request.data["name"]
        number = request.data["number"]
        email=request.data["email"]
        travelling_party =request.data["travelling_party"]

        contact=Contacts.objects.create(gig=gig,type=type,name=name,number=number,email=email,travelling_party=travelling_party)

        response_data = {
            "id":contact.id,
            "gig":str(contact.gig),
            "type": contact.type,
            "name": contact.name,
            "number": contact.number,
            "email": contact.email,
            "travelling_party": contact.travelling_party,
            }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "Contact created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)  

class ContactUpdateAPIView(CreateAPIView):
    serializer_class=ContactSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        gig=Gigs.objects.get(id=request.data["gig"])
        type = request.data["type"]
        name = request.data["name"]
        number = request.data["number"]
        email=request.data["email"]
        travelling_party =request.data["travelling_party"]
        
        id=self.kwargs["pk"]

        if not Contacts.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
             "message": "contact {} id is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

        contact=Contacts.objects.get(id=id)
        contact.gig=gig
        contact.type=type
        contact.name=name
        contact.number=number
        contact.email=email
        contact.travelling_party=travelling_party
        contact.save()

        response_data = {
            "id":contact.id,
            "gig": str(contact.gig),
            "type": contact.type,
            "name": contact.name,
            "number": contact.number,
            "email": contact.email,
            "travelling_party":contact.travelling_party,
            }
        return Response(data={"status": status.HTTP_200_OK,
                            "message": "Contact Updated",
                            "results": {'data': response_data}},
                        status=status.HTTP_200_OK)
class ContactListAPIView(ListAPIView):
    serializer_class =ContactSerializer
    queryset=Contacts.objects.all()
    
    def get(self, request, *args, **kwargs):
        # print(request.user,"------------------")
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Hotel list",
                                 "result": serializer.data},
                                status=status.HTTP_200_OK)

class ContactDeleteAPIView(DestroyAPIView):
    serializer_class = ContactSerializer

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        if Contacts.objects.filter(id=id).exists():
            contact = Contacts.objects.get(id=id)
            contact.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

class DocumentCreateAPIView(CreateAPIView):
    serializer_class= DocumentSerializer

    def post(self,request, *args, **kwargs):
        serializer= self.get_serializer(data= request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        gig=Gigs.objects.get(id=request.data["gig"])
        boarding_passes=request.data["boarding_passes"]
        flight_confirmation_ticket= request.data["flight_confirmation_ticket"]
        hotel_voucher= request.data["hotel_voucher"]

        document= Documents.objects.create(gig=gig,boarding_passes=boarding_passes,flight_confirmation_ticket=flight_confirmation_ticket
        ,hotel_voucher=hotel_voucher)

        response_data={
            "id":document.id,
            "gig":str(document.gig),
            "boarding_passes":document.boarding_passes,
            "flight_confirmation_ticket":document.flight_confirmation_ticket,
            "hotel_voucher":document.hotel_voucher
        }
        return Response(data={"status":status.HTTP_200_OK,
                              "error":False,
                              "message":"document created",
                              "result":{'data':response_data}},
                        status=status.HTTP_200_OK)


class DocumentUpdateAPIView(CreateAPIView):
    serializer_class=DocumentSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        gig=Gigs.objects.get(id=request.data["gig"])
        boarding_passes = request.data["boarding_passes"]
        flight_confirmation_ticket = request.data["flight_confirmation_ticket"]
        hotel_voucher=request.data["hotel_voucher"]
        
        id=self.kwargs["pk"]

        if not Documents.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
             "message": "Document {} id is not exists".format(id)},status=status.HTTP_400_BAD_REQUEST)

        document=Documents.objects.get(id=id)
        document.gig=gig
        document.boarding_passes=boarding_passes
        document.flight_confirmation_ticket=flight_confirmation_ticket
        document.hotel_voucher=hotel_voucher
        document.save()

        response_data = {
            "id":document.id,
            "gig":str(document.gig),
            "boarding_passes": document.boarding_passes,
            "flight_confirmation_ticket": document.flight_confirmation_ticket,
            "hotel_voucher": document.hotel_voucher,
            }
        return Response(data={"status": status.HTTP_200_OK,
                            "message": "document Updated",
                            "results": response_data},
                        status=status.HTTP_200_OK)
class DocumentListAPIView(ListAPIView):
    serializer_class=DocumentSerializer
    queryset= Documents.objects.all()

    def get(self,request, *args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        return Response(data={"status":status.HTTP_200_OK,
                                "error":False,
                                "message":"document list",
                                "result":serializer.data},
                        status=status.HTTP_200_OK)

class DocumentDeleteAPIView(DestroyAPIView):
    serializer_class=DocumentSerializer
    def delete(self,request, *args,**kwargs):
        id = self.kwargs["pk"]
        if Documents.objects.filter(id=id).exists():
            document=Documents.objects.get(id=id)
            document.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

class GuestListCreateAPIView(CreateAPIView):
    serializer_class=GuestListSerializer
    def post(self,request,*args,**kwargs):
        serializer= self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status":status.HTTP_400_BAD_REQUEST,
                                "error":serializer.errors,},
                        status=status.HTTP_400_BAD_REQUEST)
        gig=Gigs.objects.get(id=request.data["gig"])
        guestlist_detail=request.data["guestlist_detail"]
        guestlist= request.data["guestlist"]

        guestl= GuestList.objects.create(gig=gig,guestlist_detail=guestlist_detail,guestlist=guestlist)

        response_data={
            "id":guestl.id,
            "gig":str(guestl.gig),
            "guestlist_detail":guestl.guestlist_detail,
            "guestlist":guestl.guestlist,
        }
        return Response(data={"status":status.HTTP_200_OK,
                                "error":False,
                                "message":"guestlist created",
                                "result":{'data':response_data}},
                        status=status.HTTP_200_OK)

class GuestListUpdateAPIView(CreateAPIView):
    serializer_class=GuestListSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        gig=Gigs.objects.get(id=request.data["gig"])
        guestlist_detail = request.data["guestlist_detail"]
        guestlist = request.data["guestlist"]
        
        id=self.kwargs["pk"]

        if not Documents.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
             "message": "guestlist {} id is not exists".format(id)},status=status.HTTP_400_BAD_REQUEST)

        guestl=GuestList.objects.get(id=id)
        guestl.gig=gig
        guestl.guestlist_detail=guestlist_detail
        guestl.guestlist=guestlist
        guestl.save()

        response_data = {
            "id":guestl.id,
            "gig":str(guestl.gig),
            "guestlist_detail": guestl.guestlist_detail,
            "guestlist": guestl.guestlist,
            }
        return Response(data={"status": status.HTTP_200_OK,
                            "message": "guestlist Updated",
                            "results": response_data},
                        status=status.HTTP_200_OK)

class GuestListListAPIView(ListAPIView):
    serializer_class=GuestListSerializer
    queryset= GuestList.objects.all()

    def get(self,request, *args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        return Response(data={"status":status.HTTP_200_OK,
                                "error":False,
                                "message":"guestlist list",
                                "result":serializer.data},
                        status=status.HTTP_200_OK)

class GuestListDeleteAPIView(DestroyAPIView):
    serializer_class= GuestListSerializer
    def delete(self,request,*args,**kwargs):
        id = self.kwargs["pk"]
        if GuestList.objects.filter(id=id).exists():
            guestl=GuestList.objects.get(id=id)
            guestl.delete()
            return Response({"res": "id {} deleted!".format(id)}, status=status.HTTP_200_OK)
        else:
            return Response({"res": "id {} is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

class SetTimeCreateAPIView(CreateAPIView):
    serializer_class=SetTimeSerialiazer
    def post(self,request,*args,**kwargs):
        serializer= self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status":status.HTTP_400_BAD_REQUEST,
                                "error":serializer.errors,},
                        status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.get(id=request.data["user"])
        gig=Gigs.objects.get(id=request.data["gig"])
        venue=Venue.objects.get(id=request.data["venue"])
        start=request.data["start"]
        finish= request.data["finish"]

        settime= SetTime.objects.create(user=user,gig=gig,venue=venue,start=start,finish=finish)

        response_data={
            "id":settime.id,
            "user":str(settime.user),
            "gig":str(settime.gig),
            "venue":str(settime.venue),
            "start":settime.start,
            "finish":settime.finish
        }
        return Response(data={"status":status.HTTP_200_OK,
                                "error":False,
                                "message":"settime created",
                                "result":{'data':response_data}},
                        status=status.HTTP_200_OK)    

class SetTimeUpdateAPIView(CreateAPIView):
    serializer_class=SetTimeSerialiazer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.get(id=request.data["user"])
        gig=Gigs.objects.get(id=request.data["gig"])
        venue=Venue.objects.get(id=request.data["venue"])
        start=request.data["start"]
        finish= request.data["finish"]
        
        id=self.kwargs["pk"]

        if not SetTime.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
             "message": "settime {} id is not exists".format(id)},status=status.HTTP_400_BAD_REQUEST)

        settime=SetTime.objects.get(id=id)
        settime.user=user
        settime.gig=gig
        settime.venue=venue
        settime.start=start
        settime.finish=finish
        settime.save()

        response_data = {
            "id":settime.id,
            "user":str(settime.user),
            "gig":str(settime.gig),
            "venue":str(settime.venue),
            "start": settime.start,
            "finish": settime.finish,
            }
        return Response(data={"status": status.HTTP_200_OK,
                            "message": "settime Updated",
                            "results": response_data},
                        status=status.HTTP_200_OK)

class SetTimeListAPIView(ListAPIView):
    serializer_class=SetTimeSerialiazer
    queryset= SetTime.objects.all()

    def get(self,request, *args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        return Response(data={"status":status.HTTP_200_OK,
                                "error":False,
                                "message":"SETTIME list",
                                "result":serializer.data},
                        status=status.HTTP_200_OK)












class AllDataAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    # serializer_class = LoginUserSerializers
    # flights = FlightBook.objects.all()


    def get(self, request, *args, **kwargs):
        response = {}
        final = []
        users = User.objects.all()
        for user in users:
            gigs = Gigs.objects.filter(user=user)
            gig_list = []
            
            flight_list = []
            for gig in gigs:
                
                flights = FlightBook.objects.filter(gig=gig)
                for flight in flights:
                    print(flight,'----------flight-------')
                    flight_list.append({
                        "id": flight.id,
                        "depart_location": flight.depart_location,
                        "depart_lat_long": flight.depart_lat_long,
                        "depart_time": flight.depart_time,
                        "depart_terminal": flight.depart_terminal,
                        "depart_gate": flight.depart_gate,
                        "arrival_location": flight.arrival_location,
                        "arrival_lat_long": flight.arrival_lat_long,
                        "arrival_time": flight.arrival_time,
                        "arrival_terminal": flight.arrival_terminal,
                        "arrival_gate": flight.arrival_gate,
                        "airlines": flight.airlines,
                        "flight_number": flight.flight_number,
                        "flight_class": flight.flight_class,
                        "wather": flight.wather,
                        "user": flight.user.id,
                        "gig": flight.gig.id
                    })

                gig_list.append({
                "id": gig.id,
                "title": gig.title,
                "descriptions": gig.descriptions,
                "profile_pic": gig.profile_pic,
                "cover_image": gig.cover_image,
                "location": gig.location,
                "show": gig.show,
                "stage": gig.stage,
                "visa": gig.visa,
                "Equipment": gig.Equipment,
                "date": gig.date,
                "sound_check_time": gig.sound_check_time,
                "user": gig.user.id,
                "flights":flight_list
                })



            final.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "gigs":gig_list
                
            })
        print(response)
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Schedule list",
                                 "result": final},
                                status=status.HTTP_200_OK)

class ScheduleAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    # serializer_class = LoginUserSerializers
    # flights = FlightBook.objects.all()


    def get(self, request, *args, **kwargs):
        response = {}
        final = []
        users = User.objects.all()
        
        flights = FlightBook.objects.all()
        cabs = CabBook.objects.all()
        for flight in flights:
            final.append({
                "type" : "flight",
                "flight_id": flight.id,
                "depart_location": flight.depart_location,
                "depart_lat_long": flight.depart_lat_long,
                "depart_time": flight.depart_time,
                "depart_terminal": flight.depart_terminal,
                "depart_gate": flight.depart_gate,
                "arrival_location": flight.arrival_location,
                "arrival_lat_long": flight.arrival_lat_long,
                "arrival_time": flight.arrival_time,
                "arrival_terminal": flight.arrival_terminal,
                "arrival_gate": flight.arrival_gate,
                "airlines": flight.airlines,
                "flight_number": flight.flight_number,
                "flight_class": flight.flight_class,
                "wather": flight.wather,
                "user": flight.user.id,
                "gig": flight.gig.id
            })

        for cab in cabs:
            final.append({
                "type" : "cab",
                "cab_id": cab.id,
                "depart_location": cab.depart_location,
                "depart_lat_long": cab.depart_lat_long,
                "depart_time": cab.depart_time,
                "arrival_location": cab.arrival_location,
                "arrival_lat_long": cab.arrival_lat_long,
                "arrival_time": cab.arrival_time,
                "driver_name": cab.driver_name,
                "driver_number": cab.driver_number,
                "wather": cab.wather,
                "user": cab.user.id,
                "gig": cab.gig.id
            })
        print(response)
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Schedule list",
                                 "result": final},
                                status=status.HTTP_200_OK)




class allListView(ListAPIView):
   serializer_class_UserSerializer = UserListSerializer
   serializer_class_GigsSerializer = GigsSerializer
   serializer_class_FlightSerializer = FlightSerializer
   serializer_class_CabBookSerializer = CabBookSerializer
   serializer_class_HotelListSerializer = HotelListSerializer
   serializer_class_VenueListSerializer = VenueListSerializer
   serializer_class_SetTimeSerializer= SetTimeSerialiazer

   def get(self, request, *args, **kwrgs):
      if request.method == 'GET':
        users = User.objects.all()
        gigs = Gigs.objects.all()
        flights = FlightBook.objects.all()
        cabs = CabBook.objects.all()
        hotels = Hotel.objects.all()
        venues = Venue.objects.all()
        settimes=SetTime.objects.all()

        seralizer1 = self.serializer_class_UserSerializer(users, many=True)
        seralizer2 = self.serializer_class_GigsSerializer(gigs, many=True)
        seralizer3 = self.serializer_class_FlightSerializer(flights, many=True)
        seralizer4 = self.serializer_class_CabBookSerializer(cabs, many=True)
        seralizer5 = self.serializer_class_HotelListSerializer(hotels, many=True)
        seralizer6 = self.serializer_class_VenueListSerializer(venues, many=True)

        final = []
        users = User.objects.all()
        
        flights = FlightBook.objects.all()
        cabs = CabBook.objects.all()
        for flight in flights:
            final.append({
                "type" : "flight",
                "flight_id": flight.id,
                "depart_location": flight.depart_location,
                "depart_lat_long": flight.depart_lat_long,
                "depart_time": flight.depart_time,
                "depart_terminal": flight.depart_terminal,
                "depart_gate": flight.depart_gate,
                "arrival_location": flight.arrival_location,
                "arrival_lat_long": flight.arrival_lat_long,
                "arrival_time": flight.arrival_time,
                "arrival_terminal": flight.arrival_terminal,
                "arrival_gate": flight.arrival_gate,
                "airlines": flight.airlines,
                "flight_number": flight.flight_number,
                "flight_class": flight.flight_class,
                "wather": flight.wather,
                "user": flight.user.id,
                "gig": flight.gig.id
            })

        for cab in cabs:
            final.append({
                "type" : "cab",
                "cab_id": cab.id,
                "depart_location": cab.depart_location,
                "depart_lat_long": cab.depart_lat_long,
                "depart_time": cab.depart_time,
                "arrival_location": cab.arrival_location,
                "arrival_lat_long": cab.arrival_lat_long,
                "arrival_time": cab.arrival_time,
                "driver_name": cab.driver_name,
                "driver_number": cab.driver_number,
                "wather": cab.wather,
                "user": cab.user.id,
                "gig": cab.gig.id
            })
        for settime in settimes:
            final.append({
                "type":"settime",
                "settime_id":settime.id,
                "user":str(settime.user),
                "gig":str(settime.gig),
                "venue":str(settime.venue),
                "start":settime.start,
                "finish":settime.finish
            })

        response = {
            'users':seralizer1.data,
            'gigs':seralizer2.data,
            'hotels':seralizer5.data,
            'venues':seralizer6.data,
            # 'flights':seralizer3.data,
            # 'cabs':seralizer4.data,
            "schedule" : final
            }
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Schedule list",
                                    "result": response},
                                status=status.HTTP_200_OK)


class ScheduleAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    # serializer_class = LoginUserSerializers
    # flights = FlightBook.objects.all()


    def get(self, request, *args, **kwargs):
        response = {}
        final = []
        users = User.objects.all()

        flights = FlightBook.objects.all()
        cabs = CabBook.objects.all()
        for flight in flights:
            final.append({
            "type" : "flight",
            "flight_id": flight.id,
            "depart_location": flight.depart_location,
            "depart_lat_long": flight.depart_lat_long,
            "depart_time": flight.depart_time,
            "depart_terminal": flight.depart_terminal,
            "depart_gate": flight.depart_gate,
            "arrival_location": flight.arrival_location,
            "arrival_lat_long": flight.arrival_lat_long,
            "arrival_time": flight.arrival_time,
            "arrival_terminal": flight.arrival_terminal,
            "arrival_gate": flight.arrival_gate,
            "airlines": flight.airlines,
            "flight_number": flight.flight_number,
            "flight_class": flight.flight_class,
            "wather": flight.wather,
            "user": flight.user.id,
            "gig": flight.gig.id
            })

            for cab in cabs:
                final.append({
                "type" : "cab",
                "cab_id": cab.id,
                "depart_location": cab.depart_location,
                "depart_lat_long": cab.depart_lat_long,
                "depart_time": cab.depart_time,
                "arrival_location": cab.arrival_location,
                "arrival_lat_long": cab.arrival_lat_long,
                "arrival_time": cab.arrival_time,
                "driver_name": cab.driver_name,
                "driver_number": cab.driver_number,
                "wather": cab.wather,
                "user": cab.user.id,
                "gig": cab.gig.id
                })


                print(response)
                return Response(data={"status": status.HTTP_200_OK,
                "error": False,
                "message": "Schedule list",
                "result": final},
                status=status.HTTP_200_OK)