from django.db import models
from django.contrib.auth.models import User 

# Use string reference for the Inventory model
INVENTORY_MODEL = 'Inventory.Inventory' 

class TicketPurchase(models.Model):
    # Field 1: Customer Link (FK)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='purchases',
        verbose_name="Customer"
    )
    
    # Field 2: Inventory Link (FK) - What slot did they buy?
    inventory = models.ForeignKey(
        INVENTORY_MODEL, 
        on_delete=models.PROTECT, 
        related_name='sales',
        verbose_name="Inventory Item"
    )
    
    # Field 3: Quantity (1 for our case, but flexible)
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantity Purchased"
    )
    
    # Field 4: Status tracking
    STATUS_CHOICES = (
        ('CONFIRMED', 'Confirmed'),
        # ... other statuses like PENDING or CANCELLED
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='CONFIRMED'
    )
    
    # Field 5: Timestamp
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Ticket Purchases"

    def __str__(self):
        return f"Purchase #{self.id} by {self.user.username} - {self.status}"
    
 
# Create a new serializer for displaying purchase history

from rest_framework import serializers
from TicketPurchage.models import TicketPurchase # Ensure TicketPurchase is imported here!
class HistorySerializer(serializers.ModelSerializer):
    # Use a ModelSerializer for simplicity
    class Meta:
        model = TicketPurchase
        # List all the fields you want to show the customer
        fields = ['id', 'inventory', 'quantity', 'purchase_date', 'status']    