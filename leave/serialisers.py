from datetime import datetime
from rest_framework import serializers
from .models import Leave
from django.core.exceptions import ValidationError
from employee.serializers import StaffListSerializer


class LeaveListSerializer(serializers.ModelSerializer):
    staff = StaffListSerializer()
    relieve_staff = StaffListSerializer()

    class Meta:
        model = Leave
        exclude = ("updated_at", )


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        exclude = ("updated_at", )

    def create(self, validated_data):
        validated_data['staff'] = self.context['request'].user
        return super().create(validated_data)


class LeaveUpdateSerializer(serializers.ModelSerializer):
    class Meta(LeaveSerializer.Meta):
        exclude = ("updated_at", )

    def update(self, instance, validated_data):
        if validated_data['status'] in ['REJECTED', "APPROVED"]:
            instance.status_updated_at = datetime.now()
        return super().update(instance, validated_data)


class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ("status", 'manager_note')
