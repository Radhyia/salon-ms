from django.db import models
from sbs import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserRoles:
    CUSTOMER = 'customer'
    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'), 
        (ADMIN, 'Admin'),   
        (EMPLOYEE, 'Employee')
    ]



class SbsAccountManager(BaseUserManager):
    def create_user(self, email, password=None): 
        email = self.normalize_email(email=email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        email = self.normalize_email(email=email)
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):   
    email = models.EmailField(verbose_name="email", max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True) 
    last_name = models.CharField(max_length=30, blank=True, null=True) 
    role = models.CharField(max_length=20, choices=UserRoles.ROLE_CHOICES, default=UserRoles.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = SbsAccountManager()

    def get_short_name(self):
        return f"{self.first_name}"


class Profile(models.Model):
    # General fields
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='Phone Number')
    profile_pic = models.ImageField(upload_to='profile/', default="profile/default.jpg", verbose_name='Profile Picture')
    data_joined = models.DateTimeField(auto_now_add=True)

    # Customer fields
    address = models.TextField(blank=True, null=True, verbose_name='Your Address')
    location = models.CharField(max_length=30, blank=True, null=True, verbose_name='Your Location')

    # Employee fields
    skills = models.TextField(blank=True, null=True, verbose_name='Skills')
    experience_years = models.IntegerField(default=0, verbose_name='Experience Years')
    availability_status = models.BooleanField(default=True, verbose_name='Available for work')

    def _str_(self):
        return f"Profile for {self.get_full_name()}"
    
    def get_full_name(self):
        return f"{self.user.first_name.title()}-{self.user.last_name.title()}"
    
    def delete(self):
        self.profile_pic.delete()
        super().delete()