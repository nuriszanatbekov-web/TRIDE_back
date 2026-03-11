from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email милдеттүү!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('M', 'Эркек'),
        ('F', 'Аял'),
    ]

    email          = models.EmailField(unique=True)
    first_name     = models.CharField(max_length=100)
    last_name      = models.CharField(max_length=100)
    date_of_birth  = models.DateField(null=True, blank=True)
    gender         = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    weight         = models.FloatField(null=True, blank=True)   # кг
    height         = models.FloatField(null=True, blank=True)   # см

    is_active          = models.BooleanField(default=False)  # email тастыкталганда True
    is_staff           = models.BooleanField(default=False)
    is_email_verified  = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class EmailVerificationCode(models.Model):
    """Email тастыктоо коду — 6 орундуу сан"""
    user       = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code       = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email} - {self.code}'