from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response 
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404


# Create your views here.


class VendorListCreateAPIView(generics.GenericAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        vendors = self.get_queryset()
        serializer = self.get_serializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        vendor = self.get_object()
        serializer = self.get_serializer(vendor)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        vendor = self.get_object()
        serializer = self.get_serializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        vendor = self.get_object()
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class VendorPerformanceView(generics.GenericAPIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        performance = HistoricalPerformance.objects.filter(vendor=vendor).latest('date')
        data = {
            'on_time_delivery_rate': performance.on_time_delivery_rate,
            'quality_rating_avg': performance.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': performance.fulfillment_rate
        }
        return Response(data)


class AcknowledgePurchaseOrder(generics.GenericAPIView):
    def post(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        po.acknowledgment_date = timezone.now()
        po.save()
        return Response(status=status.HTTP_200_OK)
