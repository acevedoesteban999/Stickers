from django.contrib import admin
from .models import Product,Movement,RegisteCash
# Register your models here.
admin.site.register(Product)
admin.site.register(Movement)
admin.site.register(RegisteCash)