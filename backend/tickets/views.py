from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.permissions import class_login_required, class_permission_required
import json
from django.http import JsonResponse
from django.views import View
from appointments.models import Appointment
from datetime import datetime

def is_weekend(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.weekday() >= 5

@class_login_required
@class_permission_required('tickets.view_ticket')
@method_decorator(csrf_exempt, name='dispatch')
class AvailableTicketsView(View):
    def post(self, request):
        data = json.loads(request.body)
        date = data.get('date')
        if not date:
            return JsonResponse({'error': 'date is required'}, status=400)
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
        except Exception:
            return JsonResponse({'error': 'Invalid date format, expected YYYY-MM-DD'}, status=400)
        max_rooms = 24 if is_weekend(date) else 14
        used_rooms = Appointment.objects.filter(appointment_date=date, room__isnull=False, deleted_at__isnull=True).values_list('room', flat=True)
        available_rooms = [i for i in range(1, max_rooms+1) if i not in used_rooms]
        max_tickets = 100
        used_tickets = Appointment.objects.filter(appointment_date=date, ticket_number__isnull=False, deleted_at__isnull=True).values_list('ticket_number', flat=True)
        available_tickets = [i for i in range(1, max_tickets+1) if i not in used_tickets]
        return JsonResponse({'available_rooms': available_rooms, 'available_tickets': available_tickets})

@class_login_required
@class_permission_required('tickets.view_ticket')
@method_decorator(csrf_exempt, name='dispatch')
class NextRoomNumberView(View):
    def post(self, request):
        data = json.loads(request.body)
        date = data.get('date')
        appointment_id = data.get('appointment_id')
        if not date:
            return JsonResponse({'error': 'date is required'}, status=400)
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
        except Exception:
            return JsonResponse({'error': 'Invalid date format, expected YYYY-MM-DD'}, status=400)
        max_rooms = 24 if is_weekend(date) else 14
        qs = Appointment.objects.filter(appointment_date=date, room__isnull=False, deleted_at__isnull=True)
        if appointment_id:
            qs = qs.exclude(id=appointment_id)
        used_rooms = list(qs.values_list('room', flat=True))
        for i in range(1, max_rooms+1):
            if i not in used_rooms:
                return JsonResponse({'room_number': i})
        room_count = len(used_rooms)
        return JsonResponse({'room_number': (room_count % max_rooms) + 1})

@class_login_required
@class_permission_required('tickets.view_ticket')
@method_decorator(csrf_exempt, name='dispatch')
class NextTicketNumberView(View):
    def post(self, request):
        data = json.loads(request.body)
        date = data.get('date')
        appointment_id = data.get('appointment_id')
        if not date:
            return JsonResponse({'error': 'date is required'}, status=400)
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
        except Exception:
            return JsonResponse({'error': 'Invalid date format, expected YYYY-MM-DD'}, status=400)
        qs = Appointment.objects.filter(appointment_date=date, ticket_number__isnull=False, deleted_at__isnull=True)
        if appointment_id:
            qs = qs.exclude(id=appointment_id)
        used_tickets = list(qs.values_list('ticket_number', flat=True))
        if not used_tickets:
            return JsonResponse({'ticket_number': 1})
        max_ticket = max(used_tickets)
        for i in range(1, max_ticket+1):
            if i not in used_tickets:
                return JsonResponse({'ticket_number': i})
        return JsonResponse({'ticket_number': max_ticket+1})

@class_login_required
@class_permission_required('tickets.view_ticket')
@method_decorator(csrf_exempt, name='dispatch')
class ResourceStatsView(View):
    def post(self, request):
        data = json.loads(request.body)
        date = data.get('date')
        if not date:
            return JsonResponse({'error': 'date is required'}, status=400)
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
        except Exception:
            return JsonResponse({'error': 'Invalid date format, expected YYYY-MM-DD'}, status=400)
        is_weekend_flag = is_weekend(date)
        max_rooms = 24 if is_weekend_flag else 14
        appointments_count = Appointment.objects.filter(appointment_date=date, deleted_at__isnull=True).count()
        rooms_used = Appointment.objects.filter(appointment_date=date, room__isnull=False, deleted_at__isnull=True).count()
        tickets_used = Appointment.objects.filter(appointment_date=date, ticket_number__isnull=False, deleted_at__isnull=True).count()
        room_usage_percentage = round((rooms_used / max_rooms) * 100, 2) if max_rooms > 0 else 0
        return JsonResponse({
            'date': date,
            'is_weekend': is_weekend_flag,
            'max_rooms': max_rooms,
            'total_appointments': appointments_count,
            'rooms_used': rooms_used,
            'rooms_available': max_rooms - rooms_used,
            'tickets_used': tickets_used,
            'room_usage_percentage': room_usage_percentage
        })
