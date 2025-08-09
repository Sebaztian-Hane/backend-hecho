from django.urls import path
from .views import RoomListCreateView, RoomDetailUpdateView, AvailableRoomsByDateView

urlpatterns = [
    path('', RoomListCreateView.as_view(), name='room-list-create'),
    path('<int:pk>/', RoomDetailUpdateView.as_view(), name='room-detail-update'),
    path('available-by-date/', AvailableRoomsByDateView.as_view(), name='room-available-by-date'),
]
