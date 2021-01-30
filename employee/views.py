from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (StaffSerializer, CustomObtainTokenPairSerializer,
                          PasswordResetSerializer)
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

    @action(methods=['POST'],
            detail=False,
            serializer_class=PasswordResetSerializer)
    def reset_password(self, request):
        """Endpoint to initiate Password reset"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            pass
        except Exception as e:
            return Response({"error": str(e)},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomObtainTokenPairView(TokenObtainPairView):
    """Login with staff_id, and password"""
    serializer_class = CustomObtainTokenPairSerializer
