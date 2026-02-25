from rest_framework import viewsets
from .models import Shipment, Parcel
from .serializers import ShipmentSerializer, ParcelSerializer

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer