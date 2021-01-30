from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StaffViewsets

app_name = 'employee'

router = DefaultRouter()
router.register('', StaffViewsets)

urlpatterns = [
    path('', include(router.urls)),
]