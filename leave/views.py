from django.shortcuts import render
from datetime import datetime
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Leave
from .serialisers import (LeaveSerializer, StatusUpdateSerializer,
                          LeaveUpdateSerializer, LeaveListSerializer)
from employee.permissions import IsAdmin, IsLineManagerOrAdmin


# Create your views here.
class LeaveViewsets(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['staff__id', 'staff__lastname', 'staff__firstname']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STAFF':
            return self.queryset.filter(staff=user)
        if user.role == 'MANAGER':
            return self.queryset.filter(staff__line_manager=user)
        return super().get_queryset()

    def get_permission(self):
        permission_classes = super().get_permissions()
        if self.action == 'update_status':
            permission_classes = [IsLineManagerOrAdmin]
        return [permission for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LeaveListSerializer
        if self.action == 'partial_update':
            return LeaveUpdateSerializer
        if self.action == 'update_status':
            return StatusUpdateSerializer
        else:
            return super().get_serializer_class()

    @action(methods=['PATCH'],
            detail=True,
            serializer_class=StatusUpdateSerializer,
            url_path="update_status")
    def update_status(self, request, pk=id):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(data=request.data,
                                             partial=True,
                                             instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['status_updated_at'] = datetime.now()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return str(e)