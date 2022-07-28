from django.contrib import admin
from django.urls import path
from tourlife_app import views

urlpatterns = [
     path('admin_login', views.AdminLoginAPIView.as_view(), name="admin_login"),
     path('login', views.LoginAPIView.as_view(), name="login"),

     path('user_create', views.UserCreateAPIView.as_view(), name="register"),
     path('user_update/<int:pk>', views.UserUpdateAPIView.as_view(), name="update_user"),
     path('user_list', views.UserListAPIView.as_view(), name="list_user"),
     path('user_delete/<int:pk>', views.UserDeleteAPIView.as_view(), name="delete_user"),
     path('all_user', views.GetAllUserAPIView.as_view(), name="all_user"),
     

     path('gigs_create',views.GigsCreateAPIView.as_view(),name='gigs_create'),
     path('gigs_list',views.GigsListAPIView.as_view(),name='gigs_list'),
     path('gigs_update/<int:pk>',views.GigsUpdateAPIView.as_view(),name='gigs_update'),
     path('gigs_delete/<int:pk>',views.GigsDeleteAPIView.as_view(),name='gigs_delete'),
     path('all_gigs',views.GetallGigsAPIView.as_view(),name='all_gigs'),
     

     path('flightbook_create',views.FlightBookCreateAPIView.as_view(),name='flightbook_create'),
     path('flightbook_update/<int:pk>',views.FlightBookUpdateAPIView.as_view(),name='flightbook_update'),
     path('flightbook_list',views.FlightBookListAPIView.as_view(),name='flightbook_list'),
     path('flightbook_delete/<int:pk>',views.FlightBookDeleteAPIView.as_view(),name='flightbook_delete'),
     path('all_flight',views.GetallFlightAPIView.as_view(),name='all_flight'),
     
     
     path('cabbook_create',views.CabBookCreateAPIView.as_view(),name='cabbook_create'),
     path('cabbook_update/<int:pk>',views.CabBookUpdateAPIView.as_view(),name='cabbook_update'),
     path('cabbook_list',views.CabBookListAPIView.as_view(),name='cabbook_list'),
     path('cabbook_delete/<int:pk>',views.CabBookDeleteAPIView.as_view(),name='cabbook_delete'),
     
     path('venue_create',views.VenueCreateAPIView.as_view(),name='venue_create'),
     path('venue_update/<int:pk>',views.VenueUpdateAPIView.as_view(),name='venue_update'),
     path('venue_list',views.VenueListAPIView.as_view(),name='venue_list'),
     path('venue_delete/<int:pk>',views.VenueDeleteAPIView.as_view(),name='venue_delete'),
     path('all_venue',views.GetallVenueAPIView.as_view(),name='all_venue'),
     

     path('hotel_create',views.HotelCreateAPIView.as_view(),name='hotel_create'),
     path('hotel_update/<int:pk>',views.HotelUpdateAPIView.as_view(),name='hotel_update'),
     path('hotel_list',views.HotelListAPIView.as_view(),name='hotel_list'),
     path('hotel_delete/<int:pk>',views.HotelDeleteAPIView.as_view(),name='hotel_delete'),
 
     path('contact_create',views.ContactCreateAPIView.as_view(),name='contact_create'),
     path('contact_update/<int:pk>',views.ContactUpdateAPIView.as_view(),name='contact_update'),
     path('contact_list',views.ContactListAPIView.as_view(),name='contact_list'),
     path('contact_delete/<int:pk>',views.ContactDeleteAPIView.as_view(),name='contact_delete'),
 

     path('guestlist_create',views.GuestListCreateAPIView.as_view(),name='guestlist_create'),
     path('guestlist_update/<int:pk>',views.GuestListUpdateAPIView.as_view(),name='guestlist_update'),
     path('guestlist_list',views.GuestListListAPIView.as_view(), name="guestlist_list"),
     path('guestlist_delete/<int:pk>',views.GuestListDeleteAPIView.as_view(),name='guestlist_delete'),
     
     path('settime_create',views.SetTimeCreateAPIView.as_view(),name='settime_create'),
     path('settime_update/<int:pk>',views.SetTimeUpdateAPIView.as_view(),name='settime_update'),
     path('settime_list',views.SetTimeListAPIView.as_view(), name="settime_list"),
     path('settime_delete/<int:pk>',views.SetTimeDeleteAPIView.as_view(),name='settime_delete'),

     path('document_create',views.DocumentCreateAPIView.as_view(),name='document_create'),
     path('document_update/<int:pk>',views.DocumentUpdateAPIView.as_view(),name='document_update'),
     path('document_list',views.DocumentListAPIView.as_view(), name="document_list"),
     path('document_delete/<int:pk>',views.DocumentDeleteAPIView.as_view(),name='document_delete'),


     path('forgot_password',views.ForgotPasswordAPIView.as_view(),name='forgot_password'),
     path('otpcheck',views.OTPCheckAPIView.as_view(),name='otpcheck'),
     path('set_new_password',views.SetNewPasswordAPIView.as_view(),name='set_new_password'),
     
     
     path('all_data',views.allListView.as_view(),name='all_data'),
     path('all_data2',views.AllDataAPIView.as_view(),name='all_data2'),
    
]