from django.urls import path
from . import views

urlpatterns = [
    path('', views.EarningsListView.as_view(), name='earnings-list'),  # /api/earnings/
    path('drivers/<int:driver_id>/', views.DriverEarningsView.as_view(), name='driver-earnings'),  # /api/earnings/drivers/1/
    path('payouts/', views.PayoutListView.as_view(), name='payout-list'),  # /api/earnings/payouts/
    path('payouts/<int:id>/', views.PayoutDetailView.as_view(), name='payout-detail'),  # /api/earnings/payouts/1/
    path('payouts/process/', views.PayoutProcessView.as_view(), name='payout-process'),  # /api/earnings/payouts/process/
]