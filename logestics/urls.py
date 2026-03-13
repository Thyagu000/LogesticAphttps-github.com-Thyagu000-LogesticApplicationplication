"""
URL configuration for logestics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/drivers/', include('drivers.urls')),  #urls.py is not there yet
    #
    # path('api/auth/',include('auth_system.urls')),
    #path('api/earnings/', include('earnings.urls')),
    #path('api/tracking/',include('tracking.urls')),
    #path('', lambda request: redirect('tracking-index')),
    #path('api/parcelmanagement/',include('parcelmanagement.urls')),
    #path('api/logestics/',include('shipment.urls')),
    #path('api/payments/',include('payments.urls')),
    #path('api/tracking/',include('tracking.urls')),
    path('api/shipments/',include('shipments.urls')),
    

]
