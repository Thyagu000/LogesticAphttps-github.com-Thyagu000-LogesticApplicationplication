from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_page, name='payment-page'),
    path('edit/<int:pk>/', views.payment_page, name='edit-payment'),
    path('delete/<int:pk>/', views.delete_payment, name='delete-payment'),
]