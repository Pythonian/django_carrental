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
    path('signup/carvendor/',
         views.VendorSignUpView.as_view(), name='vendor_signup'),
]
