from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from vehicleapp.models import Brand

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_dealer', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser field is_active must be true')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser field is_staff must be true')
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser field is_admin must be True')
        
        if extra_fields.get('is_dealer') is not True:
            raise ValueError('Superuser field is_dealer must be True')
        
        return self.create_user(email=email, password=password, **extra_fields)

    

class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=250)
    username = models.CharField(max_length=50, null=True)
    phone_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    phone = models.PositiveBigIntegerField(null=True, validators=[phone_regex])
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_dealer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        if self.username:
            return f'{self.username} - {self.email}'
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    
class Dealer(models.Model):
    DISTRICT_CHOICES = [
        ('ernakulam', 'Ernakulam'),
        ('kannur', 'Kannur'),
        ('kollam', 'Kollam'),
        ('kozhikode', 'Kozhikode'),
        ('palakkad', 'Palakkad'),
        ('thiruvananthapuram', 'Thiruvananthapuram'),
        ('wayanad', 'Wayanad'),
        ('alappuzha', 'Alappuzha'),
        ('idukki', 'Idukki'),
        ('kasaragod', 'Kasaragod'),
        ('kottayam', 'Kottayam'),
        ('malappuram', 'Malappuram'),
        ('pathanamthitta', 'Pathanamthitta'),
        ('thrissur', 'Thrissur'),
    ]

    STATE_CHOICES = [
        ('kerala', 'Kerala'),
        # Add more state choices as needed
    ]

    COUNTRY_CHOICES = [
        ('india', 'India'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    website = models.CharField(max_length=150, null=True)
    address = models.TextField(null=True)
    district = models.CharField(max_length=20, choices=DISTRICT_CHOICES, null=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, null=True)
    pin_code = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, default='india', null=True)
    field_experience = models.IntegerField( null=True)
    num_staff = models.IntegerField(null=True)
    sales_contact_no = models.CharField(max_length=20, null=True)
    service_contact_no = models.CharField(max_length=20, null=True)


    def __str__ (self):
        return self.user.username

