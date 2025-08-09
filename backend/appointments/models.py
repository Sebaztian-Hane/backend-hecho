from django.db import models
from statuses.models import AppointmentStatus
from patients.models import Patient
from therapists.models import Therapist
from django.utils import timezone

class Appointment(models.Model):
    appointment_date = models.DateField()
    appointment_hour = models.TimeField()
    ailments = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    surgeries = models.TextField(blank=True, null=True)
    reflexology_diagnostics = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    initial_date = models.DateField(blank=True, null=True)
    final_date = models.DateField(blank=True, null=True)
    appointment_type = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    social_benefit = models.CharField(max_length=255, blank=True, null=True)
    payment_detail = models.TextField(blank=True, null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ticket_number = models.CharField(max_length=255, blank=True, null=True)
    appointment_status = models.ForeignKey(AppointmentStatus, on_delete=models.SET_NULL, null=True, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, related_name='appointments')
    therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, related_name='appointments')
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Auditoría de cambios
    status_history = models.JSONField(default=list, blank=True)

    def set_status(self, new_status):
        # Control de transiciones válidas
        valid_transitions = {
            'Pendiente': ['Confirmada', 'Cancelada'],
            'Confirmada': ['Completada', 'Cancelada'],
            'Completada': [],
            'Cancelada': []
        }
        current = self.appointment_status.name if self.appointment_status else None
        if current and new_status.name not in valid_transitions.get(current, []):
            raise ValueError(f"Transición inválida de {current} a {new_status.name}")
        # Registrar auditoría
        self.status_history.append({
            'from': current,
            'to': new_status.name,
            'timestamp': timezone.now().isoformat()
        })
        self.appointment_status = new_status
        self.save()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"Appointment {self.id} - {self.appointment_date}"
