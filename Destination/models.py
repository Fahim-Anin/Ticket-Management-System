from django.db import models

# Create your models here.
class Destination(models.Model):
    name = models.CharField(
        max_length=255, 
        unique=True,  # Ensures no two destinations can have the same name (e.g., prevents "Barisal" and "barisal")
        verbose_name="Destination Name"
    )
    
    # 3. is_active (The Control Switch)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Selling Active" # Clearly shows what this field means in the Admin
    )
    
    # 4. Audit Fields (The Time Stamps)
    created_at = models.DateTimeField(
        auto_now_add=True  # Automatically sets the field to the time the object was first created
    )
    updated_at = models.DateTimeField(
        auto_now=True      # Automatically updates the field every time the object is saved
    )
    
    # --- Model Meta and String Representation ---

    class Meta:
        # Orders the list alphabetically by name in the database/admin interface
        ordering = ['name'] 
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

    def __str__(self):
        # This is what shows up in the Django Admin list and Foreign Key dropdowns
        return self.name
