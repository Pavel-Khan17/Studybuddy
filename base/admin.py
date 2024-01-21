from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import RoomModel, TopicModel, MassageModel
from .forms import CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ("id","name","username","email", "is_staff", "is_active",)
    list_filter = ("name","username","email")
    fieldsets = (
        (None, {"fields": ("name", "username","bio","email", "password",  "is_staff",
                "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide"),
            "fields": (
                "name", "username","bio","email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(CustomUser)
admin.site.register(RoomModel)
admin.site.register(TopicModel)
admin.site.register(MassageModel)

