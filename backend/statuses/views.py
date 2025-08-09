from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .forms import StoreAppointmentStatusForm, UpdateAppointmentStatusForm
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from statuses.models import AppointmentStatus
from utils.permissions import class_login_required, class_permission_required

@method_decorator(csrf_exempt, name='dispatch')
@class_login_required
@class_permission_required('statuses.view_appointmentstatus')
@method_decorator(csrf_exempt, name='dispatch')
class AppointmentStatusAuditHistoryView(View):
    def get(self, request, pk):
        try:
            status = AppointmentStatus.objects.get(pk=pk, deleted_at__isnull=True)
            return JsonResponse({'audit_log': status.audit_log})
        except AppointmentStatus.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
@class_login_required
@class_permission_required('statuses.view_appointmentstatus')
@method_decorator(csrf_exempt, name='dispatch')
class AppointmentStatusListCreateView(View):
    def get(self, request):
        from django.core.paginator import Paginator
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 30))
        qs = AppointmentStatus.objects.filter(deleted_at__isnull=True)
        paginator = Paginator(qs, per_page)
        page_obj = paginator.get_page(page)
        items = list(page_obj.object_list.values())
        if not items:
            return JsonResponse({'message': 'Aún no se ha creado ningún estado de cita'}, status=200)
        return JsonResponse({
            'items': items,
            'total': paginator.count,
            'page': page_obj.number,
            'per_page': per_page
        })

    def post(self, request):
        data = json.loads(request.body)
        form = StoreAppointmentStatusForm(data)
        if form.is_valid():
            status = form.save()
            return JsonResponse({'id': status.id, 'name': status.name, 'description': status.description}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
@class_login_required
@class_permission_required('statuses.change_appointmentstatus')
@method_decorator(csrf_exempt, name='dispatch')
class AppointmentStatusDetailUpdateView(View):
    def delete(self, request, pk):
        try:
            status = AppointmentStatus.objects.get(pk=pk, deleted_at__isnull=True)
        except AppointmentStatus.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        status.deleted_at = timezone.now()
        status.save()
        return JsonResponse({'message': 'Estado de cita eliminado correctamente'})
    def patch(self, request, pk):
        try:
            status = AppointmentStatus.objects.get(pk=pk, deleted_at__isnull=True)
        except AppointmentStatus.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(status, key, value)
        status.save()
        return JsonResponse({'id': status.id, 'name': status.name, 'description': status.description})
    def get(self, request, pk):
        try:
            status = AppointmentStatus.objects.get(pk=pk, deleted_at__isnull=True)
            return JsonResponse({'id': status.id, 'name': status.name, 'description': status.description})
        except AppointmentStatus.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)

    def put(self, request, pk):
        try:
            status = AppointmentStatus.objects.get(pk=pk, deleted_at__isnull=True)
        except AppointmentStatus.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        form = UpdateAppointmentStatusForm(data, instance=status)
        if form.is_valid():
            status = form.save()
            return JsonResponse({'id': status.id, 'name': status.name, 'description': status.description})
        return JsonResponse({'errors': form.errors}, status=400)

    def delete(self, request, pk):
        try:
            status = AppointmentStatus.objects.get(pk=pk, deleted_at__isnull=True)
        except AppointmentStatus.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        status.delete()
        return JsonResponse({'message': 'Estado de cita eliminado correctamente'}, status=200)

