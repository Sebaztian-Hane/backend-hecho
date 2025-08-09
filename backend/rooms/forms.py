from django import forms
from .models import Room

class StoreRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        error_messages = {
            'number': {
                'unique': 'Ya existe una habitación con este número.',
                'required': 'El número de habitación es obligatorio.'
            },
        }

    def clean_number(self):
        number = self.cleaned_data['number']
        if Room.objects.filter(number=number, deleted_at__isnull=True).exists():
            raise forms.ValidationError('Ya existe una habitación con este número.')
        return number

class UpdateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
