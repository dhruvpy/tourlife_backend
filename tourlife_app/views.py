# from asyncio.windows_events import NULL
from tempfile import tempdir
from .models import *
from .serializer import *
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
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
from django.template.loader import get_template 
from django.template.loader import render_to_string
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponse
import pdfkit  
import datetime
def get_user_queryset():
    return User.objects.all().exclude(is_delete=True)

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
        last_name = request.POST.get("last_name")
        first_name = request.data["first_name"]
        email = request.data["email"]
        password = request.data["password"]
        mobile_no = request.data["mobile_no"]
        profile_image = request.FILES.get('profile_image')
        is_manager = request.data["is_manager"]
        is_artist = request.data["is_artist"]
        # is_delete = request.data["is_delete"]

        if User.objects.filter(username=username).exists() | User.objects.filter(email=email).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "This email or username is already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(username=username, first_name=first_name,  password=password, email=email, mobile_no=mobile_no,is_manager=is_manager,is_artist=is_artist,is_delete=False)
        print(profile_image,"////////////////////")
        if not last_name==None:
            user.last_name=last_name

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)

        today = datetime.datetime.now()

        today = today.strftime("%Y-%m-%d-%H-%M-%S")

        client.put_object(Bucket='tourlife_test',
                          Key='User/user'+str(user.id)+str(today)+'.png',
                          Body= profile_image,
                          ACL='public-read-write',
                          ContentType='image/png',
                          )

        url = client.generate_presigned_url(ClientMethod='get_object',
                                            Params={'Bucket': 'tourlife_test',
                                                    'Key': 'User/user'+str(user.id)+str(today)+'.png'}, HttpMethod=None)

        url=url.split('?')
        url=url[0]
        user.profile_image=url
        user.save()

        response_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": user.password,
            "email": user.email,
            "mobile_no": str(user.mobile_no),
            "profile_image": str(url),
            "is_artist": user.is_artist,
            "is_manager": user.is_manager,
            "is_delete":user.is_delete
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": 'Add new user',
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
        last_name = request.POST.get("last_name")
        password = request.data["password"]
        email = request.data["email"]
        mobile_no = request.data["mobile_no"]
        profile_image = request.FILES.get('profile_image')
        is_manager = request.data["is_manager"]
        is_artist = request.data["is_artist"]
        id = self.kwargs["pk"]

        if not User.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # if User.objects.filter(username=username).exists() | User.objects.filter(email=email).exists():
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "This email or username is already exists"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        print(profile_image)
        user = User.objects.get(id=id)

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)
        today = datetime.datetime.now()

        today = today.strftime("%Y-%m-%d-%H-%M-%S")

        
        if not user.profile_image== None:
        
            key=user.profile_image.split('test/')
            client.delete_object(Bucket='tourlife_test',
            Key=key[1],
            )

        if not profile_image== None:
            
            client.put_object(Bucket='tourlife_test',
                            Key='User/user'+str(user.id)+str(today)+'.png',
                            Body= profile_image,
                            ACL='public-read-write',
                            ContentType='image/png',
                            )

            url = client.generate_presigned_url(ClientMethod='get_object',
                                                Params={'Bucket': 'tourlife_test',
                                                'Key': 'User/user'+str(user.id)+str(today)+'.png'}, HttpMethod=None)

            url=url.split('?')
            url=url[0]
            user.profile_image = url 
        if not last_name==None:
            user.last_name=last_name
        user.username = username
        user.first_name = first_name
        user.password = password
        user.email = email
        user.mobile_no = mobile_no
        user.is_manager = is_manager
        user.is_artist = is_artist
        user.save()

        response_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": user.password,
            "email": user.email,
            "mobile_no": user.mobile_no,
            "profile_image": str(user.profile_image),
            "is_manager": user.is_manager,
            "is_artist": user.is_artist
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "message": "User updated",
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
    
    queryset = User.objects.all().exclude(email='admin@gmail.com').exclude(is_delete=True)


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
    queryset = User.objects.all().exclude(email='admin@gmail.com').exclude(is_delete=True)


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

class GetUserAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = ListUserSerializers
    # renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        if not User.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        if user.is_delete == True:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        

        
        # queryset = self.get_queryset()
        serializer = self.get_serializer(user)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get gig",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)

class UserDeleteAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = CreateUserSerializers

    def post(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        # is_delete=request.data["is_delete"]
        # print(is_delete,"////////////////////////////")

        id = self.kwargs["pk"]
        if not User.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        # if is_delete==True:
        #     user.delete()
        user.is_delete=True
        user.save()
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)
       
        key=user.profile_image.split('test/')
        client.delete_object(Bucket='tourlife_test',
         Key=key[1],
         )

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

        if user.is_delete == True:
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error': True, 'message': "User not exists"}, status=status.HTTP_400_BAD_REQUEST)


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

        if user.is_delete == True:
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error': True, 'message': "User not exists"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {"email": user.email, "password": user.password}

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Admin User Login Successfully.",
                              "result": {'id': user.id,
                                         'first_name': user.first_name,
                                         'last_name': user.last_name,
                                         'profile_image': user.profile_image,
                                         'token': jwt_token,
                                         'is_manager': user.is_manager}},
                        status=status.HTTP_200_OK)


class ForgotPasswordAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotpasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error': True, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        if not User.objects.filter(email=email).exists():
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'message': "email is not registered", }, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            random_num = random.randint(1000, 9999)
            otp = random_num

            subject = 'send otp'
            message = 'your otp is {}'.format(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            # send_mail(subject, message, email_from, recipient_list)

            Emailotp.objects.create(email=email, otp=otp)

            return Response(data={"Status": status.HTTP_200_OK, "error": False, 'message': 'We have sent you a otp to reset your password', "results": {"email": email, "otp": otp}}, status=status.HTTP_200_OK)


class OTPCheckAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        print(otp)
        email = request.data.get('email')
        print(email)

        if otp is None:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'message': 'please enter otp'}, status=status.HTTP_400_BAD_REQUEST)

        if email is None:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'message': 'please enter email address'}, status=status.HTTP_400_BAD_REQUEST)
        
        emailotp = Emailotp.objects.filter(email=email).last()
        # print(emailotp.otp,"''''''''''''''''''''''''''")
        # print(emailotp.email,"''''''''''''''''''''''''''")


        if not emailotp:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'message': 'please enter valid email'}, status=status.HTTP_400_BAD_REQUEST)

        if not (emailotp.email == email and emailotp.otp == otp):
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'message': 'otp is expire or not valid this mail'}, status=status.HTTP_400_BAD_REQUEST)

        emailotp.otp_check = True
        emailotp.save()
        return Response(data={'status': status.HTTP_200_OK, 'error': False, 'message': 'otp check please set new password'}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'error': True, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        print(email)
        new_password = request.data['new_password']

        user = User.objects.filter(email=email).last()

        if not user:
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST, 'error': True, 'message': 'please enter valid email'}, status=status.HTTP_400_BAD_REQUEST)
        user.password = new_password
        user.save()
        emailotp_obj = Emailotp.objects.filter(email=user.email).last()
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
        print(request.FILES.get("cover_image"),'--------------')
        if not serializer.is_valid():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user_id_list = request.data["user"]
        user_id_list = json.loads(user_id_list)
        user = User.objects.filter(id__in=user_id_list)
        title = request.data["title"]
        descriptions = request.data["descriptions"]
        # profile_pic = request.data["profile_pic"]
        cover_image = request.FILES.get("cover_image")
        location = request.data["location"]
        show = request.data["show"]
        stage = request.data["stage"]
        visa = request.data["visa"]
        Equipment = request.data["Equipment"]
        start_date = request.data["start_date"]
        end_date = request.data["end_date"]
        sound_check_time = request.POST.get("sound_check_time")
        Equipment_email = request.data["Equipment_email"]
        print(sound_check_time,"//////////////")

        gigs = Gigs.objects.create(title=title,
        location=location, visa=visa, Equipment=Equipment, start_date=start_date, end_date=end_date)
        gigs.user.set(user)
      
        if not sound_check_time== None:
            gigs.sound_check_time=sound_check_time
        #     user.sound_check_time=sound_check_time
        if not stage==None:
            gigs.stage=stage
        if not show==None:
            gigs.show=show
        if not descriptions==None:
            gigs.descriptions=descriptions
        if not Equipment_email==None:
            gigs.Equipment_email=Equipment_email
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)
        today = datetime.datetime.now()

        today = today.strftime("%Y-%m-%d-%H-%M-%S")

        print(today,"::")
        
        client.put_object(Bucket='tourlife_test',
                          Key='Gigs/gig'+str(gigs.id)+str(today)+'.png',
                          
                        #   Body=bytes(json.dumps(profile_image).encode()),
                        Body= cover_image,
                        ACL='public-read-write',
                          ContentType='image/png',
                          )

        url = client.generate_presigned_url(ClientMethod='get_object',
                                            Params={'Bucket': 'tourlife_test',
                                                    'Key': 'Gigs/gig'+str(gigs.id)+str(today)+'.png'},  HttpMethod=None)
        
        url=url.split('?')
        url=url[0]
        gigs.cover_image=url
        print(gigs.id,'----------')
        
        gigs.save()

        for i in user:
            GigMaster.objects.create(gig=gigs,user=i)

        response_data = {
            "id": gigs.id,
            "user":  gigs.user.all().values_list('id', flat=True),
            "title": gigs.title,
            "descriptions": gigs.descriptions,
            "cover_image": str(gigs.cover_image),
            "location": gigs.location,
            "show": gigs.show,
            "stage": gigs.stage,
            "visa": gigs.visa,
            "Equipment": gigs.Equipment,
            "start_date" : gigs.start_date,
            "end_date" : gigs.end_date,
            "sound_check_time": gigs.sound_check_time,
            "Equpment_email" : gigs.Equipment_email
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
        user = User.objects.filter(id__in=user_id_list)
        title = request.data["title"]
        descriptions = request.data["descriptions"]
        # profile_pic = request.data["profile_pic"]
        cover_image = request.FILES.get("cover_image")
        location = request.data["location"]
        show = request.data["show"]
        stage = request.data["stage"]
        visa = request.data["visa"]
        Equipment = request.data["Equipment"]
        start_date = request.data["start_date"]
        end_date = request.data["end_date"]
        sound_check_time = request.POST.get("sound_check_time")
        Equipment_email= request.data["Equipment_email"]
        id = self.kwargs["pk"]
        if not Gigs.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gigs is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)


        gigs = Gigs.objects.get(id=id)

        a = GigMaster.objects.filter(gig=gigs)
        a.delete()
        for i in user:
            GigMaster.objects.create(gig=gigs,user=i)
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)
        
        today = datetime.datetime.now()
    
        today = today.strftime("%Y-%m-%d-%H-%M-%S")
        print(gigs.cover_image,"::::::::::::::::::::::::::::")
        if not gigs.cover_image == None:

            key=gigs.cover_image.split('test/')
            client.delete_object(Bucket='tourlife_test',
            Key=key[1],
            )
        if not cover_image == None:
            
            client.put_object(Bucket='tourlife_test',
                            Key='Gigs/gig'+str(gigs.id)+str(today)+'.png',
                            # Body=bytes(json.dumps(cover_image).encode()),
                            Body= cover_image,
                            ACL='public-read-write',
                            ContentType='image/png',
                            )

            url = client.generate_presigned_url(ClientMethod='get_object',
                                                Params={'Bucket': 'tourlife_test',
                                                        'Key': 'Gigs/gig'+str(gigs.id)+str(today)+'.png'}, HttpMethod=None)
            url=url.split('?')
            url=url[0]
            gigs.cover_image = url

        if not sound_check_time==None:
            gigs.sound_check_time=sound_check_time
        if not stage==None:
            gigs.stage=stage
        if not show==None:
            gigs.show=show
        if not descriptions==None:
            gigs.descriptions=descriptions
        if not Equipment_email==None:
            gigs.Equipment_email=Equipment_email

        gigs.title = title
        gigs.location = location
        gigs.visa = visa
        gigs.Equipment = Equipment
        gigs.start_date = start_date
        gigs.end_date = end_date
        # gigs.sound_check_time = sound_check_time
        gigs.user.set(user)
        gigs.save()

        response_data = {
            "id": gigs.id,
            "user": gigs.user.all().values_list('id', flat=True),
            "title": gigs.title,
            "descriptions": gigs.descriptions,
            "cover_image": str(gigs.cover_image),
            "location": gigs.location,
            "show": gigs.show,
            "stage": gigs.stage,
            "visa": gigs.visa,
            "Equipment": gigs.Equipment,
            "start_date" : gigs.start_date,
            "end_date" : gigs.end_date,
            "sound_check_time": gigs.sound_check_time,
            "Equipment_email": gigs.Equipment_email
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
    
    user=get_user_queryset()

    queryset = Gigs.objects.all()
    for x in queryset:
        users=x.user.all()
        check=[i for i in users if i in get_user_queryset()]
        x.user.set(check)

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        # user = User.objects.get(id=id)
        # if user.is_delete == True:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
        #                     status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class GetallGigsAPIView(ListAPIView):
    permission_classes = [AllowAny]
    # renderer_classes = [JSONRenderer]

    serializer_class = ListGigSerializer
    user = get_user_queryset()
    queryset = Gigs.objects.all()
    # queryset=[]
    for x in queryset:

        users=x.user.all()
        check=[i for i in users if i in get_user_queryset()]
        
        x.user.set(check)
    
    def get(self, request, *args, **kwargs):
       
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)

        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "All gigs list",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)


class GetGigsAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = ListGigSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        user= get_user_queryset()
        id = self.kwargs["pk"]
        if not Gigs.objects.filter(id=id,user__in=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gigs is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        gig = Gigs.objects.get(id=id)

        
        serializer = self.get_serializer(gig)
        print(gig.id,"?///////////////////////////")
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get gig",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)


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
        print(gigs,"/////////////////////////////////")
        key=gigs.cover_image.split('test/')
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)
        client.delete_object(Bucket='tourlife_test', Key=key[1])


        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Gigs deleted"},
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
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
        # if not FlightBook.objects.filter(user=user).exists():
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User or gig not exists "},
        #      status=status.HTTP_400_BAD_REQUEST)
        flightbook = FlightBook.objects.create(user=user, gig=gig, depart_location=depart_location, depart_lat_long=depart_lat_long,
                                               depart_time=depart_time, depart_terminal=depart_terminal, depart_gate=depart_gate, arrival_location=arrival_location,
                                               arrival_lat_long=arrival_lat_long, arrival_time=arrival_time, arrival_terminal=arrival_terminal,
                                               airlines=airlines, arrival_gate=arrival_gate, flight_number=flight_number, flight_class=flight_class)
        if not wather==None:
            flightbook.wather=wather
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
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
        if not wather==None:
            flightbook.wather=wather
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
    user=get_user_queryset()
    queryset = FlightBook.objects.filter(user__in=user)

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
    user=get_user_queryset()

    queryset = FlightBook.objects.filter(user__in=user)

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

class GetFlightAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = FlightSerializer

    def get(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        user = User.objects.get(id=id)
        if user.is_delete == True:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        

        user = User.objects.get(id=id)
        # user = User.objects.all()
        id1 = self.kwargs["pk1"]

        if not Gigs.objects.filter(id=id1,user=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gig is not exists or not this user gig"},
                            status=status.HTTP_400_BAD_REQUEST)

        gig = Gigs.objects.get(id=id1,user=user)

        flight= FlightBook.objects.filter(user=user,gig=gig).all()
        print(flight,">><<>><<>>")
        
        # # queryset = self.get_queryset()
        serializer = self.get_serializer(flight,many=True)
        # print(gig.id,"?///////////////////////////")
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get flight",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)
       
      
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
                              "message": "Flightbook deleted"},
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
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
        # w=depart_lat_long.split('-')
        # wather = get_weather_report(w[1])


        cabbook = CabBook.objects.create(user=user, gig=gig, depart_location=depart_location, depart_lat_long=depart_lat_long,
                                         depart_time=depart_time, arrival_location=arrival_location,
                                         arrival_lat_long=arrival_lat_long, arrival_time=arrival_time,
                                         driver_name=driver_name, driver_number=driver_number)
        if not wather==None:
            cabbook.wather=wather
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
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
        if not wather==None:
            cabbook.wather=wather
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
    user=get_user_queryset()

    queryset = CabBook.objects.filter(user__in=user)

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)

class GetCabAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = CabSerializer
    # renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        user = User.objects.get(id=id)
        if user.is_delete == True:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        # user = User.objects.all()
        id1 = self.kwargs["pk1"]
        if not Gigs.objects.filter(id=id1,user=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gig is not exists or not this user gig"},
                            status=status.HTTP_400_BAD_REQUEST)

        gig = Gigs.objects.get(id=id1,user=user)

        cab= CabBook.objects.filter(user=user,gig=gig).all()
        
        serializer = self.get_serializer(cab,many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get cabbook",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)

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
                              "message": "Cabbook deleted"},
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        venue_name = request.data["venue_name"]

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
        hospitality_email = request.data["hospitality_email"]
        catring = request.data["catring"]
        catring_detail = request.data["catring_detail"]
        # if Venue.objects.filter(user=user, gig=gig).exists():
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST,
        #                           "message": "Venue is already add this gig", },
        #                     status=status.HTTP_400_BAD_REQUEST)

        venue = Venue.objects.create(user=user, gig=gig, venue_name=venue_name,address=address, direction=direction, website=website, number=number,
                                     indoor=indoor, covered=covered,   
                                     hospitality=hospitality ,catring=catring, )
        if not dressing_room==None:
            venue.dressing_room=dressing_room
        if not credential_collection==None:
            venue.credential_collection=credential_collection
        if not capacity==None:
            venue.capacity=capacity
        if not hospitality_detail==None:
            venue.hospitality_detail=hospitality_detail
        if not catring_detail==None:
            venue.catring_detail=catring_detail
        if not hospitality_email==None:
            venue.hospitality_email=hospitality_email
        if not wather==None:
            venue.wather=wather
        response_data = {
            "user": str(venue.user),
            "gig": str(venue.gig),
            "id": venue.id,
            "venue_name":venue.venue_name,
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
            "hospitality_email": venue.hospitality_email,
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        venue_name = request.data["venue_name"]
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
        hospitality_email = request.data["hospitality_email"]
        catring = request.data["catring"]
        catring_detail = request.data["catring_detail"]

        id = self.kwargs["pk"]

        if not Venue.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Venue is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        vanue = Venue.objects.get(id=id)
        if not dressing_room==None:
            vanue.dressing_room=dressing_room
        if not credential_collection==None:
            vanue.credential_collection=credential_collection
        if not capacity==None:
            vanue.capacity=capacity
        if not hospitality_detail==None:
            vanue.hospitality_detail=hospitality_detail
        if not catring_detail==None:
            vanue.catring_detail=catring_detail
        if not hospitality_email==None:
            vanue.hospitality_email=hospitality_email
        if not wather==None:
            vanue.wather=wather
        vanue.user = user
        vanue.gig = gig
        vanue.venue_name=venue_name
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
            "venue_name":vanue.venue_name,
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
            "hospitality_email": vanue.hospitality_email,
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
    user=get_user_queryset()

    queryset = Venue.objects.filter(user__in=user)

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
    user=get_user_queryset()

    queryset = Venue.objects.filter(user__in=user)

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

class GetVenueAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = VenueListSerializer
    # renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        user = User.objects.get(id=id)
        if user.is_delete == True:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        # user = User.objects.all()
        id1 = self.kwargs["pk1"]
        if not Gigs.objects.filter(id=id1,user=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gig is not exists or not this user gig"},
                            status=status.HTTP_400_BAD_REQUEST)

        gig = Gigs.objects.get(id=id1,user=user)

        venue= Venue.objects.filter(user=user,gig=gig).all()
        
        # # queryset = self.get_queryset()
        serializer = self.get_serializer(venue,many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get venue",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)
        # context={
        #     "venue_list": venue}
        # html = get_template("venue.html").render(context)
       
        # html=render_to_string('venue.html', context)
       

        # pdf= pdfkit.from_string(html)
        
        # return HttpResponse(pdf, content_type='application/pdf')
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
                              "message": "Venue deleted"},
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

        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        hotel_name = request.data["hotel_name"]
        address = request.data["address"]
        direction = request.data["direction"]
        website = request.data["website"]
        number = request.data["number"]
        room_buyout = request.data["room_buyout"]
        # if Hotel.objects.filter(user=user, gig=gig).exists():
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST,
        #                           "message": "hotel is already add this user and gig", },
        #                     status=status.HTTP_400_BAD_REQUEST)

        hotel = Hotel.objects.create(user=user, gig=gig, hotel_name=hotel_name, address=address, direction=direction, website=website, number=number,
                                      room_buyout=room_buyout,)

        response_data = {
            "id": hotel.id,
            "user": str(hotel.user),
            "gig": str(hotel.gig),
            "hotel_name": hotel.hotel_name,
            "address": hotel.address,
            "direction": hotel.direction,
            "website": hotel.website,
            "number": hotel.number,
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        address = request.data["address"]
        hotel_name = request.data["hotel_name"]
        direction = request.data["direction"]
        website = request.data["website"]
        number = request.data["number"]
        room_buyout = request.data["room_buyout"]

        id = self.kwargs["pk"]

        if not Hotel.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Hotel is not exists".format(id)}, status=status.HTTP_400_BAD_REQUEST)

        hotel = Hotel.objects.get(id=id)
        hotel.user = user
        hotel.gig = gig
        hotel.hotel_name = hotel_name
        hotel.address = address
        hotel.direction = direction
        hotel.website = website
        hotel.number = number
        hotel.room_buyout = room_buyout
        hotel.save()

        response_data = {
            "id": hotel.id,
            "user": str(hotel.user),
            "gig": str(hotel.gig),
            "hotel_name": hotel.hotel_name,
            "address": hotel.address,
            "direction": hotel.direction,
            "website": hotel.website,
            "number": hotel.number,
            "room_buyout": hotel.room_buyout,
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "Hotel Updated",
                              "results": {'data': response_data}},
                        status=status.HTTP_200_OK)
# from xhtml2pdf import pisa

class HotelListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = HotelListSerializer
    user=get_user_queryset()

    queryset = Hotel.objects.filter(user__in=user)

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)

class GetHotelAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = HotelListSerializer
    # renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        user = User.objects.get(id=id)
        if user.is_delete == True:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        # user = User.objects.all()
        id1 = self.kwargs["pk1"]
        if not Gigs.objects.filter(id=id1,user=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gig is not exists or not this user gig"},
                            status=status.HTTP_400_BAD_REQUEST)

        gig = Gigs.objects.get(id=id1,user=user)

        hotel= Hotel.objects.filter(user=user,gig=gig).all()
        
        # # queryset = self.get_queryset()
        serializer = self.get_serializer(hotel,many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get hotel",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)

# def hotel_render_pdf_view(request, *args, **kwargs):
#     # id = self.kwargs["pk"]
#     id = kwargs.get('pk')

#     if not Hotel.objects.filter(id=id).exists():
#         return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Hotel is not exists"},
#                         status=status.HTTP_400_BAD_REQUEST)
#     hotel = Hotel.objects.get(id=id)

#     template_path = 'hotel.html'
#     context = {'hotel_list': hotel}
#     response = HttpResponse(content_type='application/pdf')


#     response['Content-Disposition'] = 'filename="report.pdf"'

#     template = get_template(template_path)
#     html = template.render(context)

#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response
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
                              "message": "Hotel deleted"},
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

        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
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

        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
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
    user=get_user_queryset()

    queryset = Contacts.objects.filter(user__in=user)

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)

class GetContactsAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = ContactListSerializer
    # renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        user = User.objects.get(id=id)
        if user.is_delete == True:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        # user = User.objects.all()
        id1 = self.kwargs["pk1"]
        if not Gigs.objects.filter(id=id1,user=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gig is not exists or not this user gig"},
                            status=status.HTTP_400_BAD_REQUEST)

        gig = Gigs.objects.get(id=id1,user=user)

        contact= Contacts.objects.filter(user=user,gig=gig).all()
        
        # # queryset = self.get_queryset()
        serializer = self.get_serializer(contact,many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get contact",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)

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
                              "message": "Contact deleted"},
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        guestlist_detail = request.data["guestlist_detail"]
        guestlist = request.data["guestlist"]
        name = request.data["name"]
        email = request.data["email"]
        contact_no = request.data["contact_no"]

        if GuestList.objects.filter(user=user, gig=gig).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST,
                                  "message": "guestlist is already add", },
                            status=status.HTTP_400_BAD_REQUEST)

        guestl = GuestList.objects.create(
            user=user, gig=gig, guestlist_detail=guestlist_detail, guestlist=guestlist,name=name,email=email,contact_no=contact_no)

        response_data = {
            "id": guestl.id,
            "user": str(guestl.user),
            "gig": str(guestl.gig),
            "guestlist_detail": guestl.guestlist_detail,
            "guestlist": guestl.guestlist,
            "name": guestl.name,
            "email": guestl.email,
            "contact_no": guestl.contact_no
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        guestlist_detail = request.data["guestlist_detail"]
        guestlist = request.data["guestlist"]
        name = request.data["name"]
        email = request.data["email"]
        contact_no = request.data["contact_no"]

        id = self.kwargs["pk"]

        if not GuestList.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
             "message": "Guestlist is not exists".format(id)},status=status.HTTP_400_BAD_REQUEST)
        
        guestl=GuestList.objects.get(id=id)
        guestl.user=user
        guestl.gig=gig
        guestl.guestlist_detail=guestlist_detail
        guestl.guestlist=guestlist
        guestl.name=name
        guestl.email=email
        guestl.contact_no=contact_no
        guestl.save()

        response_data = {
            "id": guestl.id,
            "user": str(guestl.user),
            "gig": str(guestl.gig),
            "guestlist_detail": guestl.guestlist_detail,
            "guestlist": guestl.guestlist,
            "name": guestl.name,
            "email": guestl.email,
            "contact_no": guestl.contact_no
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
    user=get_user_queryset()

    queryset = GuestList.objects.filter(user__in=user)

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)

class GetGuestlistAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = GuestSerializer
    # renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        user = User.objects.get(id=id)
        if user.is_delete == True:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        # user = User.objects.all()
        id1 = self.kwargs["pk1"]
        if not Gigs.objects.filter(id=id1,user=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gig is not exists or not this user gig"},
                            status=status.HTTP_400_BAD_REQUEST)

        gig = Gigs.objects.get(id=id1,user=user)

        guest= GuestList.objects.filter(user=user,gig=gig).all()
        
        # # queryset = self.get_queryset()
        serializer = self.get_serializer(guest,many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get guestlist",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)
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
                              "message": "Guestlist deleted"},
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not Venue.objects.filter(id=request.data["venue"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Venue not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        # user_id_list = request.data["user"]
        # user_id_list = json.loads(user_id_list)
        # user = User.objects.filter(id__in=user_id_list)
        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        venue = Venue.objects.get(id=request.data["venue"])
        depart_time = request.data["depart_time"]
        arrival_time = request.data["arrival_time"]
        add = request.data["add"]
        add = json.loads(add)

        settime = SetTime.objects.create(
            user=user, gig=gig, venue=venue, depart_time=depart_time, arrival_time=arrival_time,add=add)

        response_data = {
            "id": settime.id,
            "user": str(settime.user),
            "gig": str(settime.gig),
            "venue": str(settime.venue),
            "depart_time": settime.depart_time,
            "arrival_time": settime.arrival_time,
            "add": settime.add
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not Venue.objects.filter(id=request.data["venue"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Venue not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        venue = Venue.objects.get(id=request.data["venue"])
        depart_time = request.data["depart_time"]
        arrival_time = request.data["arrival_time"]
        add = request.data["add"]
        add = json.loads(add)

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
        settime.add=add
        settime.save()

        response_data = {
            "id": settime.id,
            "user": str(settime.user),
            "gig": str(settime.gig),
            "venue": str(settime.venue),
            "depart_time": settime.depart_time,
            "arrival_time": settime.arrival_time,
            "add": settime.add
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
    user=get_user_queryset()

    queryset = SetTime.objects.filter(user__in=user)

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)

class GetAllSettimeAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = SetTimeListSerializer
    user=get_user_queryset()

    queryset = SetTime.objects.filter(user__in=user)

    def get(self, request, *args, **kwargs):
        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "All settime list",
                              "data": serializer.data},
                        status=status.HTTP_200_OK)

class GetSettimeAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = SetTimeListSerializer
    # renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        user = User.objects.get(id=id)
        if user.is_delete == True:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        # user = User.objects.all()
        id1 = self.kwargs["pk1"]
        if not Gigs.objects.filter(id=id1,user=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gig is not exists or not this user gig"},
                            status=status.HTTP_400_BAD_REQUEST)

        gig = Gigs.objects.get(id=id1,user=user)

        settime= SetTime.objects.filter(user=user,gig=gig).all()
        
        # # queryset = self.get_queryset()
        serializer = self.get_serializer(settime,many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get settime",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)

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
                              "message": "Settime deleted"},
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not FlightBook.objects.filter(id=request.data["flight"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Flight not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=request.data["user"])
        gig = Gigs.objects.get(id=request.data["gig"])
        flight = FlightBook.objects.get(id=request.data["flight"])
        type = request.data["type"]
        document = request.FILES.get("document")

        # document = request.FILES.get('document')
        passes = Document.objects.create(
            user=user, gig=gig, flight=flight, type=type)

        today = datetime.datetime.now()

        today = today.strftime("%Y-%m-%d-%H-%M-%S")

        

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)
        # client.upload_file(document, 'tourlife_test', 'Documents/doc'+str(passes.id)+'.pdf')
        client.put_object(
            Bucket= 'tourlife_test',
            ACL='public-read-write',
            Body=document,
            Key='Documents/doc'+str(passes.id)+str(today)+'.pdf',
        )
        
        url = client.generate_presigned_url(ClientMethod='get_object',
                                            Params={'Bucket': 'tourlife_test',
                                                    'Key': 'Documents/doc'+str(passes.id)+str(today)+'.pdf'}, HttpMethod=None)
        url=url.split('?')
        url=url[0]
        passes.document= url
        passes.save()
        response_data = {
            "id": passes.id,
            "user": str(passes.user),
            "gig": str(passes.gig),
            "flight": str(passes.flight),
            "type": passes.type,
            "document": str(url)
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
        if not User.objects.filter(id=request.data["user"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Gigs.objects.filter(id=request.data["gig"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Gig not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not FlightBook.objects.filter(id=request.data["flight"]):
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Flight not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        id = self.kwargs["pk"]
        
        if not Document.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True,
                                  "message": "Passes is not exists"}, status=status.HTTP_400_BAD_REQUEST)

        passes = Document.objects.get(id=id)

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

        today = datetime.datetime.now()

        today = today.strftime("%Y-%m-%d-%H-%M-%S")
        if not passes.document == None:
            key=passes.document.split('test/')
            client.delete_object(Bucket='tourlife_test',
            Key=key[1],
            )
        if not document==None:
            client.put_object(
            Bucket= 'tourlife_test',
            ACL='public-read-write',
            Body=document,
            Key='Documents/doc'+str(passes.id)+str(today)+'.pdf',
        )
            url = client.generate_presigned_url(ClientMethod='get_object',
                                                Params={'Bucket': 'tourlife_test',
                                                        'Key': 'Documents/doc'+str(passes.id)+str(today)+'.pdf'}, HttpMethod=None)
            url=url.split('?')
            url=url[0]
            passes.document = url
        passes.user = user
        passes.gig = gig
        passes.flight = flight
        passes.type = type
        passes.save()

        response_data = {
            "id": passes.id,
            "user": str(passes.user),
            "gig": str(passes.gig),
            "flight": str(passes.flight),
            "type": passes.type,
            "document":str(passes.document)
        }
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "document updated",
                              "result": {'data': response_data}},
                        status=status.HTTP_200_OK)


class DocumentListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    serializer_class = DocumentsListSerializer
    user=get_user_queryset()

    queryset = Document.objects.filter(user__in=user)

    def get(self, request, *args, **kwargs):

        # if not request.user.is_manager:
        #     return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "User not allowed"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)


class GetDocumentAPIView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = DocumentsListSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        user = User.objects.get(id=id)
        if user.is_delete == True:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        # user = User.objects.all()
        id1 = self.kwargs["pk1"]
        if not Gigs.objects.filter(id=id1,user=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gig is not exists or not this user gig"},
                            status=status.HTTP_400_BAD_REQUEST)

        gig = Gigs.objects.get(id=id1,user=user)

        document= Document.objects.filter(user=user,gig=gig).all()
        
        # # queryset = self.get_queryset()
        serializer = self.get_serializer(document,many=True)
        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "get document",
                              "data": serializer.data},
                        status=status.HTTP_200_OK,)

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
        today = datetime.datetime.now()

        today = today.strftime("%Y-%m-%d-%H-%M-%S")
        print(passes.document,"::::::::::::::::::::::::::::::::::::")
        key=passes.document.split('test/')
        print(key)
        
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://notificationimages.fra1.digitaloceanspaces.com',
                                aws_access_key_id='GWA6S3ACCBWG66EWNHW3',
                                aws_secret_access_key='jLOt2aNGIZFuDjAP37Q54sJnt+x7lK7FhvkGcrHvftU',)
       
        client.delete_object(Bucket='tourlife_test',
         Key=key[1],
         )

        return Response(data={"status": status.HTTP_200_OK,
                              "error": False,
                              "message": "document deleted"},
                        status=status.HTTP_200_OK)




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
            
            users = User.objects.all().exclude(email='admin@gmail.com').exclude(is_delete=True)
            # gigs = Gigs.objects.filter(start_date__gte = datetime.datetime.now())
            gigs = Gigs.objects.all()
            # gig_master = GigMaster.objects.filter(gig__start_date__gte = datetime.datetime.now())
            gig_master = GigMaster.objects.all()
            flights = FlightBook.objects.all()
            cabs = CabBook.objects.all()
            hotels = Hotel.objects.all()
            venues = Venue.objects.all()
            # settimes = SetTime.objects.filter(gig__start_date__gte = datetime.datetime.now())
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
            users = User.objects.all().exclude(email='admin@gmail.com').exclude(is_delete=True)

            # flights = FlightBook.objects.filter(gig__start_date__gte = datetime.datetime.now())
            # cabs = CabBook.objects.filter(gig__start_date__gte = datetime.datetime.now())
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
            for gig in gig_master:
                schedule = FlightBook.objects.filter(gig=gig.gig.id).count(
                ) + CabBook.objects.filter(gig=gig.gig.id).count() + SetTime.objects.filter(gig=gig.gig.id).count()
                contact = Contacts.objects.filter(gig=gig.gig.id).count()
                document = Document.objects.filter(gig=gig.gig.id).count()
                gig_users_list = []
                for user in gig.gig.user.all():
                    gig_users_list.append({
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_manager": user.is_manager
                })
                gig_response.append({
                    "id": int(gig.gig.id),
                    "title": gig.gig.title,
                    "description": gig.gig.descriptions,
                    "profile_pic": gig.user.profile_image,
                    "cover_image": gig.gig.cover_image,
                    "location": gig.gig.location,
                    "show": gig.gig.show,
                    "stage": gig.gig.stage,
                    "visa": gig.gig.visa,
                    "Equipment": gig.gig.Equipment,
                    "start_date": gig.gig.start_date,
                    "end_date": gig.gig.end_date,
                    "sound_check_time": gig.gig.sound_check_time,
                    "user": int(gig.user.id),
                    "schedule_count": schedule,
                    "contact_count": contact,
                    "document_count": document,
                    "equipment_email": gig.gig.Equipment_email,
                })
            dates = []
            user_list = []
            f = []
            for i in final:
                dates.append(str(i["depart_time"]))
                user_list.append(str(i["user"]))

            dates = [*set(dates)]

            a = {}
            for date in dates:
                f.append({date: []})

            # for date in dates:
            #     for i in final:
            #         if date == str(i["depart_time"]):

            #             print(date, str(i["depart_time"]))
            #             print('--------------')
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
                'weather': get_weather_report("surat")

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


# from django.http import HttpResponse
# from django.views.generic import View

# from tourlife_app.utils import render_to_pdf #created in step 4

# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         data = {
#              'name': 'nensi', 
#              'amount': 39.99,
#             'customer_name': 'Cooper Mann',
#             'order_id': 1233434,
#         }
#         pdf = render_to_pdf('pdf/datatable.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')
from itertools import chain
# from fpdf import FPDF,HTMLMixin
import html
from fpdf import FPDF, HTMLMixin
from unittest import result
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from xhtml2pdf import pisa 
import io as StringIO 
from django.template.loader import get_template 
from django.template import Context 
# def html_to_pdf_directly(template_source, context_dict={}): 
#     template_path = template_source
#     context = context_dict
#     template = get_template(template_path)
#     html = template.render(context) 
#     result = StringIO.StringIO() 
#     pdf = pisa.pisaDocument(StringIO.StringIO(html), dest=result) 
#     if not pdf.err: 
#         return HttpResponse(result.getvalue(), content_type='application/pdf') 
#     else: return HttpResponse('Errors')


def xhtml2pdf(template_source, context_dict={}):
    template_path = template_source
    context = context_dict
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




    # template = get_template(template_source)
    # html = template.render(context_dict)
    # result = BytesIO()
    # pdf= pisa.pisaDocument(BytesIO(html.encode("cp1252")),result)
    # if not pdf.err():
    #     return HttpResponse(result.getvalue(),context_type="application/pdf")
    # return None

class alllistApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class_UserSerializer = UserListSerializer

    def get(self,request,*args,**kwargs):
        context={}
        id = self.kwargs["pk"]
        if not User.objects.filter(id=id).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "user is not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        # user = User.objects.all()
        id1 = self.kwargs["pk1"]
        if not Gigs.objects.filter(id=id1,user=user).exists():
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "gig is not exists or not this user gig"},
                            status=status.HTTP_400_BAD_REQUEST)

        gig = Gigs.objects.get(id=id1,user=user)
        gigs= Gigs.objects.get(id=id1)
        # p=gigs.User.filter(user=gigs)
        users =gigs.user.all().values_list('id', flat=True)
        print(gigs.user.all().values_list('username', flat=True),"????????????????????????????????")

        allgigs = Gigs.objects.all()
        a=list(allgigs).index(gig)
        x= len(allgigs)-1
        
        nextgig=None
        pregig=None
        if not a==x:
            nextgig=allgigs[a+1]
            print(allgigs[a+1],":;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
        if not a==0:
            pregig=allgigs[a-1]

            print(allgigs[a-1],":;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")


        # print(x,"////><><><><><><><><>")
    
        
        
        if gig.Equipment==True:
            gig.Equipment='Confirmed'
        else:
            gig.Equipment='Unconfirmed'
        a=0
        if CabBook.objects.filter(user=user,gig=gig).exists():
            # cab = CabBook.objects.filter(user__in=users,gig=gig).all()
            cab = CabBook.objects.filter(user=user,gig=gig).all()
        else:
            print('-=-=-=-=-=-=-=-=-=-=-=-=')
            cab=None

        if FlightBook.objects.filter(user=user,gig=gig).exists():
            flight = FlightBook.objects.filter(user=user,gig=gig).all()
        else:
            flight=None
        if SetTime.objects.filter(user=user,gig=gig).exists():
            settime = SetTime.objects.filter(user=user,gig=gig).all()
        else:
            settime=None 
        # for x, y in map(flight, cab, settime):
        #     print(x,y,"????????????>>><<<<<<>>>>>>>>")
        # import numpy as np
        # con = np.concatenate((cab, flight))
        # all = np.concatenate((con,settime))
        # all = np.concatenate([cab,flight,settime])
        # all.sorted("depart_time")

        all=[]
        if not cab==None:
            all.extend(cab)
        if not flight==None:
            all.extend(flight)
        if not settime==None:
            all.extend(settime)
        print(all,"?>?>?>?>?>?>")
        if all==[]:
            all=None 
        # all=None
        # if not(cab==None or flight==None or settime==None):
        #     all = sorted(chain( cab, flight,settime), key=lambda obj: obj.depart_time)
        print(all,":::::::::::::::::::::::::::::::::")
        if Venue.objects.filter(user=user,gig=gig).exists():
            venue = Venue.objects.filter(user=user,gig=gig).all()
            print(venue,"]]]]]]]]]]]]]]]]]]]")
            for ven in venue:
                if ven.indoor==True:
                    ven.indoor='Yes'
                else:
                    ven.indoor='No'
                if ven.covered==True:
                    ven.covered='Yes'
                else:
                    ven.covered='No'
                if ven.hospitality==True:
                    ven.hospitality='Confirmed'
                else:
                    ven.hospitality='Unconfirmed'
                if ven.catring==True:
                    ven.catring='Confirmed'
                else:
                    ven.catring='Unconfirmed'
        
        else:
            venue=None 

        if Hotel.objects.filter(user=user,gig=gig).exists():
            hotel = Hotel.objects.filter(user=user,gig=gig).all()
        else:
            hotel=None
        cont=[]
        if Contacts.objects.filter(user__in=users,gig=gig).exists():
            contact = Contacts.objects.filter(user=user,gig=gig).all()
            
            for con in contact:
                cont.append(con.travelling_party)
            print(cont,"??????????>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        else:
            contact=None
            

        # if GuestList.objects.filter(user__in=users,gig=gig).exists():
        #     guestlist = GuestList.objects.filter(user__in=users,gig=gig).all()
        #     print(guestlist,".......................")
        #     for guest in guestlist:
        #         if guest.guestlist==True:
        #                 guest.guestlist='Confirmed'
        #         else:
        #             guest.guestlist='Unconfirmed'
        # else:
        #     guestlist=None

        # if Document.objects.filter(user__in=users,gig=gig).exists():
        #     document = Document.objects.filter(user__in=users,gig=gig).all()
        #     print(document,"///////////////////////////////////////////////////////////////////////////")
        # else:
        #     document=None
        

        print(contact,"////////////////////////////////")
        context={
            "gig_list": gig,
            "cab_list": cab,
            "flight_list":flight,
            "venue_list":venue,
            "hotel_list":hotel,
            "settime_list":settime,
            "contact_list":contact,
            # "guest_list":guestlist,
            # "document_list":document,
            "user":user,
            "pregig":pregig,
            "nextgig":nextgig,
            "users":users,
            "all":all,
            "cont":cont,
           
            }
        options = {
        'page-size': 'Letter',
        'margin-top': '0.5in',
        'margin-right': '0.75in',
        'margin-bottom': '0.5in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'footer-left': "This is a footer",
        'footer-line':'',
        'footer-font-size':'7',
        'footer-right': '[page] of [topage]',

        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None,
    }
       

        # html.unescape(test)
        # html.escape(test)
        # print(test,"html")
        # class MyFPDF(FPDF, HTMLMixin):
        #         pass

        # pdf = MyFPDF()
        #First page
        # pdf.add_page()
        # html = render_to_string('a.html', context)

        # pdf.write_html(test, options=options)
        # pdf.output('html.pdf')
        
        # config = pdfkit.configuration(wkhtmltopdf=r"C:\Users\nensi\Pictures\wkhtmltopdf")
       
        pdf = xhtml2pdf("all_list.html", context)
        print(pdf,"pdf")

        
        # html = render_to_string('all.html', context)
        # pdf = pdfkit.from_string(html,options=options, configuration=config)
        # print(pdf,"pdf")
        # return HttpResponse(pdf, content_type='application/pdf')
        # return render(request,"all.html", context=context)
        return HttpResponse(pdf, content_type='application/pdf')


        return Response(data={"status": status.HTTP_200_OK,
                                      "error": False,
                                      "message": "Schedule list",
                                      "result": pdf},
                                status=status.HTTP_200_OK)

import requests

def get_weather_report(city):
    weather_key="79de5817a4d223b536ce61a0f630a4b4"
    url='https://api.openweathermap.org/data/2.5/weather'
    params={'appid':weather_key, 'q':city, 'units':'Metric'}
    response=requests.get(url,params=params)
    report=response.json()
    city_name= report['name']
    weather_condition= report['weather'][0]['description']
    temp= report['main']['temp']
    output= 'City: %s \nCondition: %s \nTemperature(°C): %s' %(city_name,weather_condition,temp)
    print(output)
    weather_dict = {
        'city_name': report['name'],
        'weather_condition': report['weather'][0]['description'],
        'temp': report['main']['temp']
    }
    return weather_dict
    
        
class FlightDelayApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = FlightDelaySerializer
    
    def post(self, request, *args, **kwargs):
        try:
            flightno = request.POST.get("flightno")
            if flightno == None:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Please enter flightno"},
                                status=status.HTTP_400_BAD_REQUEST)
            today = datetime.datetime.now()
        
            today_year = today.strftime("%Y")
            today_month = today.strftime("%m")
            today_day = today.strftime("%d")

            print(flightno,"today")
            params={"airlinecode":flightno[:2], "airplanecode":flightno[2:],"year":2022, "month":12, "day":16}
            url="https://api.flightapi.io/flighttrack/639c107849594391ceba156a?"
            # url1=url.append(params)
            # url1 = f'{url}airlinecode={flightno[:2]}&airplanecode={flightno[2:]}&year={today_year}&month={today_month}&day={today_day}'
            # print(url1,"url")
            print(params,"params")
            res=requests.get(url, params=params)
            # res= requests.get(url1)
            return Response(res.json())
        
        except:
            return Response(data={"status": status.HTTP_400_BAD_REQUEST, "error": True, "message": "Please enter valid flightno"},
                                status=status.HTTP_400_BAD_REQUEST)
        

        
# print(report)
# show_weather_report(report)

