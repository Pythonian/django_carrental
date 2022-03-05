from django.urls import path

from .views import (
    vehicle_create, vehicle_delete, vehicle_detail,
    vehicle_list, vehicle_update, vendor_list, compare_vehicles)

app_name = 'vehicle'

urlpatterns = [
    path('create/', vehicle_create, name='create'),
    path('vendors/', vendor_list, name='vendors'),
    path('compare/', compare_vehicles, name='compare'),
    path('<int:pk>/', vehicle_detail, name='detail'),
    path('<int:pk>/update/', vehicle_update, name='update'),
    path('<int:pk>/delete/', vehicle_delete, name='delete'),
    path('', vehicle_list, name='list'),

]
