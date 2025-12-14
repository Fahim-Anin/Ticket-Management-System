from .models import Destination
from rest_framework import serializers

class Destination(serializers.ModelSerializer):
    model = Destination
    fields=['Dest_Id' , 'name', 'is_active' , 'created_at' , 'updated_at']