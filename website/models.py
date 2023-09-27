from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from core.settings import BASE_DIR



class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    

    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=25)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='static/uploads/product/', default=os.path.join(BASE_DIR, 'static', 'default.png'))

    def __str__(self):
        return self.name

class Cart(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + '\'s Cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    cart_items = models.ManyToManyField(CartItem)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' Order'