from django.db import models
from django.utils import timezone

class AppointmentStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Auditoría de restauración
    audit_log = models.JSONField(default=list, blank=True)

    def restore(self):
        self.deleted_at = None
        self.audit_log.append({
            'action': 'restore',
            'timestamp': timezone.now().isoformat()
        })
        self.save()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.name
