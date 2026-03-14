from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item, Shipment
from .serializers import ItemSerializer, ShipmentSerializer


@api_view(['GET'])
def api_home(request):

    return Response({
        "message":"Logistics API running"
    })


@api_view(['GET'])
def get_items(request):

    items = Item.objects.all()
    serializer = ItemSerializer(items,many=True)

    return Response(serializer.data)


@api_view(['POST'])
def request_item(request):

    serializer = ShipmentSerializer(data=request.data)

    if serializer.is_valid():

        shipment = serializer.save()

        # simulate payment success
        shipment.payment_status = True
        shipment.save()

        return Response({
            "message":"Item requested successfully",
            "shipment_id":shipment.id
        })

    return Response(serializer.errors,)


@api_view(['GET'])
def track_shipment(request,id):

    shipment = Shipment.objects.get(id=id)

    return Response({
        "shipment_id":shipment.id,
        "status":shipment.delivery_status
    })


@api_view(['PUT'])
def update_status(request,id):

    shipment = Shipment.objects.get(id=id)

    status = request.data.get("status")

    shipment.delivery_status = status

    if status == "DELIVERED":
        shipment.delivery_location = request.data.get("location")

    shipment.save()

    return Response({
        "message":"Shipment updated successfully"
    })
