from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.permissions import class_login_required, class_permission_required
import json
from django.http import JsonResponse
from django.views import View
from .models import PaymentType
from django.utils import timezone

@class_login_required
@class_permission_required('payment_types.view_paymenttype')
@method_decorator(csrf_exempt, name='dispatch')
class PaymentTypeListCreateView(View):
    def get(self, request):
        payment_types = list(PaymentType.objects.filter(deleted_at__isnull=True).values())
        if not payment_types:
            return JsonResponse({'message': 'Aún no se ha creado ningún tipo de pago'}, status=200)
        return JsonResponse(payment_types, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        payment_type = PaymentType.objects.create(**data)
        return JsonResponse({'id': payment_type.id}, status=201)

@class_login_required
@class_permission_required('payment_types.change_paymenttype')
@method_decorator(csrf_exempt, name='dispatch')
class PaymentTypeDetailUpdateView(View):
    def get(self, request, pk):
        try:
            payment_type = PaymentType.objects.get(pk=pk, deleted_at__isnull=True)
            data = {field.name: getattr(payment_type, field.name) for field in payment_type._meta.fields}
            return JsonResponse(data)
        except PaymentType.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)

    def put(self, request, pk):
        try:
            payment_type = PaymentType.objects.get(pk=pk, deleted_at__isnull=True)
        except PaymentType.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(payment_type, key, value)
        payment_type.save()
        return JsonResponse({'id': payment_type.id})

    def patch(self, request, pk):
        try:
            payment_type = PaymentType.objects.get(pk=pk, deleted_at__isnull=True)
        except PaymentType.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(payment_type, key, value)
        payment_type.save()
        return JsonResponse({'id': payment_type.id})

    def delete(self, request, pk):
        try:
            payment_type = PaymentType.objects.get(pk=pk, deleted_at__isnull=True)
        except PaymentType.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        payment_type.deleted_at = timezone.now()
        payment_type.save()
        return JsonResponse({'message': 'Tipo de pago eliminado correctamente'}, status=200)
