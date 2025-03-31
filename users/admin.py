from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Users

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Users
    list_display = ['email', 'username',]

admin.site.register(Users, CustomUserAdmin)

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
#
# from users.models import User
#
# admin.site.register(User, UserAdmin)
