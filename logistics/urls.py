from django.urls import path
from . import views

urlpatterns = [

path('',views.api_home),

path('items/',views.get_items),

path('request-item/',views.request_item),

path('shipment/<int:id>/track/',views.track_shipment),

path('shipment/<int:id>/update/',views.update_status),

]