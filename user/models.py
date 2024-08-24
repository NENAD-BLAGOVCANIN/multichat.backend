from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from subscription.models import Subscription, UserSubscription

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, name=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    email = models.EmailField(max_length=60, unique=True, null=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    name = models.CharField(max_length=30)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    notifications = models.BooleanField(default=True)
    audio_notifications = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

    def get_subscription(self):
        active_subscription = (
            UserSubscription.objects.filter(user=self, status=UserSubscription.STATUS_ACTIVE)
            .order_by('-id')
            .first()
        )
        if active_subscription:
            return active_subscription.subscription
        else:
            return Subscription.objects.get(id=1)


    class Meta:
        db_table = "user"
