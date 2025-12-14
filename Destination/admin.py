from django.contrib import admin
from .models import Destination # 1. Import your model

# In bookings_app/admin.py, add the following imports and class:

from .models import Destination
from Inventory.models import Inventory # Make sure to import Inventory

# We can reuse the DestinationAdmin from before, but add Inventory as an Inline!

# Click "Add Destination"
#    ↓
# DestinationAdmin builds form
#    ↓
# You click Save
#    ↓
# Destination.save() → DB
#    ↓
    # InventoryInline -> creates  form on Inventory table
# Inventory.save() → DB (inline)
#    ↓
# Admin loads list page
#    ↓
# total_slots_display(obj) is CALLED
#    ↓
# Value is DISPLAYED








class InventoryInline(admin.TabularInline):
    # imagine the boss says:

# “When I'm adding a new destination in admin,
# I want to add the seat information right there.
# I don’t want to go to another page to set slots.”

# This is exactly why Django made Inlines.

# Without Inline (bad):

# Admin adds a Destination first,

# Then goes to Inventory page separately,

# Then creates an Inventory and connects it to that Destination.

# This is extra work and confusing.

# With Inline (good):

# On the same page where admin types “Cox’s Bazar”,
# he will also see a small table:
    """Allows Inventory to be added/edited directly on the Destination page."""
    model = Inventory # Builds an Inline Formset for Inventory
    extra = 2 # Show 1 empty form by default  Django shows 1 empty row for Inventory.
    fields = ('total_slots', 'available_slots',)
    # Prevents admins from setting available slots higher than total slots manually
    readonly_fields = ('available_slots',) 
    
    # We remove the standard registration for Inventory and only use the Inline
    # admin.site.register(Inventory)  <-- DON'T use this line!


# Modify the DestinationAdmin class to include the InventoryInline
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    # ... (Keep the previous list_display, list_filter, etc.) ...
    inlines = [InventoryInline] 
    list_display = ('name', 'is_active', 'total_slots_display', 'created_at')
    
    # This list allows the Admin to see the slot count right on the Destination list page
    def total_slots_display(self, obj):
        # Tries to get the available slots for the destination
        inventory = obj.inventories.first()
        return f"{inventory.available_slots} / {inventory.total_slots}" if inventory else "N/A"
    total_slots_display.short_description = "Available / Total Slots"

    # Add the Inline here:
    
    #Lets you edit Inventory inside Destination admin page.
    
#DestinationAdmin
# → Controls how Destination looks in admin, and connects the inline.

# Inline saves after parent
# → Destination is stored first → then Inventory receives destination_id.

# Your Inventory.save() auto-fills available_slots
# → That is why pressing Save automatically sets available = total.
    readonly_fields = ('created_at', 'updated_at')