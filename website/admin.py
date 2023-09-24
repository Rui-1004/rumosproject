from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Address, Cart, CartItem, Order, Category

admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)