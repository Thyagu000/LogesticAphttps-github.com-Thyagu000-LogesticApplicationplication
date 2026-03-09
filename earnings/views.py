from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drivers.models import DriverProfile
from .models import DriverEarning, Payout
from .serializers import DriverEarningSerializer, PayoutSerializer
from .services import process_payout
class DriverEarningsView(APIView):

    def get(self, request, id):

        earnings = DriverEarning.objects.filter(driver_id=id)
        serializer = DriverEarningSerializer(earnings, many=True)

        return Response({
            "message": "Driver earnings fetched",
            "data": serializer.data
        })
class PayoutListView(APIView):

    def get(self, request):
        payouts = Payout.objects.all()
        serializer = PayoutSerializer(payouts, many=True)

        return Response({
            "message": "Payout list",
            "data": serializer.data
        })
class PayoutDetailView(APIView):

    def get(self, request, id):
        payout = get_object_or_404(Payout, id=id)
        serializer = PayoutSerializer(payout)

        return Response({
            "message": "Payout details",
            "data": serializer.data
        })
class ProcessPayoutView(APIView):

    def post(self, request):

        driver_id = request.data.get('driver_id')
        earning_ids = request.data.get('earning_ids', [])

        driver = get_object_or_404(DriverProfile, id=driver_id)

        payout = process_payout(driver, earning_ids)

        serializer = PayoutSerializer(payout)

        return Response({
            "message": "Payout processed successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
