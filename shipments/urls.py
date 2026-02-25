from django.urls import path
from .views import (
    CreateShipmentAPIView,
    ListShipmentAPIView,
    AssignDriverAPIView,
    UpdateShipmentStatusAPIView,
    BulkCreateShipmentAPIView,
    ShipmentDetailAPIView,
    BulkUpdateShipmentStatusAPIView
)

urlpatterns = [
    path('create/', CreateShipmentAPIView.as_view(), name='create-shipment'),
    path('bulk-create/', BulkCreateShipmentAPIView.as_view(), name='bulk-create-shipment'),
    path('', ListShipmentAPIView.as_view(), name='list-shipments'),
    path('<int:pk>/assign-driver/', AssignDriverAPIView.as_view(), name='assign-driver'),
    path('<int:pk>/update-status/', UpdateShipmentStatusAPIView.as_view(), name='update-status'),
    path('<int:pk>/', ShipmentDetailAPIView.as_view(), name='shipment-detail'),
    path('bulk-update-status/', BulkUpdateShipmentStatusAPIView.as_view(), name='bulk-update-status'),
    
    ]
