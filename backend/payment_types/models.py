from django.db import models
from django.utils import timezone

class PaymentType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.name
