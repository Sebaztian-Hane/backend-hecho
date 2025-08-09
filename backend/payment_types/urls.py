from django.urls import path
from .views import PaymentTypeListCreateView, PaymentTypeDetailUpdateView

urlpatterns = [
    path('', PaymentTypeListCreateView.as_view(), name='paymenttype-list-create'),
    path('<int:pk>/', PaymentTypeDetailUpdateView.as_view(), name='paymenttype-detail-update'),
]
