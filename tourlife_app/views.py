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


class CreateUserAPIView(GenericAPIView):
    # permission_classes = [AllowAny]
    serializer_class = CreateUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
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
        # print(request.FILES['profile_image'], "////////////////////////")
        # profile_image = request.FILES.get("profile_image")

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

class UpdateUserAPIView(CreateAPIView):
    serializer_class=CreateUserSerializers
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
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

        if User.objects.filter(id=id).exists():
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

class ListUserAPIView(ListAPIView):
    serializer_class=CreateUserSerializers
    queryset=User.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializers


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error':True, 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
       
        user = User.objects.get(email=email)
        print(user.email,'-------------------------')

        if user is not None:
            if not user.password == password:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid username or password"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid username or password"},status=status.HTTP_400_BAD_REQUEST)


        if user:
            payload={"email":user.email,"password":user.password}

            print(payload)
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            # jwt_token=jwt.encode(payload,settings.SECRET_KEY, algorithm ="HS256")
            # jwt_token = jwt.JWT.encode(payload,settings.SECRET_KEY, algorithm ="HS256")

            # UserToken.objects.create(user=user, token=jwt_token)
            return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "User Login Successfully.",
                                 "result": {'id': user.id,
                                            'first_name':user.first_name, 
                                            'last_name':user.last_name, 
                                            'token': jwt_token,
                                            'is_manager': user.is_superuser}},
                                status=status.HTTP_200_OK)

class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializers


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error':True, 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
       
        user = User.objects.get(email=email)
        print(user.email,'-------------------------')

        if user is not None:
            if not user.password == password:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid username or password"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid username or password"},status=status.HTTP_400_BAD_REQUEST)


        if user:
            payload={"email":user.email,"password":user.password}

            print(payload)
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            # jwt_token=jwt.encode(payload,settings.SECRET_KEY, algorithm ="HS256")
            # jwt_token = jwt.JWT.encode(payload,settings.SECRET_KEY, algorithm ="HS256")

            # UserToken.objects.create(user=user, token=jwt_token)
            return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "User Login Successfully.",
                                 "result": {'id': user.id,
                                            'first_name':user.first_name, 
                                            'last_name':user.last_name, 
                                            'token': jwt_token,
                                            'is_manager': user.is_superuser}},
                                status=status.HTTP_200_OK)



# class LoginAPIView(GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class =LoginUserSerializers

#     def post(self, request, *args, **kwargs):
#         serializer=self.get_serializer(data=request.POST)
#         # print(serializer,'------------------------')
#         if serializer.is_valid():

#             email=serializer.validated_data["email"]
#             password=serializer.validated_data["password"]
            
#             email=request.POST["email"]
#             user_exists= User.objects.filter(email=email,password=password)
#             if user_exists.exists():
#                 user= User.objects.get(email=email,password=password)
#                 payload={"email":user.email,"password":user.password}

#                 jwt_token=jwt.encode(payload,settings.SECRET_KEY, algorithm ="HS256")
#                 # print(jwt_token,"========================================")
#                 if Usertoken.objects.filter(user=user).exists():
#                     Usertoken.objects.update(user=user,token=jwt_token)
#                 else:
#                     Usertoken.objects.create(user=user,token=jwt_token)
                    
#                 return Response(data={'status':status.HTTP_200_OK, 'message':"sucessfully login",'result':{'data':jwt_token}}
#                 ,status=status.HTTP_200_OK)
#             else:
#                 return Response(data={'status':status.HTTP_400_BAD_REQUEST, 'message':"email or password is wrong"},
#                 status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(data={"status":status.HTTP_400_BAD_REQUEST, "error":True, "message":serializer.errors},
#              status=status.HTTP_400_BAD_REQUEST)

# class Person(GenericAPIView):
#     def get(self,request,*args,**kwargs):
#         return Response(data={'status':200, 'Message':'Hello world!'},status=200)

class GigsCreateAPIView(CreateAPIView):
    serializer_class = GigsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # print(serializer,'------------------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        # print(request.FILES.get("profile_pic","///////////////////////"))
        user= User.objects.get(id=request.data["user"])
        # user = request.data["user"]
        title = request.data["title"]
        descriptions = request.data["descriptions"]
        profile_pic = request.data["profile_pic"]
        cover_image=request.data["cover_image"]
        date=request.data["date"]

        

        gigs=Gigs.objects.create(user=user,title=title,descriptions=descriptions,
        profile_pic=profile_pic,cover_image=cover_image,date=date)

        response_data = {
            "id":gigs.id,
            "user":  str(gigs.user),
            "title": gigs.title,
            "descriptions": gigs.descriptions,
            "profile_pic": gigs.profile_pic,
            "cover_image":gigs.cover_image,
            "date":gigs.date
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "gigs created",
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



class UserListAPIView(ListAPIView):
    serializer_class =UserSerializer
    queryset=User.objects.all()
    
    def get(self, request, *args, **kwargs):
        # print(request.user,"------------------")
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset, many=True)
        print(serializer,"------")  
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Users list",
                                 "result": serializer.data},
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
                "gigs":gig_list,
                
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

   def get(self, request, *args, **kwrgs):
      if request.method == 'GET':
        users = User.objects.all()
        gigs = Gigs.objects.all()
        flights = FlightBook.objects.all()
        cabs = CabBook.objects.all()

        seralizer1 = self.serializer_class_UserSerializer(users, many=True)
        seralizer2 = self.serializer_class_GigsSerializer(gigs, many=True)
        seralizer3 = self.serializer_class_FlightSerializer(flights, many=True)
        seralizer4 = self.serializer_class_CabBookSerializer(cabs, many=True)

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

        response = {
            'users':seralizer1.data,
            'gigs':seralizer2.data,
            # 'flights':seralizer3.data,
            # 'cabs':seralizer4.data,
            "schedule" : final
            }
        return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "Schedule list",
                                    "result": response},
                                status=status.HTTP_200_OK)

          