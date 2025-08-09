from django import forms
from .models import Therapist

class StoreTherapistForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = '__all__'
        error_messages = {
            'document_number': {
                'unique': 'Ya existe un terapeuta con este número de documento.',
                'required': 'El número de documento es obligatorio.'
            },
            'name': {
                'required': 'El nombre es obligatorio.'
            },
        }

    def clean_document_number(self):
        document_number = self.cleaned_data['document_number']
        if Therapist.objects.filter(document_number=document_number, deleted_at__isnull=True).exists():
            raise forms.ValidationError('Ya existe un terapeuta con este número de documento.')
        return document_number

class UpdateTherapistForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = '__all__'
