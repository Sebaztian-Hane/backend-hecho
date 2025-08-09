from django.urls import path
from .views import AppointmentStatusListCreateView, AppointmentStatusDetailUpdateView, AppointmentStatusAuditHistoryView

urlpatterns = [
    path('', AppointmentStatusListCreateView.as_view(), name='appointmentstatus-list-create'),
    path('<int:pk>/', AppointmentStatusDetailUpdateView.as_view(), name='appointmentstatus-detail-update'),
    path('<int:pk>/audit-history/', AppointmentStatusAuditHistoryView.as_view(), name='appointmentstatus-audit-history'),
]
