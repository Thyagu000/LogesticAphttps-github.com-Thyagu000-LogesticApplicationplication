from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShipmentViewSet, ParcelViewSet

router = DefaultRouter()
router.register(r'shipments', ShipmentViewSet)
router.register(r'parcels', ParcelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]