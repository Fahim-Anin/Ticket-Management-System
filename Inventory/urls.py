# Inventory/urls.py

from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet

router = DefaultRouter()
# Register the ViewSet. This creates the URL: /inventory/
router.register(r'inventory', InventoryViewSet, basename='inventory')

urlpatterns = router.urls