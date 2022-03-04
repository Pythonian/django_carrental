from django.urls import path

from .views import (
    vehicle_create, vehicle_delete, vehicle_detail,
    vehicle_list, vehicle_update)

app_name = 'vehicle'

urlpatterns = [
    path('', vehicle_list, name='list'),
    path('create/', vehicle_create, name='create'),
    path('<int:pk>/', vehicle_detail, name='detail'),
    path('<int:pk>/update/', vehicle_update, name='update'),
    path('<int:pk>/delete/', vehicle_delete, name='delete'),
    
]