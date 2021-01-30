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

    def validate(self, attrs):
        user = self.context['request'].user
        type = attrs.get('type')
        duration = attrs.get('duration')
        if type == "annual_leave" and duration >= 14:
            raise serializers.ValidationError(
                "Please input a duration below 14 days")
        if int(duration) > getattr(user, type):
            raise serializers.ValidationError(
                "you requested more than your available days")
        return super().validate(attrs)


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
