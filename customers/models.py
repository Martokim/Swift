from django.db import models

# Create your models here.
class Customer(models.Model):
    image = models.ImageField(upload_to='customers_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    #admission number
    admission_number = models.IntegerField(default=0)
    email = models.EmailField(max_length=25)
    gender = models.CharField(max_length=10, default="Not specified")
    age = models.IntegerField(default=0)



# constructor
    def __str__(self):
       return self.name
    
from django.db import models

#order models
class Order(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
