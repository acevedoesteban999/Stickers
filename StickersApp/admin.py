from django.contrib import admin
from .models import Product,Movement,RegisteCash,Visits,UsEr,SummaryDate,Category,SubCategory,SubCategoryColor
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class UsErAdmin(UserAdmin ):
        fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined","is_admin","is_worker","image")}),
    )
admin.site.register(UsEr, UsErAdmin)
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubCategoryColor)
admin.site.register(Movement)
admin.site.register(RegisteCash)
admin.site.register(Visits)
admin.site.register(SummaryDate)
