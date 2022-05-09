from django.db import models
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class memberdetails(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(max_length=255, unique=True)
    verificationcode = models.CharField(max_length=6)
    accountId = models.CharField(max_length=10)
    containerId = models.CharField(max_length=255)
    imageId = models.CharField(max_length=255)
    client_data_client_endpoint = models.CharField(max_length=6)
    server_data_client_endpoint = models.CharField(max_length=6)
    gtm_endpoint = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    
    def __str__(self):
        return self.email

    objects = UserManager()

class files(models.Model):
    file_name = models.FileField(upload_to='media/')
    file_type = models.CharField(max_length=10, null=True, blank=True)
    member = models.ForeignKey(memberdetails, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)