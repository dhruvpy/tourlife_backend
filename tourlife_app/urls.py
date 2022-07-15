from django.contrib import admin
from django.urls import path
from tourlife_app import views

urlpatterns = [
     path('create_user', views.CreateUserAPIView.as_view(), name="register"),
     path('login', views.LoginAPIView.as_view(), name="login"),
     # path('person',views.Person.as_view(),name='person'),
     path('gigs_list',views.GigsListAPIView.as_view(),name='gigs_list'),
     path('users_list',views.UserListAPIView.as_view(),name='users_list'),
     # path('schedule_list',views.ScheduleListAPIView.as_view(),name='schedule_list'),
     path('all_data',views.allListView.as_view(),name='all_data'),
     path('all_data2',views.AllDataAPIView.as_view(),name='all_data2'),
     path('schedule_list',views.ScheduleAPIView.as_view(),name='schedule_list'),
    
     path('gigs_create',views.GigsCreateAPIView.as_view(),name='gigs_create'),
]