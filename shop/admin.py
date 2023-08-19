from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(Shop)
admin.site.register(Review)
admin.site.register(Page)
admin.site.register(Categorie)

