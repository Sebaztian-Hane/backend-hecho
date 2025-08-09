from appointments.models import Appointment
from django.core.paginator import Paginator
from django.db.models import Q

class AppointmentService:
    @staticmethod
    def search_appointments(search, per_page=30, page=1):
        qs = Appointment.objects.filter(deleted_at__isnull=True)
        if search:
            qs = qs.filter(
                Q(ailments__icontains=search) |
                Q(diagnosis__icontains=search) |
                Q(patient__name__icontains=search) |
                Q(therapist__name__icontains=search)
            )
        paginator = Paginator(qs, per_page)
        page_obj = paginator.get_page(page)
        items = list(page_obj.object_list.values())
        return {
            'items': items,
            'total': paginator.count,
            'page': page_obj.number,
            'per_page': per_page
        }

    @staticmethod
    def get_paginated_by_date(date, per_page=30, page=1):
        qs = Appointment.objects.filter(appointment_date=date, deleted_at__isnull=True)
        paginator = Paginator(qs, per_page)
        page_obj = paginator.get_page(page)
        items = list(page_obj.object_list.values())
        return {
            'items': items,
            'total': paginator.count,
            'page': page_obj.number,
            'per_page': per_page
        }
