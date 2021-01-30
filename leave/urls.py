from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveViewsets

app_name = "leave"

router = DefaultRouter()
router.register('', LeaveViewsets)

urlpatterns = [
    path('', include(router.urls)),
]