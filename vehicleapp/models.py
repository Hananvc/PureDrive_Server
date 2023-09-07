from django.db import models
from django.core.exceptions import ValidationError

COLOR_CHOICES = (
    ('White','White'),
    ('Black','Black'),
    ('Green','Green'),
    ('Red','Red'),
    ('Yellow','Yellow'),
    ('Blue','Blue'),
    ('Brown','Brown'),
    ('Orange','Orange'),
)
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
def validate_default_image(value):
    if not value:
        raise ValidationError("Default image is required.")

def validate_brochure(value):
    if not value:
        raise ValidationError("Brochure is required.")

class Vehicle(models.Model):
    model_name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    brochure = models.FileField(upload_to='brochures/', null=True, blank=True, validators=[validate_brochure])
    default_image = models.ImageField(upload_to='default_images/', null=True, blank=True, validators=[validate_default_image])

    def clean(self):
        if not self.default_image:
            raise ValidationError("Default image is required.")

        if not self.brochure:
            raise ValidationError("Brochure is required.")

    def __str__(self):
        return self.model_name
    
class Variant(models.Model):
    name = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    color = models.CharField(choices=COLOR_CHOICES,max_length=50)
    battery_capacity_kwh = models.DecimalField(max_digits=5, decimal_places=2)
    range_km = models.PositiveIntegerField()
    charging_time_hours = models.PositiveIntegerField()
    motor_power_kw = models.PositiveIntegerField()
    fast_charging = models.BooleanField(default=False)
    year_manufactured = models.PositiveIntegerField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

  

    def __str__(self):
        return self.name
    
    
class image(models.Model):
    Variant=models.ForeignKey(Variant,on_delete=models.CASCADE,null=True,blank=True,related_name='images')
    Vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,null=True)
    images=models.ImageField(upload_to='vehicle_images',null=True)

    def __str__(self):
        if self.Variant:
            return f"{self.Variant.name}"
        elif self.Vehicle:
            return f"Vehicle image - {self.Vehicle.model_name}"
        else:
            return "Unnamed Image"
        

class News(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True)
    url = models.URLField(max_length=1000,null=True)
    url_to_image = models.URLField(max_length=1000,null=True)
    

    def __str__(self):
        return self.title
    

class test(models.Model):
    name=models.CharField( max_length=50)
    created_at=models.DateTimeField( auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.created_at}"

class testride(models.Model):
    booking_reference = models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    model_name=models.CharField(max_length=50)
    date=models.DateField()
    time=models.TimeField()
    dealer=models.CharField(max_length=50)
    dealer_email=models.EmailField()
    customer_name=models.CharField(max_length=50)
    customer_email=models.CharField(max_length=50)
    customer_phone=models.BigIntegerField()
    booking_status=models.CharField(max_length=50,default="Pending",null=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.model_name} - {self.dealer} - {self.date}"
