from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
import uuid


class UserManager(BaseUserManager):
    def create_user(self, staff_id, password=None):
        """Creates and saves a new user"""
        if not staff_id:
            raise ValueError("Staff must have an Id")
        staff = self.model(staff_id, password)
        staff = super().create(staff_id=staff_id)
        staff.set_password(password)
        staff.save(using=self._db)
        return staff

    def create_superuser(self, staff_id, password):
        """Create and saves a new superuser"""
        staff_id = self.create_user(staff_id, password)
        staff_id.is_staff = True
        staff_id.is_superuser = True
        staff_id.save(using=self._db)
        return staff_id


USER_ROLES = (("ADMIN", "ADMIN"), ("STAFF", "STAFF"), ("MANAGER", "MANAGER"))


def default_role():
    return "STAFF"


# Create your models here.
class Staff(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    staff_id = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    line_manager = models.ForeignKey('self',
                                     related_name='staff_line_manager',
                                     on_delete=models.SET_NULL,
                                     blank=True,
                                     null=True)
    annual_leave = models.IntegerField(default=0)
    sick_leave = models.IntegerField(default=0)
    compassionate_leave = models.IntegerField(default=0)
    exam_leave = models.IntegerField(default=0)
    role = models.CharField(max_length=10,
                            choices=USER_ROLES,
                            default=default_role)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'staff_id'

    objects = UserManager()

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f"{self.firstname} - {self.lastname}"
