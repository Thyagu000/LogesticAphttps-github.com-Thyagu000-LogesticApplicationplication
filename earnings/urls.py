from django.urls import path
from .views import (
    DriverEarningsView,
    PayoutListView,
    PayoutDetailView,
    ProcessPayoutView
)

urlpatterns = [

    path('drivers/<int:id>/earnings/', DriverEarningsView.as_view()),
    path('payouts/', PayoutListView.as_view()),
    path('payouts/<int:id>/', PayoutDetailView.as_view()),
    path('payouts/process/', ProcessPayoutView.as_view()),
]
