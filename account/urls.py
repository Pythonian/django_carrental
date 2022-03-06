from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logout/',
         auth_views.LogoutView.as_view(), name='logout'),
    path('login/',
         auth_views.LoginView.as_view(
             redirect_authenticated_user=True), name='login'),

    path('signup/customer/',
         views.CustomerSignUpView.as_view(), name='customer_signup'),
    path('customer/create-profile/',
         views.customer_create_profile, name='customer_create_profile'),
    path('customer/update-profile/',
         views.customer_update_profile, name='customer_update_profile'),
    path('customer/verify/',
         views.customer_verification, name='customer_verification'),

    path('signup/carvendor/',
         views.VendorSignUpView.as_view(), name='vendor_signup'),
    path('vendor/create-profile/',
         views.vendor_create_profile, name='vendor_create_profile'),
    path('vendor/update-profile/',
         views.vendor_update_profile, name='vendor_update_profile'),
    path('vendor/my-vehicles/',
         views.vendor_manage_vehicles, name='vendor_manage_vehicles'),
]
