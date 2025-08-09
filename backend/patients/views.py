from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.permissions import class_login_required, class_permission_required
import json
from django.http import JsonResponse
from django.views import View
from .models import Patient
from django.utils import timezone

@class_login_required
@class_permission_required('patients.view_patient')
@method_decorator(csrf_exempt, name='dispatch')
class PatientListCreateView(View):
    def get(self, request):
        patients = list(Patient.objects.filter(deleted_at__isnull=True).values())
        if not patients:
            return JsonResponse({'message': 'Aún no se ha creado ningún paciente'}, status=200)
        return JsonResponse(patients, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        patient = Patient.objects.create(**data)
        return JsonResponse({'id': patient.id}, status=201)

@class_login_required
@class_permission_required('patients.change_patient')
@method_decorator(csrf_exempt, name='dispatch')
class PatientDetailUpdateView(View):
    def get(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk, deleted_at__isnull=True)
            data = {field.name: getattr(patient, field.name) for field in patient._meta.fields}
            return JsonResponse(data)
        except Patient.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)

    def put(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk, deleted_at__isnull=True)
        except Patient.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(patient, key, value)
        patient.save()
        return JsonResponse({'id': patient.id})

    def patch(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk, deleted_at__isnull=True)
        except Patient.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(patient, key, value)
        patient.save()
        return JsonResponse({'id': patient.id})

    def delete(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk, deleted_at__isnull=True)
        except Patient.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        patient.deleted_at = timezone.now()
        patient.save()
        return JsonResponse({'message': 'Paciente eliminado correctamente'}, status=200)
