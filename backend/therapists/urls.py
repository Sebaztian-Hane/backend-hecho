from django.urls import path
from .views import TherapistListCreateView, TherapistDetailUpdateView

urlpatterns = [
    path('', TherapistListCreateView.as_view(), name='therapist-list-create'),
    path('<int:pk>/', TherapistDetailUpdateView.as_view(), name='therapist-detail-update'),
]
