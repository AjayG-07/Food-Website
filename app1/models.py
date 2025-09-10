from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=50)
    disciption = models.CharField(max_length=250)
    img = models.ImageField(upload_to='img/', blank=True, null=True)
    prize = models.IntegerField()


class FoodCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True,related_name='cart')
    food =models.ForeignKey('Food',on_delete=models.CASCADE)
    quantity  =models.PositiveBigIntegerField(default=1)

    def total_food_price(self):
        return  self.food.prize * self.quantity 
    
    def __str__(self):
        return f"{self.food.name} - {self.quantity}"
    


class CustomUser(AbstractUser):  
    pass
