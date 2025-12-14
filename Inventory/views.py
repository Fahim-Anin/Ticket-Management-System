# Inventory/views.py

from rest_framework import viewsets
from .models import Inventory
from .serializers import InventorySerializer
from rest_framework.permissions import AllowAny # Allows unauthenticated users to view the list


# Browser / Postman
#         ↓
# URL → View (ViewSet)
#         ↓
# View asks MODEL for data (ORM)
#         ↓
# Model returns Python objects
#         ↓
# View passes objects to SERIALIZER
#         ↓
# Serializer converts objects → JSON
#         ↓
# Response sent back


class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    
    # DRF automatically gives you:

    # list() → /inventory/

    # retrieve() → /inventory/3/

    # You did NOT write these methods
    # DRF already wrote them for you.
    # API endpoint that allows customers to view the available inventory slots.

    serializer_class = InventorySerializer
    permission_classes = [AllowAny] # This list is public, so no login is needed
# This runs BEFORE database access.

# Meaning:

# Anyone can access this API

# No login required

# If this was missing:

# Default permission might block access

    def get_queryset(self):
       # get_queryset() does not call the model  It asks the ORM manager to fetch rows described by the model
        """
        Custom queryset to filter the inventory list.
        We only want to show destinations that are active and have slots remaining.
        When someone requests data, THIS is how you get it.
        """
        
        return Inventory.objects.filter(
#             What this means:

# “Hey Django ORM, I want to work with the Inventory table.”

# This manager(objects.) already knows:

# Table name

# Columns

# Foreign keys

# Relationships

            
            # This is Django ORM talking to the database.

            # This line prepares a SQL query.
            # Filter 1: Available slots must be greater than 0
            available_slots__gt=0, 
            # Only return rows where available_slots > 0”
            # WHERE available_slots > 0
            # Filter 2: The related Destination must be marked as active
            destination__is_active=True 
            
            # “Look at the related Destination table
            # Only return inventory whose destination.is_active = True”
            # SQL Query:
            # JOIN destination ON inventory.destination_id = destination.id WHERE destination.is_active = TRUE
    
            
        ).select_related('destination') # Optimizes the database query (less work)
# Meaning:

# “Fetch Inventory + Destination in ONE SQL query”

# Without this:

# Django would hit DB again for every inventory.destination

# With this:

# One clean JOIN query

# After SQL executes, Django returns: 
# [
#   Inventory(pk=3, destination=Destination("chittagong"), total_slots=3, available_slots=3),
#   Inventory(pk=4, destination=Destination("coxsbazar"), total_slots=5, available_slots=2)
# ]
# 📌 THESE ARE NOT JSON
# 📌 THESE ARE PYTHON OBJECTS

#  Now the serializer:Loops over each Inventory object Reads its fields Reads related Destination Builds JSON
