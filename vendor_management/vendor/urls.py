from django.urls import path
from .views import *

urlpatterns = [
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-detail'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor_performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrder.as_view(), name='acknowledge_purchase_order'),

]