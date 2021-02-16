from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_admin=False, is_staff=False):
        if not email:
            raise ValueError("User must have an email")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password=None):
        user_obj = self.create_user(
            email,
            password=password,
            is_active= True,
            is_admin = True,
            is_staff=True
        )
        return user_obj

class Account(AbstractBaseUser):
    PROJECT_MANAGER = 1
    DEVELOPER = 2
    SUBMITER = 3
    ROLE_CHOICES = [
        (PROJECT_MANAGER,'Project Manager'),
        (DEVELOPER,'Developer'),
        (SUBMITER,'Submiter'),
    ]

    email = models.EmailField(max_length=254, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices= ROLE_CHOICES, default=3)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)