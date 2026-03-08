from django.urls import path
from . import views  

urlpatterns = [
    path("shipments/<int:id>/tracking/", views.shipment_tracking),
    path("shipments/<int:id>/live-location/", views.shipment_live_location),
    path("shipments/export/", views.export_shipments),
    path("", views.api_root),  
]