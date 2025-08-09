from django.urls import path
from tickets.views import AvailableTicketsView, NextRoomNumberView, NextTicketNumberView, ResourceStatsView

urlpatterns = [
    path('available/', AvailableTicketsView.as_view(), name='available-tickets'),
    path('next-room/', NextRoomNumberView.as_view(), name='next-room-number'),
    path('next-ticket/', NextTicketNumberView.as_view(), name='next-ticket-number'),
    path('stats/', ResourceStatsView.as_view(), name='resource-stats'),
]
