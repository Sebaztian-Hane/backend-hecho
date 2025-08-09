from django import forms
from .models import Appointment

class StoreAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        error_messages = {
            'appointment_date': {
                'required': 'La fecha de la cita es obligatoria.',
                'invalid': 'La fecha de la cita no es válida.'
            },
            'appointment_hour': {
                'invalid': 'La hora de la cita no es válida.'
            },
            'patient_id': {
                'required': 'El paciente es obligatorio.'
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        patient_id = cleaned_data.get('patient_id')
        appointment_date = cleaned_data.get('appointment_date')
        appointment_hour = cleaned_data.get('appointment_hour')
        # Validación de solapamiento de citas
        if patient_id and appointment_date and appointment_hour:
            from appointments.models import Appointment
            exists = Appointment.objects.filter(
                patient_id=patient_id,
                appointment_date=appointment_date,
                appointment_hour=appointment_hour,
                deleted_at__isnull=True
            ).exists()
            if exists:
                raise forms.ValidationError('Ya existe una cita para este paciente en la fecha y hora seleccionadas.')
        # Autocompletado desde la última cita completa
        # (Solo si el campo está vacío)
        from patients.models import Patient
        if patient_id:
            last_appointment = Appointment.objects.filter(
                patient_id=patient_id,
                deleted_at__isnull=True
            ).order_by('-appointment_date', '-appointment_hour').first()
            if last_appointment:
                fields_to_fill = [
                    'diagnosis', 'ailments', 'surgeries', 'reflexology_diagnostics',
                    'medications', 'observation', 'initial_date'
                ]
                for field in fields_to_fill:
                    if not cleaned_data.get(field) and getattr(last_appointment, field, None):
                        cleaned_data[field] = getattr(last_appointment, field)
        return cleaned_data

class UpdateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
