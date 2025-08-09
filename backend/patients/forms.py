from django import forms
from .models import Patient

class StorePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        error_messages = {
            'document_number': {
                'unique': 'Ya existe un paciente con este número de documento.',
                'required': 'El número de documento es obligatorio.'
            },
            'name': {
                'required': 'El nombre es obligatorio.'
            },
        }

    def clean_document_number(self):
        document_number = self.cleaned_data['document_number']
        if Patient.objects.filter(document_number=document_number, deleted_at__isnull=True).exists():
            raise forms.ValidationError('Ya existe un paciente con este número de documento.')
        return document_number

class UpdatePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
