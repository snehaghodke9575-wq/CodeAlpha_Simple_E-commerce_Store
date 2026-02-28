from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    discription=models.TextField()

    def __str__(self):
        return self.name
    


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.product.name} - {self.user.username}"
    
class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    total_price= models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    payment_id=models.CharField(max_length=200, blank=True, null=True)
    paid=models.BooleanField(default=False)


    def __str(self):
        return str(self.id)
    
      
     


      

    

