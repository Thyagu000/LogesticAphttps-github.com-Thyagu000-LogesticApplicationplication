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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tenants.views import TenantViewSet, TenantSettingViewSet
from users.views import TenantUserViewSet, RoleViewSet, PermissionViewSet
from rest_framework.authtoken import views


router = DefaultRouter()

# Tenant Management
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'tenant-settings', TenantSettingViewSet, basename='tenant-settings')

# User Management
router.register(r'tenant-users', TenantUserViewSet, basename='tenant-users')
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'permissions', PermissionViewSet, basename='permissions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/v1/shipments/', include('shipments.urls')),
]