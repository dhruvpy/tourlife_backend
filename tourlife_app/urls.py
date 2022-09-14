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
     path('get_user/<int:pk>', views.GetUserAPIView.as_view(), name="get_user"),
     

     path('gigs_create',views.GigsCreateAPIView.as_view(),name='gigs_create'),
     path('gigs_list',views.GigsListAPIView.as_view(),name='gigs_list'),
     path('gigs_update/<int:pk>',views.GigsUpdateAPIView.as_view(),name='gigs_update'),
     path('gigs_delete/<int:pk>',views.GigsDeleteAPIView.as_view(),name='gigs_delete'),
     path('all_gigs',views.GetallGigsAPIView.as_view(),name='all_gigs'),
     path('get_gigs/<int:pk>',views.GetGigsAPIView.as_view(),name='get_gigs'),
     # path('all',views.allGigsAPIView.as_view(),name='all'),
     

     path('flightbook_create',views.FlightBookCreateAPIView.as_view(),name='flightbook_create'),
     path('flightbook_update/<int:pk>',views.FlightBookUpdateAPIView.as_view(),name='flightbook_update'),
     path('flightbook_list',views.FlightBookListAPIView.as_view(),name='flightbook_list'),
     path('flightbook_delete/<int:pk>',views.FlightBookDeleteAPIView.as_view(),name='flightbook_delete'),
     path('all_flight',views.GetallFlightAPIView.as_view(),name='all_flight'), 
     path('get_flight/<int:pk>/<int:pk1>',views.GetFlightAPIView.as_view(),name='get_flight'),
     
     
     path('cabbook_create',views.CabBookCreateAPIView.as_view(),name='cabbook_create'),
     path('cabbook_update/<int:pk>',views.CabBookUpdateAPIView.as_view(),name='cabbook_update'),
     path('cabbook_list',views.CabBookListAPIView.as_view(),name='cabbook_list'),
     path('cabbook_delete/<int:pk>',views.CabBookDeleteAPIView.as_view(),name='cabbook_delete'),
     path('get_cab/<int:pk>/<int:pk1>',views.GetCabAPIView.as_view(),name='get_cab'),
     
     path('venue_create',views.VenueCreateAPIView.as_view(),name='venue_create'),
     path('venue_update/<int:pk>',views.VenueUpdateAPIView.as_view(),name='venue_update'),
     path('venue_list',views.VenueListAPIView.as_view(),name='venue_list'),
     path('venue_delete/<int:pk>',views.VenueDeleteAPIView.as_view(),name='venue_delete'),
     path('all_venue',views.GetallVenueAPIView.as_view(),name='all_venue'),
     path('get_venue/<int:pk>/<int:pk1>',views.GetVenueAPIView.as_view(),name='get_venue'),

     path('hotel_create',views.HotelCreateAPIView.as_view(),name='hotel_create'),
     path('hotel_update/<int:pk>',views.HotelUpdateAPIView.as_view(),name='hotel_update'),
     path('hotel_list',views.HotelListAPIView.as_view(),name='hotel_list'),
     path('hotel_delete/<int:pk>',views.HotelDeleteAPIView.as_view(),name='hotel_delete'),
     path('get_hotel/<int:pk>/<int:pk1>',views.GetHotelAPIView.as_view(),name='get_hotel'),

 
     path('contact_create',views.ContactCreateAPIView.as_view(),name='contact_create'),
     path('contact_update/<int:pk>',views.ContactUpdateAPIView.as_view(),name='contact_update'),
     path('contact_list',views.ContactListAPIView.as_view(),name='contact_list'),
     path('contact_delete/<int:pk>',views.ContactDeleteAPIView.as_view(),name='contact_delete'),
     path('get_contact/<int:pk>/<int:pk1>',views.GetContactsAPIView.as_view(),name='get_contact'),
 

     path('guestlist_create',views.GuestListCreateAPIView.as_view(),name='guestlist_create'),
     path('guestlist_update/<int:pk>',views.GuestListUpdateAPIView.as_view(),name='guestlist_update'),
     path('guestlist_list',views.GuestListListAPIView.as_view(), name="guestlist_list"),
     path('guestlist_delete/<int:pk>',views.GuestListDeleteAPIView.as_view(),name='guestlist_delete'),
     path('get_guestlist/<int:pk>/<int:pk1>',views.GetGuestlistAPIView.as_view(),name='get_guestlist'),

     
     path('settime_create',views.SetTimeCreateAPIView.as_view(),name='settime_create'),
     path('settime_update/<int:pk>',views.SetTimeUpdateAPIView.as_view(),name='settime_update'),
     path('settime_list',views.SetTimeListAPIView.as_view(), name="settime_list"),
     path('settime_delete/<int:pk>',views.SetTimeDeleteAPIView.as_view(),name='settime_delete'),
     path('all_set',views.GetAllSettimeAPIView.as_view(), name="all_set"),
     path('get_settime/<int:pk>/<int:pk1>',views.GetSettimeAPIView.as_view(),name='get_settime'),

     path('document_create',views.DocumentCreateAPIView.as_view(),name='document_create'),
     path('document_update/<int:pk>',views.DocumentUpdateAPIView.as_view(),name='document_update'),
     path('document_list',views.DocumentListAPIView.as_view(), name="document_list"),
     path('document_delete/<int:pk>',views.DocumentDeleteAPIView.as_view(),name='document_delete'),
     path('get_document/<int:pk>/<int:pk1>',views.GetDocumentAPIView.as_view(), name="get_document"),


     path('forgot_password',views.ForgotPasswordAPIView.as_view(),name='forgot_password'),
     path('otpcheck',views.OTPCheckAPIView.as_view(),name='otpcheck'),
     path('set_new_password',views.SetNewPasswordAPIView.as_view(),name='set_new_password'),
     
     
     path('all_data',views.allListView.as_view(),name='all_data'),
     path('all_data2',views.AllDataAPIView.as_view(),name='all_data2'),
     path('all_list/<int:pk>/<int:pk1>',views.alllistApiView.as_view(),name='all_list'),
    
]