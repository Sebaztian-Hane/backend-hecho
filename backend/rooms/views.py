from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.permissions import class_login_required, class_permission_required
import json
from django.http import JsonResponse
from django.views import View
from .models import Room
from django.utils import timezone
from appointments.models import Appointment
from datetime import datetime

@method_decorator(csrf_exempt, name='dispatch')
class AvailableRoomsByDateView(View):
    ## @class_login_required
    ## @class_permission_required('rooms.view_room')
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        data = json.loads(request.body)
        date = data.get('date')
        if not date:
            return JsonResponse({'error': 'date is required'}, status=400)
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
        except Exception:
            return JsonResponse({'error': 'Invalid date format, expected YYYY-MM-DD'}, status=400)
        used_rooms = Appointment.objects.filter(appointment_date=date, room__isnull=False, deleted_at__isnull=True).values_list('room', flat=True)
        available_rooms = list(Room.objects.filter(deleted_at__isnull=True).exclude(number__in=used_rooms).values())
        return JsonResponse({'available_rooms': available_rooms})

@method_decorator(csrf_exempt, name='dispatch')
class RoomListCreateView(View):
    ## @class_login_required
    ## @class_permission_required('rooms.view_room')
    @method_decorator(csrf_exempt, name='dispatch')
    def get(self, request):
        rooms = list(Room.objects.filter(deleted_at__isnull=True).values())
        if not rooms:
            return JsonResponse({'message': 'Aún no se ha creado ninguna habitación'}, status=200)
        return JsonResponse(rooms, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        room = Room.objects.create(**data)
        return JsonResponse({'id': room.id}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class RoomDetailUpdateView(View):
    ## @class_login_required
    ## @class_permission_required('rooms.change_room')
    @method_decorator(csrf_exempt, name='dispatch')
    def get(self, request, pk):
        try:
            room = Room.objects.get(pk=pk, deleted_at__isnull=True)
            data = {field.name: getattr(room, field.name) for field in room._meta.fields}
            return JsonResponse(data)
        except Room.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)

    def put(self, request, pk):
        try:
            room = Room.objects.get(pk=pk, deleted_at__isnull=True)
        except Room.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(room, key, value)
        room.save()
        return JsonResponse({'id': room.id})

    def patch(self, request, pk):
        try:
            room = Room.objects.get(pk=pk, deleted_at__isnull=True)
        except Room.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(room, key, value)
        room.save()
        return JsonResponse({'id': room.id})

    def delete(self, request, pk):
        try:
            room = Room.objects.get(pk=pk, deleted_at__isnull=True)
        except Room.DoesNotExist:
            return JsonResponse({'message': 'No encontrado'}, status=404)
        room.deleted_at = timezone.now()
        room.save()
        return JsonResponse({'message': 'Habitación eliminada correctamente'}, status=200)
