from django.urls import path
from .views import (
    ListCreateShipmentAPIView,
    BulkCreateShipmentAPIView,
    AssignDriverAPIView,
    UpdateShipmentStatusAPIView,
    ShipmentDetailAPIView,
    BulkUpdateShipmentStatusAPIView
)

urlpatterns = [
    path('', ListCreateShipmentAPIView.as_view(), name='list-create-shipments'),  # GET + POST
    path('bulk-create/', BulkCreateShipmentAPIView.as_view(), name='bulk-create-shipment'),
    path('<int:pk>/assign-driver/', AssignDriverAPIView.as_view(), name='assign-driver'),
    path('<int:pk>/update-status/', UpdateShipmentStatusAPIView.as_view(), name='update-status'),
    path('<int:pk>/', ShipmentDetailAPIView.as_view(), name='shipment-detail'),
    path('bulk-update-status/', BulkUpdateShipmentStatusAPIView.as_view(), name='bulk-update-status'),
]