from django.db import models
from Destination.models import Destination
# Create your models here.
# In bookings_app/models.py, below the Destination model:

# HTTP Request
#    ↓
# ViewSet
#    ↓
# get_queryset()
#    ↓
# Inventory.objects (ORM Manager)
#    ↓
# SQL Query
#    ↓
# Inventory Python Objects
#    ↓
# Serializer
#    ↓
# JSON Response



class Inventory(models.Model):
# This class does 3 things at once:

# Defines a Python class

# Defines a Database table

# Registers itself with Django’s ORM
# objects = models.Manager()   # auto added by Django

    # Foreign Key 1 (FK1): Links to the Destination table
    destination = models.ForeignKey(
        Destination, 
        on_delete=models.CASCADE,  #DELETE all related Child records if i delete this destination
        related_name='inventories',
        # Forward Access (Standard): If you have an Inventory object, 
        # you access the destination like this: inventory.destination.name.

        # Reverse Access (Related Name): If you have a Destination object, 
        # you can access all its related Inventory objects using the related_name: destination.inventories.all()
        verbose_name="Related Destination"
    )
    
    # Total capacity (static input by admin)
    total_slots = models.PositiveIntegerField(
        default=0,
        verbose_name="Total Capacity"
    )
    
    # CRITICAL: The slot counter (decreased by booking logic)
    available_slots = models.PositiveIntegerField(
        default=0,
        verbose_name="Available Slots"
    )

    class Meta:
        verbose_name_plural = "Inventories"
        # Ensures no two inventory records can point to the same destination (if you only have one ticket type per destination)
        unique_together = ('destination',)
        # When an admin tries to create a new Inventory record, 
        # if the destination_id (the FK) already exists in another Inventory record, the database will raise an error and prevent the save.

    def __str__(self):
        return f"{self.destination.name} - Slots: {self.available_slots}"
    
    def save(self, *args, **kwargs):
        
        """
        This runs ONLY when:

        Admin clicks Save

        OR API creates Inventory
        Sets available_slots to total_slots only when the record is first created.
        """
        # Check if the object is new (has no primary key yet)
        if not self.pk: 
            # If it's a brand new record, initialize available slots to the total capacity
            self.available_slots = self.total_slots
# So when admin enters:

# total_slots = 5


# Django automatically sets:

# available_slots = 5


# 📌 This prevents manual mistakes
# 📌 This guarantees consistency
        super().save(*args, **kwargs) # Call the base save method
        
        
#         Admin form → Inventory object created

# save() runs

# available_slots auto-filled

# Data saved to DB