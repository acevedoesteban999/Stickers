from django.contrib import admin
from .models import Product,Movement,RegisteCash,Category,Visits
# Register your models here.
admin.site.register(Product)
admin.site.register(Movement)
admin.site.register(Category)
admin.site.register(RegisteCash)
admin.site.register(Visits)
