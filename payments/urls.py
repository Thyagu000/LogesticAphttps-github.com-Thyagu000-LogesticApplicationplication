from django.urls import path
from . import views

urlpatterns = [

    # HTML Page
    path('', views.payment_page, name='payment-page'),
    path('edit/<int:pk>/', views.payment_page, name='edit-payment'),
    path('delete/<int:pk>/', views.delete_payment, name='delete-payment'),

    # API
    path('list/', views.payment_list),
    path('create/', views.create_payment),
]