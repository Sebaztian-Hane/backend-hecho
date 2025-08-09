from django.urls import path
from .views import PatientListCreateView, PatientDetailUpdateView

urlpatterns = [
    path('', PatientListCreateView.as_view(), name='patient-list-create'),
    path('<int:pk>/', PatientDetailUpdateView.as_view(), name='patient-detail-update'),
]
