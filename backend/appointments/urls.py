from django.urls import path
from appointments.views import (
    AppointmentListCreateView, AppointmentDetailUpdateView,
    SearchAppointmentsView, PaginatedAppointmentsByDateView,
    PendingAppointmentsCalendarByDateView, CompletedAppointmentsCalendarByDateView,
    AppointmentAuditHistoryView, AppointmentChangeStatusView
)

urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('<int:pk>/', AppointmentDetailUpdateView.as_view(), name='appointment-detail-update'),
    path('search/', SearchAppointmentsView.as_view(), name='search-appointments'),
    path('paginated-by-date/', PaginatedAppointmentsByDateView.as_view(), name='paginated-appointments-by-date'),
    path('pending-calendar/', PendingAppointmentsCalendarByDateView.as_view(), name='pending-appointments-calendar'),
    path('completed-calendar/', CompletedAppointmentsCalendarByDateView.as_view(), name='completed-appointments-calendar'),
    path('<int:pk>/audit-history/', AppointmentAuditHistoryView.as_view(), name='appointment-audit-history'),
    path('<int:pk>/change-status/', AppointmentChangeStatusView.as_view(), name='appointment-change-status'),
]