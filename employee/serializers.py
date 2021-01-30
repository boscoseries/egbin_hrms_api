from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Staff


class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ("firstname", "lastname", "middlename", "staff_id", "role")


class StaffSerializer(serializers.ModelSerializer):
    line_manager = StaffListSerializer()

    class Meta:
        model = Staff
        exclude = ("user_permissions", "groups")


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset"""
    staff_id = serializers.CharField()
    new_password = serializers.CharField()

    def create(self, validated_data):
        password = validated_data.get('new_password')
        staff = Staff.objects.filter(
            staff_id=validated_data.get('staff_id', None)).first()
        if staff:
            staff.set_password(password)
            staff.save()
            return staff
        raise Exception("No staff with supplied ID")


class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {'invalid': 'Password does not match.'}

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token.id = user.id
        token['role'] = user.role
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token['staff_id'] = user.staff_id
        return token