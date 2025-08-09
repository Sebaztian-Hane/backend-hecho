from django.db import models
from django.utils import timezone

class Room(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"Room {self.number}"
