from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import StaffSerializer, CustomObtainTokenPairSerializer
from .models import Staff
from .permissions import IsAdmin


# Create your views here.
class StaffViewsets(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['firstname', 'lastname', 'staff_id']

    def get_permissions(self):
        permission_classes = [permissions.AllowAny]
        if self.action in ['retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        if self.action in ['list', 'update', 'partial_update', 'delete']:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]


class CustomObtainTokenPairView(TokenObtainPairView):
    """Login with staff_id, and password"""
    serializer_class = CustomObtainTokenPairSerializer
