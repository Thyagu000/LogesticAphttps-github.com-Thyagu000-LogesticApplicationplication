from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tracking-index'),  # Home page for tracking
    path('shipments/', views.shipment_list, name='shipment-list'),  # List of shipments
    path('shipments/<int:pk>/', views.shipment_detail, name='shipment-detail'),
    path('notifications/', views.notifications, name='notifications'),  # Notifications list
]