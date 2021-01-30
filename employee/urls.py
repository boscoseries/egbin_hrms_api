from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StaffViewsets, CustomObtainTokenPairView
from rest_framework_simplejwt.views import (TokenRefreshView, TokenVerifyView,
                                            TokenObtainPairView)

app_name = 'employee'

router = DefaultRouter()
router.register('', StaffViewsets)

urlpatterns = [
    path('token/', CustomObtainTokenPairView.as_view(), name='signin'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('token/verify/', TokenVerifyView.as_view(), name='verify-token'),
]

urlpatterns += router.urls