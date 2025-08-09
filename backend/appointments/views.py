from appointments.services import AppointmentService
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.permissions import class_login_required, class_permission_required
import json
from appointments.forms import StoreAppointmentForm, UpdateAppointmentForm
from django.http import JsonResponse
from appointments.models import Appointment
from statuses.models import AppointmentStatus

@class_login_required
@class_permission_required('appointments.search_appointment')
@method_decorator(csrf_exempt, name='dispatch')
class SearchAppointmentsView(View):
    def post(self, request):
        data = json.loads(request.body)
        search = data.get('search', '')
        per_page = data.get('per_page', 30)
        page = data.get('page', 1)
        results = AppointmentService.search_appointments(search, per_page, page)
        if not results['items']:
            return JsonResponse({'message': 'No se encontraron citas con el término de búsqueda proporcionado'}, status=200)
        return JsonResponse(results)

@class_login_required
@class_permission_required('appointments.view_appointment')
@method_decorator(csrf_exempt, name='dispatch')
class PaginatedAppointmentsByDateView(View):
    def post(self, request):
        data = json.loads(request.body)
        date = data.get('date')
        per_page = data.get('per_page', 30)
        page = data.get('page', 1)
        results = AppointmentService.get_paginated_by_date(date, per_page, page)
        if not results['items']:
            return JsonResponse({'message': 'Aún no se ha creado ninguna cita'}, status=200)
        return JsonResponse(results)

@class_login_required
@class_permission_required('appointments.view_appointment')
@method_decorator(csrf_exempt, name='dispatch')
class PendingAppointmentsCalendarByDateView(View):
    def post(self, request):
        data = json.loads(request.body)
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        per_page = data.get('per_page', 30)
        page = data.get('page', 1)
        results = AppointmentService.get_pending_calendar_by_date(start_date, end_date, per_page, page)
        if not results['items']:
            return JsonResponse({'message': 'No hay citas pendientes'}, status=200)
        return JsonResponse(results)

@class_login_required
@class_permission_required('appointments.view_appointment')
@method_decorator(csrf_exempt, name='dispatch')
class CompletedAppointmentsCalendarByDateView(View):
    def post(self, request):
        data = json.loads(request.body)
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        per_page = data.get('per_page', 30)
        page = data.get('page', 1)
        results = AppointmentService.get_completed_calendar_by_date(start_date, end_date, per_page, page)
        if not results['items']:
            return JsonResponse({'message': 'Aún no se ha completado ninguna cita para este día'}, status=200)
        return JsonResponse(results)

@class_login_required
@class_permission_required('appointments.view_appointment')
@method_decorator(csrf_exempt, name='dispatch')
class AppointmentListCreateView(View):
    def get(self, request):
        appointments = list(Appointment.objects.filter(deleted_at__isnull=True).values())
        if not appointments:
            return JsonResponse({'message': 'Aún no se ha creado ninguna cita'}, status=200)
        return JsonResponse(appointments, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        form = StoreAppointmentForm(data)
        if form.is_valid():
            appointment = form.save()
            return JsonResponse({'id': appointment.id}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

@class_login_required
@class_permission_required('appointments.change_appointment')
@method_decorator(csrf_exempt, name='dispatch')
class AppointmentDetailUpdateView(View):
    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, deleted_at__isnull=True)
        except Appointment.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            if key == 'appointment_status' and isinstance(value, int):
                try:
                    value = AppointmentStatus.objects.get(pk=value)
                except AppointmentStatus.DoesNotExist:
                    continue
            setattr(appointment, key, value)
        appointment.save()
        result = {field.name: getattr(appointment, field.name) for field in appointment._meta.fields}
        if appointment.appointment_status:
            result['appointment_status'] = {
                'id': appointment.appointment_status.id,
                'name': appointment.appointment_status.name,
                'description': appointment.appointment_status.description
            }
        else:
            result['appointment_status'] = None
        return JsonResponse(result)
    def get(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, deleted_at__isnull=True)
            data = {field.name: getattr(appointment, field.name) for field in appointment._meta.fields}
            if appointment.appointment_status:
                data['appointment_status'] = {
                    'id': appointment.appointment_status.id,
                    'name': appointment.appointment_status.name,
                    'description': appointment.appointment_status.description
                }
            else:
                data['appointment_status'] = None
            return JsonResponse(data)
        except Appointment.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)

    def put(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        form = UpdateAppointmentForm(data, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            return JsonResponse({'id': appointment.id})
        return JsonResponse({'errors': form.errors}, status=400)

    def delete(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, deleted_at__isnull=True)
        except Appointment.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        appointment.delete()
        return JsonResponse({'message': 'Cita eliminada correctamente'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class AppointmentAuditHistoryView(View):
    def get(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, deleted_at__isnull=True)
            return JsonResponse({'status_history': appointment.status_history})
        except Appointment.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class AppointmentChangeStatusView(View):
    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, deleted_at__isnull=True)
        except Appointment.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        new_status_id = data.get('status_id')
        if not new_status_id:
            return JsonResponse({'message': 'Falta status_id'}, status=400)
        try:
            new_status = AppointmentStatus.objects.get(pk=new_status_id, deleted_at__isnull=True)
        except AppointmentStatus.DoesNotExist:
            return JsonResponse({'message': 'Status no encontrado'}, status=404)
        try:
            appointment.set_status(new_status)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=400)
        return JsonResponse({'message': 'Estado actualizado', 'status_history': appointment.status_history})

