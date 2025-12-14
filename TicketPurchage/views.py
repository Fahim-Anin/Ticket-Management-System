# Booking/views.py - CLEANED VERSION

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

# Core Models and Serializer
from .models import TicketPurchase
from Inventory.models import Inventory 
from .serializers import BookingSerializer


# Booking/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated # We need this import
from .models import TicketPurchase
from .serializers import BookingSerializer,CancelTicketSerializer # Assuming you want simple output

# ... other imports (APIView, transaction, etc.)
# The secure Booking View

class CancelTicketAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CancelTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchage_id = serializer.validated_data['purchage_id']
        quantity_to_cancel = serializer.validated_data['quantity']
        try:
            with transaction.atomic():
                purchage = TicketPurchase.objects.select_for_update().get(pk=purchage_id, user= request.user)
                if quantity_to_cancel>purchage.quantity:
                    return Response(
                        {"error": "Cannot cancel more tickets than were purchased for this item."},
                        status=status.HTTP_400_BAD_REQUEST
                    )    
                # update increased inventory table slot     
                purchage.inventory.available_slots += quantity_to_cancel
                purchage.inventory.save()
                
                #update TicketPurchage table quantity slot
                purchage.quantity -= quantity_to_cancel
                purchage.save() # Save the updated purchase
        except TicketPurchase.DoesNotExist:
            return Response(
                {"error": "Purchase not found or you do not have permission to cancel it."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        # 9. Handle any other database errors
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred during cancellation."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        
                
class BookingCreateAPIView(APIView):
    # Remember to set the permission class in settings.py or here!
    # permission_classes = [IsAuthenticated] 
    
    def post(self, request, *args, **kwargs):
        # 1. Validate the incoming data
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        
#         serializer.validated_data = {
#   "inventory_id": 4,
#   "quantity": 3
# }
#         # Get data
        # Deserialize the incoming data 
        inventory_id = serializer.validated_data['inventory_id']
        quantity = serializer.validated_data['quantity']
        
        # 2. START THE SECURE TRANSACTION BLOCK
        try:
            with transaction.atomic(): 
#  This tells the database:

# “From here until the end, treat everything as ONE unit”

# Meaning:

# Either everything succeeds

# Or everything is undone

# If server crashes midway → DB rolls back.
                
                # --- A. ACQUIRE LOCK and retrieve Inventory ---
                inventory = Inventory.objects.select_for_update().get(pk=inventory_id)
# With select_for_update()-> What really happens:

# DB finds inventory row id=4. DB LOCKS that row

# Other requests must WAIT ⏸ This lock stays until: transaction ends or error happens .This is database-level locking, not Django magic.
                # --- B. DOUBLE-CHECK SLOTS ---
                if inventory.available_slots < quantity:
                    return Response(
                        {"error": "Booking failed: Not enough slots available."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # --- C. DECREMENT SLOTS ---
                inventory.available_slots -= quantity
                inventory.save()
                
                # --- D. CREATE PURCHASE RECORD ---
                user = request.user # The authenticated user is available here
                
                purchase = TicketPurchase.objects.create(
                    user=user, 
                    inventory=inventory,
                    quantity=quantity,
                    status='CONFIRMED'
                )
                
                # Transaction commits here. Slots permanently decreased and Purchase permanently saved. Lock released for another customer
                # response is sent and Postman sees success.
                return Response(
                    {"message": "Booking successful!", "purchase_id": purchase.id},
                    status=status.HTTP_201_CREATED
                )
                
        # Handle errors gracefully
# Is inventory_id an integer?

# Is quantity ≥ 1?

# If ❌ → Django stops here
        except Inventory.DoesNotExist:
            return Response(
                {"error": f"Inventory ID {inventory_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            


# TicketPurchage/views.py

# ... import HistorySerializer ...
from .serializers import HistorySerializer
class CustomerHistoryAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    # Django now sees the imported HistorySerializer class
    serializer_class = HistorySerializer 
    
    def get_queryset(self):
        # We previously confirmed this logic is correct
        return TicketPurchase.objects.filter(user=self.request.user).order_by('-booked_at')
# Reminder: Do not forget to clean up any old, unused imports or classes!            