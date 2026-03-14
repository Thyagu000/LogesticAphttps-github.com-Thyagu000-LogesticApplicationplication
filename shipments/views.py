# shipments/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import csv

from .models import Shipment
# Home Page
def home(request):
    return render(request, "shipments/home.html")


# ----------------------------
# API Root - /api/
# ----------------------------
@api_view(['GET'])
def api_root(request):
    return Response({"message": "Shipments API Running"})

# ----------------------------
# Shipment Tracking Template
# /api/shipments/<id>/tracking/
# ----------------------------
def shipment_tracking(request, id):
    shipment = get_object_or_404(Shipment, id=id)
    return render(request,"tracking.html",{"shipment":shipment})

# ----------------------------
# Shipment Live Location API
# /api/shipments/<id>/live-location/
# ----------------------------
@api_view(['GET'])
def shipment_live_location(request, id):
    try:
        shipment = Shipment.objects.get(id=id)
        data = {
            "shipment_id": shipment.id,
            "latitude": shipment.latitude,
            "longitude": shipment.longitude,
            "status": shipment.status
        }
        return Response(data)
    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

# ----------------------------
# Shipment Export CSV API
# /api/shipments/export/
# ----------------------------
@api_view(['GET'])
def export_shipments(request):
    shipments = Shipment.objects.all()

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="shipments.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID","Order ID","Customer","Latitude","Longitude","Status","Created At"])

    for shipment in shipments:
        writer.writerow([
            shipment.id,
            shipment.order_id,
            shipment.customer_name,
            shipment.latitude,
            shipment.longitude,
            shipment.status,
            shipment.created_at
        ])

    return response
