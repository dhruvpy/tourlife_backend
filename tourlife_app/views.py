from django.db.models import Count
from .models import *
from .serializer import *
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.permissions import AllowAny
import boto3
import jwt
from django.conf import settings
from rest_framework.authentication import TokenAuthentication, get_authorization_header
import random

from django.conf import settings
from django.core.mail import send_mail
from .pagination import CustomPagination
from rest_framework.pagination import PageNumberPagination
import json


from tourlife_app import serializer


class UserCreateAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = CreateUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},status=status.HTTP_400_BAD_REQUEST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data["username"]
        last_name = request.data["last_name"]
        first_name = request.data["first_name"]
        email = request.data["email"]
        password = request.data["password"]
        mobile_no = request.data["mobile_no"]
        profile_image = request.data["profile_image"]

        if User.objects.filter(username=username).exists() | User.objects.filter(email=email).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "This email or username is already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, password=password, email=email, mobile_no=mobile_no,
                                   profile_image=profile_image)
        response_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
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
    permission_classes = [AllowAny]

    serializer_class = CreateUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},status=status.HTTP_400_BAD_REQUEST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data["username"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        password = request.data["password"]
        email = request.data["email"]
        mobile_no = request.data["mobile_no"]
        profile_image = request.data["profile_image"]

        id = self.kwargs["pk"]

        if not User.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        # if User.objects.filter(username=username).exists() | User.objects.filter(email=email).exists():
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "This email or username is already exists"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.password = password
        user.email = email
        user.mobile_no = mobile_no
        user.profile_image = profile_image
        user.save()

        response_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": user.password,
            "email": user.email,
            "mobile_no": user.mobile_no,
            "profile_image": str(user.profile_image)
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "user updated",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class MyPaginator(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1


class UserListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = ListUserSerializers
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class GetAllUserAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = ListUserSerializers
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "All user list",
                              "data": serializer.data},
                        status=status.HTTP_200_OK)


class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = CreateUserSerializers

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not User.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        user.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "User deleted"},
                        status=status.HTTP_200_OK)


class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error': True, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.filter(email=email, password=password).first()

        if not user:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error': True, 'message': "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {"email": user.email, "password": user.password}

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "User Login Successfully.",
                              "result": {'id': user.id,
                                         'first_name': user.first_name,
                                         'last_name': user.last_name,
                                         'token': jwt_token,
                                         'is_manager': user.is_manager}},
                        status=status.HTTP_200_OK)


class AdminLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error': True, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.filter(email=email, password=password).first()

        if not user:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error': True, 'message': "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_manager == True:
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error': True, 'message': "User is not allow"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {"email": user.email, "password": user.password}

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Admin User Login Successfully.",
                              "result": {'id': user.id,
                                         'first_name': user.first_name,
                                         'last_name': user.last_name,
                                         'token': jwt_token,
                                         'is_manager': user.is_manager}},
                        status=status.HTTP_200_OK)


class ForgotPasswordAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotpasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error': True, 'error_message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        if not User.objects.filter(email=email).exists():
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'error_message': "email is not registered", }, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            random_num = random.randint(1000, 9999)
            otp = random_num

            subject = 'send otp'
            message = 'your otp is {}'.format(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            Emailotp.objects.create(email=email, otp=otp)

            return Response(data={"Status": status.HTTP_200_OK, "error": False, 'message': 'We have sent you a otp to reset your password', "results": {"email": email, "otp": otp}}, status=status.HTTP_200_OK)


class OTPCheckAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        print(otp)
        email = request.data.get('email')

        if otp is None:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'error_message': 'please enter otp'}, status=status.HTTP_400_BAD_REQUEST)

        if email is None:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'error_message': 'please enter email address'}, status=status.HTTP_400_BAD_REQUEST)
        emailotp = Emailotp.objects.filter(email=email).last()

        if not emailotp:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'error_message': 'please enter valid email or otp'}, status=status.HTTP_400_BAD_REQUEST)

        if not emailotp.email == email and emailotp.otp == otp:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'error_message': 'otp is expire or not valid this mail'}, status=status.HTTP_400_BAD_REQUEST)

        emailotp.otp_check = True
        emailotp.save()
        return Response(data={'status': status.HTTP_200_OK, 'error': False, 'message': 'otp check please set new password'}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error': True, 'error_message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        new_password = request.data['new_password']
        user = User.objects.filter(email=email).last()
        emailotp_obj = Emailotp.objects.filter(email=user.email).last()
        if not user:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'error_message': 'please enter valid email'}, status=status.HTTP_400_BAD_REQUEST)
        user.password = new_password
        user.save()
        emailotp_obj.delete()
        return Response(data={'status': status.HTTP_200_OK, 'error': False, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)


class GigsCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = CreateGigsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # temp = Gigs.objects.filter(id=3)
        # for i in temp:
        #     print(i.user.all())
        #     temp2 = Gigs.objects.filter(id=2).first()
        #     temp2.user.set(i.user.all())
        #     temp2.save()
        user_id_list = request.data["user"]
        user_id_list = json.loads(user_id_list)
        # print(type(a))
        user = User.objects.filter(id__in=user_id_list)
        title = request.data["title"]
        descriptions = request.data["descriptions"]
        profile_pic = request.data["profile_pic"]
        cover_image = request.data["cover_image"]
        location = request.data["location"]
        show = request.data["show"]
        stage = request.data["stage"]
        visa = request.data["visa"]
        Equipment = request.data["Equipment"]
        date = request.data["date"]
        sound_check_time = request.data["sound_check_time"]

        gigs = Gigs.objects.create(title=title, descriptions=descriptions,
                                   profile_pic=profile_pic, cover_image=cover_image, location=location, show=show, stage=stage, visa=visa, Equipment=Equipment, sound_check_time=sound_check_time, date=date)
        gigs.user.set(user_id_list)
        gigs.save()
        response_data = {
            "id": gigs.id,
            "user":  str(gigs.user),
            "title": gigs.title,
            "descriptions": gigs.descriptions,
            "profile_pic": str(gigs.profile_pic),
            "cover_image": str(gigs.cover_image),
            "location": gigs.location,
            "show": gigs.show,
            "stage": gigs.stage,
            "visa": gigs.visa,
            "Equipment": gigs.Equipment,
            "date": str(gigs.date),
            "sound_check_time": gigs.sound_check_time
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "gigs created",
                              "error": False,
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class GigsUpdateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = CreateGigsSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user_id_list = request.data["user"]
        user_id_list = json.loads(user_id_list)
        # print(type(a))
        user = User.objects.filter(id__in=user_id_list)
        title = request.data["title"]
        descriptions = request.data["descriptions"]
        profile_pic = request.data["profile_pic"]
        cover_image = request.data["cover_image"]
        location = request.data["location"]
        show = request.data["show"]
        stage = request.data["stage"]
        visa = request.data["visa"]
        Equipment = request.data["Equipment"]
        date = request.data["date"]
        sound_check_time = request.data["sound_check_time"]

        id = self.kwargs["pk"]
        if not Gigs.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gigs is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        gigs = Gigs.objects.get(id=id)
        # gigs.user = user
        gigs.title = title
        gigs.descriptions = descriptions
        gigs.profile_pic = profile_pic
        gigs.cover_image = cover_image
        gigs.location = location
        gigs.show = show
        gigs.stage = stage
        gigs.visa = visa
        gigs.Equipment = Equipment
        gigs.date = date
        gigs.sound_check_time = sound_check_time
        gigs.user.set(user_id_list)

        gigs.save()

        response_data = {
            "id": gigs.id,
            "user": str(gigs.user),
            "title": gigs.title,
            "descriptions": gigs.descriptions,
            "profile_pic": str(gigs.profile_pic),
            "cover_image": str(gigs.cover_image),
            "location": gigs.location,
            "show": gigs.show,
            "stage": gigs.stage,
            "visa": gigs.visa,
            "Equipment": gigs.Equipment,
            "date": gigs.date,
            "sound_check_time": gigs.sound_check_time
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "Gigs updated",
                              "error": False,
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class GigsListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = ListGigSerializer
    queryset = Gigs.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class GetallGigsAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = ListGigSerializer
    queryset = Gigs.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "All gigs list",
                              "data": serializer.data},
                        status=status.HTTP_200_OK)


class GigsDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = CreateGigsSerializer

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not Gigs.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gigs is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        gigs = Gigs.objects.get(id=id)
        gigs.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Gigs deleted",
                              "result": serializer.data},
                        status=status.HTTP_200_OK)


class FlightBookCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = FlightBookSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        depart_location = request.data["depart_location"]
        depart_lat_long = request.data["depart_lat_long"]
        depart_time = request.data["depart_time"]
        depart_terminal = request.data["depart_terminal"]
        depart_gate = request.data["depart_gate"]
        arrival_location = request.data["arrival_location"]
        arrival_lat_long = request.data["arrival_lat_long"]
        arrival_time = request.data["arrival_time"]
        arrival_terminal = request.data["arrival_terminal"]
        arrival_gate = request.data["arrival_gate"]
        airlines = request.data["airlines"]
        flight_number = request.data["flight_number"]
        flight_class = request.data["flight_class"]
        wather = request.data["wather"]

        flightbook = FlightBook.objects.create(user=user, gig=gig, depart_location=depart_location, depart_lat_long=depart_lat_long,
                                               depart_time=depart_time, depart_terminal=depart_terminal, depart_gate=depart_gate, arrival_location=arrival_location,
                                               arrival_lat_long=arrival_lat_long, arrival_time=arrival_time, arrival_terminal=arrival_terminal,
                                               airlines=airlines, arrival_gate=arrival_gate, flight_number=flight_number, flight_class=flight_class, wather=wather)

        response_data = {
            "id": flightbook.id,
            "user":  str(flightbook.user),
            "gig": str(flightbook.gig),
            "depart_location": flightbook.depart_location,
            "depart_lat_long": flightbook.depart_lat_long,
            "depart_time": flightbook.depart_time,
            "depart_terminal": flightbook.depart_terminal,
            "depart_gate": flightbook.depart_gate,
            "arrival_location": flightbook.arrival_location,
            "arrival_lat_long": flightbook.arrival_lat_long,
            "arrival_time": flightbook.arrival_time,
            "arrival_terminal": flightbook.arrival_terminal,
            "arrival_gate": flightbook.arrival_gate,
            "airlines": flightbook.airlines,
            "flight_number": flightbook.flight_number,
            "flight_class": flightbook.flight_class,
            "wather": flightbook.wather,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "Flightbook created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class FlightBookUpdateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = FlightBookSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        depart_location = request.data["depart_location"]
        depart_lat_long = request.data["depart_lat_long"]
        depart_time = request.data["depart_time"]
        depart_terminal = request.data["depart_terminal"]
        depart_gate = request.data["depart_gate"]
        arrival_location = request.data["arrival_location"]
        arrival_lat_long = request.data["arrival_lat_long"]
        arrival_time = request.data["arrival_time"]
        arrival_terminal = request.data["arrival_terminal"]
        arrival_gate = request.data["arrival_gate"]
        airlines = request.data["airlines"]
        flight_number = request.data["flight_number"]
        flight_class = request.data["flight_class"]
        wather = request.data["wather"]

        id = self.kwargs["pk"]

        if not FlightBook.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Flightbook is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        flightbook = FlightBook.objects.get(id=id)
        flightbook.user = user
        flightbook.gig = gig
        flightbook.depart_location = depart_location
        flightbook.depart_lat_long = depart_lat_long
        flightbook.depart_time = depart_time
        flightbook.depart_terminal = depart_terminal
        flightbook.depart_gate = depart_gate
        flightbook.arrival_location = arrival_location
        flightbook.arrival_lat_long = arrival_lat_long
        flightbook.arrival_time = arrival_time
        flightbook.arrival_terminal = arrival_terminal
        flightbook.arrival_gate = arrival_gate
        flightbook.airlines = airlines
        flightbook.flight_number = flight_number
        flightbook.flight_class = flight_class
        flightbook.wather = wather
        flightbook.save()

        response_data = {
            "id": flightbook.id,
            "user":  str(flightbook.user),
            "gig": str(flightbook.gig),
            "depart_location": flightbook.depart_location,
            "depart_lat_long": flightbook.depart_lat_long,
            "depart_time": flightbook.depart_time,
            "depart_terminal": flightbook.depart_terminal,
            "depart_gate": flightbook.depart_gate,
            "arrival_location": flightbook.arrival_location,
            "arrival_lat_long": flightbook.arrival_lat_long,
            "arrival_time": flightbook.arrival_time,
            "arrival_terminal": flightbook.arrival_terminal,
            "arrival_gate": flightbook.arrival_gate,
            "airlines": flightbook.airlines,
            "flight_number": flightbook.flight_number,
            "flight_class": flightbook.flight_class,
            "wather": flightbook.wather,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "Flightbook Updated",
                              "error": False,
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class FlightBookListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = FlightSerializer
    queryset = FlightBook.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class GetallFlightAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = FlightSerializer
    queryset = FlightBook.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "All flightbook list",
                              "data": serializer.data},
                        status=status.HTTP_200_OK)


class FlightBookDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = FlightBookSerializer

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not FlightBook.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Flightbook is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        flightbook = FlightBook.objects.get(id=id)
        flightbook.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Flightbook deleted",
                              "result": serializer.data},
                        status=status.HTTP_200_OK)


class CabBookCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = CabBookSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        depart_location = request.data["depart_location"]
        depart_lat_long = request.data["depart_lat_long"]
        depart_time = request.data["depart_time"]
        arrival_location = request.data["arrival_location"]
        arrival_lat_long = request.data["arrival_lat_long"]
        arrival_time = request.data["arrival_time"]
        driver_name = request.data["driver_name"]
        driver_number = request.data["driver_number"]
        wather = request.data["wather"]

        cabbook = CabBook.objects.create(user=user, gig=gig, depart_location=depart_location, depart_lat_long=depart_lat_long,
                                         depart_time=depart_time, arrival_location=arrival_location,
                                         arrival_lat_long=arrival_lat_long, arrival_time=arrival_time,
                                         driver_name=driver_name, driver_number=driver_number, wather=wather)

        response_data = {
            "id": cabbook.id,
            "user":  str(cabbook.user),
            "gig": str(cabbook.gig),
            "depart_location": cabbook.depart_location,
            "depart_lat_long": cabbook.depart_lat_long,
            "depart_time": cabbook.depart_time,
            "arrival_location": cabbook.arrival_location,
            "arrival_lat_long": cabbook.arrival_lat_long,
            "arrival_time": cabbook.arrival_time,
            "driver_name": cabbook.driver_name,
            "driver_number": cabbook.driver_number,
            "wather": cabbook.wather,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "Cabbook created",
                              "error": False,
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class CabBookUpdateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = CabBookSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        depart_location = request.data["depart_location"]
        depart_lat_long = request.data["depart_lat_long"]
        depart_time = request.data["depart_time"]
        arrival_location = request.data["arrival_location"]
        arrival_lat_long = request.data["arrival_lat_long"]
        arrival_time = request.data["arrival_time"]
        driver_name = request.data["driver_name"]
        driver_number = request.data["driver_number"]
        wather = request.data["wather"]

        id = self.kwargs["pk"]

        if not CabBook.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Cabbook is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        cabbook = CabBook.objects.get(id=id)
        cabbook.user = user
        cabbook.gig = gig
        cabbook.depart_location = depart_location
        cabbook.depart_lat_long = depart_lat_long
        cabbook.depart_time = depart_time
        cabbook.arrival_location = arrival_location
        cabbook.arrival_lat_long = arrival_lat_long
        cabbook.arrival_time = arrival_time
        cabbook.driver_name = driver_name
        cabbook.driver_number = driver_number
        cabbook.wather = wather
        cabbook.save()

        response_data = {
            "id": cabbook.id,
            "user":  str(cabbook.user),
            "gig": str(cabbook.gig),
            "depart_location": cabbook.depart_location,
            "depart_lat_long": cabbook.depart_lat_long,
            "depart_time": cabbook.depart_time,
            "arrival_location": cabbook.arrival_location,
            "arrival_lat_long": cabbook.arrival_lat_long,
            "arrival_time": cabbook.arrival_time,
            "driver_name": cabbook.driver_name,
            "driver_number": cabbook.driver_number,
            "wather": cabbook.wather,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "Cabbook Updated",
                              "error": False,
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class CabBookListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = CabSerializer
    queryset = CabBook.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class CabBookDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = CabBookSerializer

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not CabBook.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Cabbook is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        cabbook = CabBook.objects.get(id=id)
        cabbook.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Cabbook deleted",
                              "result": serializer.data},
                        status=status.HTTP_200_OK)


class VenueCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = VenueSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        address = request.data["address"]
        direction = request.data["direction"]
        website = request.data["website"]
        number = request.data["number"]
        indoor = request.data["indoor"]
        covered = request.data["covered"]
        capacity = request.data["capacity"]
        wather = request.data["wather"]
        credential_collection = request.data["credential_collection"]
        dressing_room = request.data["dressing_room"]
        hospitality = request.data["hospitality"]
        hospitality_detail = request.data["hospitality_detail"]
        catring = request.data["catring"]
        catring_detail = request.data["catring_detail"]

        venue = Venue.objects.create(user=user, gig=gig, address=address, direction=direction, website=website, number=number,
                                     indoor=indoor, covered=covered,
                                     capacity=capacity, credential_collection=credential_collection, dressing_room=dressing_room, hospitality=hospitality, hospitality_detail=hospitality_detail, catring=catring, catring_detail=catring_detail, wather=wather)

        response_data = {
            "user": str(venue.user),
            "gig": str(venue.gig),
            "id": venue.id,
            "address": venue.address,
            "direction": venue.direction,
            "website": venue.website,
            "number": venue.number,
            "indoor": venue.indoor,
            "covered": venue.covered,
            "capacity": venue.capacity,
            "credential_collection": venue.credential_collection,
            "dressing_room": venue.dressing_room,
            "hospitality": venue.hospitality,
            "hospitality_detail": venue.hospitality_detail,
            "catring": venue.catring,
            "catring_detail": venue.catring_detail,
            "wather": venue.wather,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Venue created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class VenueUpdateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = VenueSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        address = request.data["address"]
        direction = request.data["direction"]
        website = request.data["website"]
        number = request.data["number"]
        indoor = request.data["indoor"]
        covered = request.data["covered"]
        capacity = request.data["capacity"]
        wather = request.data["wather"]
        credential_collection = request.data["credential_collection"]
        dressing_room = request.data["dressing_room"]
        hospitality = request.data["hospitality"]
        hospitality_detail = request.data["hospitality_detail"]
        catring = request.data["catring"]
        catring_detail = request.data["catring_detail"]

        id = self.kwargs["pk"]

        if not Venue.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Venue is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        vanue = Venue.objects.get(id=id)
        vanue.user = user
        vanue.gig = gig
        vanue.address = address
        vanue.direction = direction
        vanue.website = website
        vanue.number = number
        vanue.indoor = indoor
        vanue.covered = covered
        vanue.capacity = capacity
        vanue.wather = wather
        vanue.credential_collection = credential_collection
        vanue.dressing_room = dressing_room
        vanue.hospitality = hospitality
        vanue.hospitality_detail = hospitality_detail
        vanue.catring = catring
        vanue.catring_detail = catring_detail
        vanue.save()

        response_data = {
            "id": vanue.id,
            "user": str(vanue.user),
            "gig": str(vanue.gig),
            "address": vanue.address,
            "direction": vanue.direction,
            "website": vanue.website,
            "number": vanue.number,
            "indoor": vanue.indoor,
            "covered": vanue.covered,
            "capacity": vanue.capacity,
            "wather": vanue.wather,
            "credential_collection": vanue.credential_collection,
            "dressing_room": vanue.dressing_room,
            "hospitality": vanue.hospitality,
            "hospitality_detail": vanue.hospitality_detail,
            "catring": vanue.catring,
            "catring_detail": vanue.catring_detail
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Venue Updated",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class VenueListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = VenueListSerializer
    queryset = Venue.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)

class GetallVenueAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = VenueListSerializer
    queryset = Venue.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "All venue list",
                              "data": serializer.data},
                        status=status.HTTP_200_OK)
class VenueDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = VenueSerializer

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not Venue.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Venue is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        venue = Venue.objects.get(id=id)
        venue.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Venue deleted",
                              "result": serializer.data},
                        status=status.HTTP_200_OK)


class HotelCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = HotelSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        hotel_name = request.data["hotel_name"]
        address = request.data["address"]
        direction = request.data["direction"]
        website = request.data["website"]
        number = request.data["number"]
        wifi_paid_for = request.data["wifi_paid_for"]
        room_buyout = request.data["room_buyout"]

        hotel = Hotel.objects.create(user=user, gig=gig, hotel_name=hotel_name, address=address, direction=direction, website=website, number=number,
                                     wifi_paid_for=wifi_paid_for, room_buyout=room_buyout,)

        response_data = {
            "id": hotel.id,
            "user": str(hotel.user),
            "gig": str(hotel.gig),
            "hotel_name": hotel.hotel_name,
            "address": hotel.address,
            "direction": hotel.direction,
            "website": hotel.website,
            "number": hotel.number,
            "wifi_paid_for": hotel.wifi_paid_for,
            "room_buyout": hotel.room_buyout,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Hotel created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class HotelUpdateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = HotelSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        address = request.data["address"]
        direction = request.data["direction"]
        website = request.data["website"]
        number = request.data["number"]
        wifi_paid_for = request.data["wifi_paid_for"]
        room_buyout = request.data["room_buyout"]

        id = self.kwargs["pk"]

        if not Hotel.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Hotel is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

        hotel = Hotel.objects.get(id=id)
        hotel.user = user
        hotel.gig = gig
        hotel.address = address
        hotel.direction = direction
        hotel.website = website
        hotel.number = number
        hotel.wifi_paid_for = wifi_paid_for
        hotel.room_buyout = room_buyout
        hotel.save()

        response_data = {
            "id": hotel.id,
            "user": str(hotel.user),
            "gig": str(hotel.gig),
            "address": hotel.address,
            "direction": hotel.direction,
            "website": hotel.website,
            "number": hotel.number,
            "wifi_paid_for": hotel.wifi_paid_for,
            "room_buyout": hotel.room_buyout,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Hotel Updated",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class HotelListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = HotelListSerializer
    queryset = Hotel.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class HotelDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = HotelSerializer

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not Hotel.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Hotel is not exists"}, status=status.HTTP_400_BAD_REQUEST)
        hotel = Hotel.objects.get(id=id)
        hotel.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Hotel deleted",
                              "result": serializer.data},
                        status=status.HTTP_200_OK)


class ContactCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        type = request.data["type"]
        name = request.data["name"]
        number = request.data["number"]
        email = request.data["email"]
        travelling_party = request.data["travelling_party"]

        contact = Contacts.objects.create(
            user=user, gig=gig, type=type, name=name, number=number, email=email, travelling_party=travelling_party)

        response_data = {
            "id": contact.id,
            "user": str(contact.user),
            "gig": str(contact.gig),
            "type": contact.type,
            "name": contact.name,
            "number": contact.number,
            "email": contact.email,
            "travelling_party": contact.travelling_party,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Contact created",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class ContactUpdateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        type = request.data["type"]
        name = request.data["name"]
        number = request.data["number"]
        email = request.data["email"]
        travelling_party = request.data["travelling_party"]

        id = self.kwargs["pk"]

        if not Contacts.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "contact is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

        contact = Contacts.objects.get(id=id)
        contact.user = user
        contact.gig = gig
        contact.type = type
        contact.name = name
        contact.number = number
        contact.email = email
        contact.travelling_party = travelling_party
        contact.save()

        response_data = {
            "id": contact.id,
            "user": str(contact.user),
            "gig": str(contact.gig),
            "type": contact.type,
            "name": contact.name,
            "number": contact.number,
            "email": contact.email,
            "travelling_party": contact.travelling_party,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Contact Updated",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)


class ContactListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = ContactListSerializer
    queryset = Contacts.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class ContactDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = ContactSerializer

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not Contacts.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Contact is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        contact = Contacts.objects.get(id=id)
        contact.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Contact deleted",
                              "result": serializer.data},
                        status=status.HTTP_200_OK)


class GuestListCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = GuestListSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "error": serializer.errors, },
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        guestlist_detail = request.data["guestlist_detail"]
        guestlist = request.data["guestlist"]
        if GuestList.objects.filter(user=user, gig=gig).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "message": "guestlist is already add", },
                            status=status.HTTP_400_BAD_REQUEST)

        guestl = GuestList.objects.create(
            user=user, gig=gig, guestlist_detail=guestlist_detail, guestlist=guestlist)

        response_data = {
            "id": guestl.id,
            "user": str(guestl.user),
            "gig": str(guestl.gig),
            "guestlist_detail": guestl.guestlist_detail,
            "guestlist": guestl.guestlist,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Guestlist created",
                              "result": {'data': response_data}},
                        status=status.HTTP_200_OK)


class GuestListUpdateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = GuestListSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        guestlist_detail = request.data["guestlist_detail"]
        guestlist = request.data["guestlist"]

        id = self.kwargs["pk"]

        if not GuestList.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
             "message": "Guestlist is not exists".format(id)},status=status.HTTP_400_BAD_REQUEST)
        
        guestl=GuestList.objects.get(id=id)
        guestl.user=user
        guestl.gig=gig
        guestl.guestlist_detail=guestlist_detail
        guestl.guestlist=guestlist
        guestl.save()

        response_data = {
            "id": guestl.id,
            "user": str(guestl.user),
            "gig": str(guestl.gig),
            "guestlist_detail": guestl.guestlist_detail,
            "guestlist": guestl.guestlist,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Guestlist Updated",
                              "results": response_data},
                        status=status.HTTP_200_OK)


class GuestListListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = GuestSerializer
    queryset = GuestList.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class GuestListDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = GuestListSerializer

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not GuestList.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Guestlist is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        guestl = GuestList.objects.get(id=id)
        guestl.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Guestlist deleted",
                              "result": serializer.data},
                        status=status.HTTP_200_OK)


class SetTimeCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = SetTimeSerialiazer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "error": serializer.errors, },
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        venue = Venue.objects.get(id=request.data["venue"])
        depart_time = request.data["depart_time"]
        arrival_time = request.data["arrival_time"]

        settime = SetTime.objects.create(
            user=user, gig=gig, venue=venue, depart_time=depart_time, arrival_time=arrival_time)

        response_data = {
            "id": settime.id,
            "user": str(settime.user),
            "gig": str(settime.gig),
            "venue": str(settime.venue),
            "depart_time": settime.depart_time,
            "arrival_time": settime.arrival_time
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Settime created",
                              "result": {'data': response_data}},
                        status=status.HTTP_200_OK)


class SetTimeUpdateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = SetTimeSerialiazer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        venue = Venue.objects.get(id=request.data["venue"])
        depart_time = request.data["depart_time"]
        arrival_time = request.data["arrival_time"]

        id = self.kwargs["pk"]

        if not SetTime.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
                                  "message": "Settime is not exists"}, status=status.HTTP_400_BAD_REQUEST)

        settime = SetTime.objects.get(id=id)
        settime.user = user
        settime.gig = gig
        settime.venue = venue
        settime.depart_time = depart_time
        settime.arrival_time = arrival_time
        settime.save()

        response_data = {
            "id": settime.id,
            "user": str(settime.user),
            "gig": str(settime.gig),
            "venue": str(settime.venue),
            "depart_time": settime.depart_time,
            "arrival_time": settime.arrival_time,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Settime Updated",
                              "results": response_data},
                        status=status.HTTP_200_OK)


class SetTimeListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = SetTimeListSerializer
    queryset = SetTime.objects.all()

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class SetTimeDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = SetTimeSerialiazer

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not SetTime.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Settime is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        settime = SetTime.objects.get(id=id)
        settime.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Settime deleted",
                              "result": serializer.data},
                        status=status.HTTP_200_OK)


class DocumentCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = DocumentSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        flight = FlightBook.objects.get(id=request.data["flight"])
        type = request.data["type"]
        document = request.FILES.get('document')

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)

        client.put_object(Bucket='Music',
                          Key=user.first_name+'.png',
                          Body=document,
                          ACL='public-read-write',
                          ContentType='image/png',
                          )
        url = client.generate_presigned_url(ClientMethod='get_object',
                                            Params={'Bucket': 'Music',
                                                    'Key': user.first_name+'.png'}, ExpiresIn=300, HttpMethod=None)
        passe = Document.objects.create(
            user=user, gig=gig, flight=flight, type=type, document=url)

        response_data = {
            "id": passe.id,
            "user": str(passe.user),
            "gig": str(passe.gig),
            "flight": str(passe.flight),
            "type": passe.type,
            "document": url
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Document created",
                              "result": {'data': response_data}},
                        status=status.HTTP_200_OK)


class DocumentUpdateAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = DocumentSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        flight = FlightBook.objects.get(id=request.data["flight"])
        type = request.data["type"]
        document = request.FILES.get('document')

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)

        client.put_object(Bucket='Music',
                          Key=user.first_name+'.png',
                          Body=document,
                          ACL='public-read-write',
                          ContentType='image/png',
                          )
        url = client.generate_presigned_url(ClientMethod='get_object',
                                            Params={'Bucket': 'Music',
                                                    'Key': user.first_name+'.png'}, ExpiresIn=300, HttpMethod=None)
        id = self.kwargs["pk"]

        if not Document.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
                                  "message": "Passes is not exists"}, status=status.HTTP_400_BAD_REQUEST)

        passe = Document.objects.get(id=id)
        passe.user = user
        passe.gig = gig
        passe.flight = flight
        passe.type = type
        passe.document = url
        passe.save()

        response_data = {
            "id": passe.id,
            "user": str(passe.user),
            "gig": str(passe.gig),
            "flight": str(passe.flight),
            "type": passe.type,
            "passes": url
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Passes updated",
                              "result": {'data': response_data}},
                        status=status.HTTP_200_OK)


class DocumentListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = DocumentsListSerializer
    queryset = Document.objects.all()

    def get(self, request, *args, **kwargs):

        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class DocumentDeleteAPIView(DestroyAPIView):
    permission_classes = [AllowAny]

    serializer_class = DocumentSerializer

    def delete(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not Document.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Passes is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        passes = Document.objects.get(id=id)
        passes.delete()
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Passes deleted",
                              "result": serializer.data},
                        status=status.HTTP_200_OK)


# class Logout(GenericAPIView):
#     # serializer_class =LogoutSerializer
#     def post(self,request,*args,**keargs):
#         auth = get_authorization_header(request).split()
#         print(auth)
#         auth.pop()
#         # print(auth,"/////////////////////")
#         # .remove(auth)
#         return Response("logout ")


class AllDataAPIView(GenericAPIView):
    permission_classes = [AllowAny]

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
                    "flights": flight_list
                })
            final.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "gigs": gig_list
            })
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
                "type": "flight",
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
                "type": "cab",
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
        # print(response)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Schedule list",
                              "result": final},
                        status=status.HTTP_200_OK)


class allListView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class_UserSerializer = UserListSerializer
    serializer_class_GigsSerializer = ListGigSerializer
    serializer_class_FlightSerializer = FlightSerializer
    serializer_class_CabBookSerializer = CabSerializer
    serializer_class_HotelListSerializer = HotelListSerializer
    serializer_class_VenueListSerializer = VenueListSerializer
    serializer_class_SetTimeSerializer = SetTimeSerialiazer
    serializer_class_ContactSerializer = ContactListSerializer
    serializer_class_GuestListSerializer = GuestSerializer
    serializer_class_DocumentSerializer = DocumentsListSerializer

    def get(self, request, *args, **kwrgs):
        if request.method == 'GET':
            
            users = User.objects.all()
            gigs = Gigs.objects.all()
            flights = FlightBook.objects.all()
            cabs = CabBook.objects.all()
            hotels = Hotel.objects.all()
            venues = Venue.objects.all()
            settimes = SetTime.objects.all()
            contacts = Contacts.objects.all()
            guestlist = GuestList.objects.all()
            documents = Document.objects.all()

            seralizer1 = self.serializer_class_UserSerializer(users, many=True)
            seralizer2 = self.serializer_class_GigsSerializer(gigs, many=True)
            seralizer3 = self.serializer_class_FlightSerializer(
                flights, many=True)
            seralizer4 = self.serializer_class_CabBookSerializer(
                cabs, many=True)
            seralizer5 = self.serializer_class_HotelListSerializer(
                hotels, many=True)
            seralizer6 = self.serializer_class_VenueListSerializer(
                venues, many=True)
            seralizer7 = self.serializer_class_ContactSerializer(
                contacts, many=True)
            serializer8 = self.serializer_class_GuestListSerializer(
                guestlist, many=True)
            serializer9 = self.serializer_class_DocumentSerializer(
                documents, many=True)

            final = []
            users = User.objects.all()

            flights = FlightBook.objects.all()
            cabs = CabBook.objects.all()
            for flight in flights:
                final.append({
                    "type": "flight",
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
                    "type": "cab",
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
                    "type": "settime",
                    "settime_id": settime.id,
                    "user": settime.user.id,
                    "gig": settime.gig.id,
                    "venue": settime.venue.direction,
                    "depart_time": settime.depart_time,
                    "arrival_time": settime.arrival_time
                })
            gig_response = []
            for gig in gigs:
                schedule = FlightBook.objects.filter(gig=gig.id).count(
                ) + CabBook.objects.filter(gig=gig.id).count() + SetTime.objects.filter(gig=gig.id).count()
                contact = Contacts.objects.filter(gig=gig.id).count()
                document = Document.objects.filter(gig=gig.id).count()
                gig_users_list = []
                for user in gig.user.all():
                    gig_users_list.append({
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_manager": user.is_manager
                })
                gig_response.append({
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
                    "user": gig_users_list,
                    "schedule_count": schedule,
                    "contact_count": contact,
                    "document_count": document,
                })
            dates = []
            user_list = []
            f = []
            for i in final:
                dates.append(str(i["depart_time"]))
                user_list.append(str(i["user"]))

            dates = [*set(dates)]

            print(f)
            print(user_list)
            a = {}
            for date in dates:
                f.append({date: []})

            # for date in dates:
            #     for i in final:
            #         if date == str(i["depart_time"]):

            #             print(date, str(i["depart_time"]))
            #             print('--------------')
            print(f, '=============')
            users_list = []
            for user in users:
                users_list.append({
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_manager": user.is_manager
                })
            response = {
                'users': seralizer1.data,
                'gigs': gig_response,
                'hotels': seralizer5.data,
                'venues': seralizer6.data,
                # 'flights':seralizer3.data,
                # 'cabs':seralizer4.data,
                "schedule": final,
                'contacts': seralizer7.data,
                'guestlists': serializer8.data,
                'documents': serializer9.data,
                # 'passeslength': len()

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
                "type": "flight",
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
                    "type": "cab",
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

                return Response(data={"status": status.HTTP_200_OK,
                                      "error": False,
                                      "message": "Schedule list",
                                      "result": final},
                                status=status.HTTP_200_OK)
