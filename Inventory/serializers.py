# Inventory/serializers.py

from rest_framework import serializers
from .models import Inventory # Import the Inventory model

class InventorySerializer(serializers.ModelSerializer):
    # This field gets the 'name' from the related Destination model via the FK
    # Source='destination.name' tells the serializer:
    # 1. Look at the 'destination' FK field.
    # 2. Follow the FK to the Destination object.
    # 3. Grab the 'name' attribute from that object.
    destination_name = serializers.CharField(source='destination.name', read_only=True)

    class Meta:
        model = Inventory
        # Fields to expose in the API output (JSON)
        fields = (
            'id', 
            'destination_name', 
            'available_slots', 
            'total_slots',
            'is_active_destination' # We will add this helper field next
        )

    # Helper method to check the destination's status (for filtering)
    def get_is_active_destination(self, obj):
        # Accesses the related Destination object's is_active field
        return obj.destination.is_active

    # Add the helper method to the fields list
    is_active_destination = serializers.SerializerMethodField()