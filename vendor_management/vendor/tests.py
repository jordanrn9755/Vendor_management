from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.utils import timezone

class VendorAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Smart Vendor',
            contact_details='smartvendor@mail.com',
            address='Pune',
            vendor_code='V123'
        )

    def test_vendor_performance_endpoint(self):
        url = reverse('vendor_performance', kwargs={'vendor_id': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_acknowledge_purchase_order_endpoint(self):
        po = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items=[],
            quantity=1,
            status='pending',
            issue_date=timezone.now()
        )
        url = reverse('acknowledge_purchase_order', kwargs={'po_id': po.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        po.refresh_from_db()
        self.assertIsNotNone(po.acknowledgment_date)

class VendorAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Smart Vendor',
            contact_details='smartvendor@mail.com',
            address='Pune',
            vendor_code='V123'
        )
        HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date=timezone.now(),
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

    def test_vendor_performance_endpoint(self):
        url = reverse('vendor_performance', kwargs={'vendor_id': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

