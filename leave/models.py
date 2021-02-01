from datetime import datetime
from django.db import models
from employee.models import User
import uuid

LEAVE_TYPES = (
    ("sick_leave", "SICK LEAVE"),
    ("annual_leave", "ANNUAL LEAVE"),
    ("exam_leave", "EXAMINATION LEAVE"),
    ("compassionate_leave", "COMPASSIONATE LEAVE"),
)

LEAVE_STATUS = (
    ("PENDING", "PENDING"),
    ("APPROVED", "APPROVED"),
    ("REJECTED", "ANNUAL LEAVE"),
)


def default_status():
    return "PENDING"


def default_type():
    return "ANNUAL"


# Create your models here.
class Leave(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    staff = models.ForeignKey(User,
                              on_delete=models.SET_NULL,
                              related_name='staff_leaves',
                              null=True)
    type = models.CharField(max_length=20,
                            choices=LEAVE_TYPES,
                            default=default_type)
    status = models.CharField(max_length=20,
                              choices=LEAVE_STATUS,
                              default=default_status)
    relieve_staff = models.ForeignKey(User,
                                      on_delete=models.SET_NULL,
                                      related_name="leave_relieve_staff",
                                      null=True)
    leave_start = models.DateTimeField()
    leave_end = models.DateTimeField()
    resumption_date = models.DateTimeField()
    duration = models.IntegerField(null=True)
    description = models.TextField(null=True)
    manager_note = models.TextField(null=True)
    status_updated_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"{self.staff.firstname} - {self.status}"

    def update_status(self, status):
        self.update(status=status, status_updated_at=datetime.now())
        self.save()
        self.refresh_from_db
        return self.status
