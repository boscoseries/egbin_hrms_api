from rest_framework import serializers
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
