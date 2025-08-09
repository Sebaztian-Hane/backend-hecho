from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.permissions import class_login_required, class_permission_required
import json
from django.http import JsonResponse
from django.views import View
from .models import Therapist
from django.utils import timezone

@class_login_required
@class_permission_required('therapists.view_therapist')
@method_decorator(csrf_exempt, name='dispatch')
class TherapistListCreateView(View):
    def get(self, request):
        therapists = list(Therapist.objects.filter(deleted_at__isnull=True).values())
        if not therapists:
            return JsonResponse({'message': 'Aún no se ha creado ningún terapeuta'}, status=200)
        return JsonResponse(therapists, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        therapist = Therapist.objects.create(**data)
        return JsonResponse({'id': therapist.id}, status=201)

@class_login_required
@class_permission_required('therapists.change_therapist')
@method_decorator(csrf_exempt, name='dispatch')
class TherapistDetailUpdateView(View):
    def get(self, request, pk):
        try:
            therapist = Therapist.objects.get(pk=pk, deleted_at__isnull=True)
            data = {field.name: getattr(therapist, field.name) for field in therapist._meta.fields}
            return JsonResponse(data)
        except Therapist.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)

    def put(self, request, pk):
        try:
            therapist = Therapist.objects.get(pk=pk, deleted_at__isnull=True)
        except Therapist.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(therapist, key, value)
        therapist.save()
        return JsonResponse({'id': therapist.id})

    def patch(self, request, pk):
        try:
            therapist = Therapist.objects.get(pk=pk, deleted_at__isnull=True)
        except Therapist.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(therapist, key, value)
        therapist.save()
        return JsonResponse({'id': therapist.id})

    def delete(self, request, pk):
        try:
            therapist = Therapist.objects.get(pk=pk, deleted_at__isnull=True)
        except Therapist.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        therapist.deleted_at = timezone.now()
        therapist.save()
        return JsonResponse({'message': 'Terapeuta eliminado correctamente'}, status=200)
