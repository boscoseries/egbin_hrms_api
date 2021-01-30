from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .serializers import StaffSerializer
from .models import Staff
from .permissions import IsAdmin


# Create your views here.
class StaffViewsets(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['firstname', 'lastname', 'staff_id']

    def get_permission(self):
        permission_classes = super().get_permissions()
        if self.action in ['retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        return [permission for permission in permission_classes]
