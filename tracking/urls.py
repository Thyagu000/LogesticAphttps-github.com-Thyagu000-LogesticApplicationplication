from django.urls import path
from . import views

urlpatterns = [
    # Example URL patterns for your tracking app
    path('', views.index, name='tracking-index'),  # Home page for tracking
    path('shipments/', views.shipment_list, name='shipment-list'),  # List of shipments
    path('shipments/<uuid:pk>/', views.shipment_detail, name='shipment-detail'),  # Shipment detail
    path('notifications/', views.notifications, name='notifications'),  # Notifications list
]