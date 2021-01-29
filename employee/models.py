from django.db import models
import uuid

USER_ROLES = (("ADMIN", "ADMIN"), ("STAFF", "STAFF"))


def default_role():
    return "STAFF"


# Create your models here.
class Staff(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    staff_id = models.CharField(max_length=255)
    line_manager = models.ForeignKey('self',
                                     related_name='staff_line_manager',
                                     on_delete=models.SET_NULL)
    leave_balance = models.IntegerField(default=0)
    role = models.CharField(max_length=10,
                            choices=USER_ROLES,
                            default=default_role)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f"{self.firstname} - {self.lastname}"
