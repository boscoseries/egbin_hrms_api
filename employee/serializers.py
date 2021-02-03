from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authentication import authenticate
from .models import User


class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "firstname", "lastname", "middlename", "staff_id",
                  "role")


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("user_permissions", "groups")


class UserListSerializer(serializers.ModelSerializer):
    line_manager = StaffListSerializer()

    class Meta:
        model = User
        exclude = ("user_permissions", "groups")


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset"""
    staff_id = serializers.CharField()
    new_password = serializers.CharField()

    def create(self, validated_data):
        password = validated_data.get('new_password')
        staff = User.objects.filter(
            staff_id=validated_data.get('staff_id', None)).first()
        if staff:
            staff.set_password(password)
            staff.save()
            return staff
        raise Exception("No staff with supplied ID")


class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {'no_active_account': 'Password does not match.'}

    def validate(self, attrs):
        super().validate(attrs)
        serializer = StaffListSerializer(authenticate(**attrs))
        data = serializer.data
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return {"result": data}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token.id = user.id
        token['role'] = user.role
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token['annual_leave'] = user.annual_leave
        token['sick_leave'] = user.sick_leave
        token['compassionate_leave'] = user.compassionate_leave
        token['exam_leave'] = user.exam_leave
        return token