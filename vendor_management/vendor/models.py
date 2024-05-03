from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f'{self.vendor}'


@receiver(post_save, sender=PurchaseOrder)
def update_metrics_on_completion(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        delivered_on_time_pos = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = delivered_on_time_pos.count() / completed_pos.count() if completed_pos.count() else 0

        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_pos_with_rating.aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating'] or 0

        successful_fulfillment_count = completed_pos.filter(issue_date__isnull=False, acknowledgment_date__isnull=False).count()
        fulfillment_rate = successful_fulfillment_count / completed_pos.count() if completed_pos.count() else 0

        HistoricalPerformance.objects.create(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            fulfillment_rate=fulfillment_rate
        )

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        total_response_time = sum((po.acknowledgment_date - po.issue_date).total_seconds() for po in pos)
        average_response_time = total_response_time / pos.count() if pos.count() else 0
        vendor.average_response_time = average_response_time
        vendor.save()

