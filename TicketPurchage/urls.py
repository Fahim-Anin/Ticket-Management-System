from django.urls import path
from .views import BookingCreateAPIView,CustomerHistoryAPIView

urlpatterns = [
    # 1. Booking endpoint: Customer sends POST request here to buy a ticket
    path('buy/', BookingCreateAPIView.as_view(), name='buy_ticket'),
    path('my_history/', CustomerHistoryAPIView.as_view(), name='customer_history'),
]