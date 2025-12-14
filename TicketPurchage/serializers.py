from rest_framework import serializers

class BookingSerializer(serializers.Serializer):
    # We do not use ModelSerializer yet, as this is for INPUT validation only.

    # Field 1: Inventory ID (The specific slot counter the user wants to buy from)
  inventory_id = serializers.IntegerField(min_value=1)
    
    # OLD: quantity = serializers.IntegerField(min_value=1, max_value=1) 
    # NEW: The constraint is removed, relying only on the view's availability check
  quantity = serializers.IntegerField(min_value=1)
  
# TicketPurchage/serializers.py

from rest_framework import serializers
from .models import TicketPurchase # Ensure TicketPurchase is imported here!

# Create a new serializer for displaying purchase history
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPurchase
        fields = ['id', 'inventory', 'quantity', 'booked_at','status']

# ... (BookingSerializer remains below this) ...  