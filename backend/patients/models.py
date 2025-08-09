from django.db import models
from django.utils import timezone

class Patient(models.Model):
    name = models.CharField(max_length=255)
    paternal_lastname = models.CharField(max_length=255)
    maternal_lastname = models.CharField(max_length=255)
    document_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"{self.name} {self.paternal_lastname} {self.maternal_lastname}"
