from django.urls import path

from . import views

app_name = 'vehicle'

urlpatterns = [
    path('create/', views.vehicle_create, name='create'),
    path('vendors/', views.vendor_list, name='vendors'),
    path('compare/', views.compare_vehicles, name='compare'),
    path('confirm-booking/',
         views.confirm_booking, name='confirm_booking'),
    path('add-to-compare/<int:pk>/',
         views.add_to_compare, name='add_to_compare'),
    path('<int:pk>/', views.vehicle_detail, name='detail'),
    path('<int:pk>/update/', views.vehicle_update, name='update'),
    path('<int:pk>/delete/', views.vehicle_delete, name='delete'),
    path('', views.vehicle_list, name='list'),

]
