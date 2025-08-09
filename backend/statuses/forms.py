from django import forms
from .models import AppointmentStatus

class StoreAppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = AppointmentStatus
        fields = ['name', 'description']
        error_messages = {
            'name': {
                'unique': 'Este estado de cita ya está registrado.',
                'required': 'El nombre es obligatorio.',
                'max_length': 'El nombre no puede superar 255 caracteres.'
            },
            'description': {
                'max_length': 'La descripción no puede superar 500 caracteres.'
            }
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if AppointmentStatus.objects.filter(name=name, deleted_at__isnull=True).exists():
            raise forms.ValidationError('Este estado de cita ya está registrado.')
        return name

class UpdateAppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = AppointmentStatus
        fields = ['name', 'description']
        error_messages = {
            'name': {
                'unique': 'El estado de cita ya está registrado.',
                'max_length': 'El nombre no puede superar 255 caracteres.'
            },
            'description': {
                'max_length': 'La descripción no puede superar 500 caracteres.'
            }
        }
