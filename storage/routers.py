from rest_framework import routers
from files_manager.views import DataViewSet

router = routers.DefaultRouter()
router.register(r'files', DataViewSet, basename='data')
