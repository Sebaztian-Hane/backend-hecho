from django import forms
from .models import PaymentType

class StorePaymentTypeForm(forms.ModelForm):
    class Meta:
        model = PaymentType
        fields = '__all__'
        error_messages = {
            'name': {
                'unique': 'Ya existe un tipo de pago con este nombre.',
                'required': 'El nombre es obligatorio.'
            },
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if PaymentType.objects.filter(name=name, deleted_at__isnull=True).exists():
            raise forms.ValidationError('Ya existe un tipo de pago con este nombre.')
        return name

class UpdatePaymentTypeForm(forms.ModelForm):
    class Meta:
        model = PaymentType
        fields = '__all__'
