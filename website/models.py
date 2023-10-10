from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from core.settings import BASE_DIR



class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='static/uploads/product/', default=os.path.join(BASE_DIR, 'static', 'uploads', 'default.png'))

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=150, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = float(sum([item.get_total for item in orderitems]))
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=25)

    def __str__(self):
        return self.street


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length= 150)
    body = models.CharField(max_length= 500)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='static/uploads/question/', null=True, blank=True)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    body = models.CharField(max_length= 500)
    created_at = models.DateTimeField(auto_now_add=True)


class Challenge(models.Model):
    text = models.CharField(max_length=500)
    image = models.ImageField(upload_to='static/uploads/challenge/')
    correct_answer = models.CharField(max_length=255)
    date = models.DateField(null=True)
