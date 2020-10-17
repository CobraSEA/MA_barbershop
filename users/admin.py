from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = User

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('username', 'first_name', 'last_name', 'nick_name',
                    'is_master', 'is_staff', 'is_active', 'gender', 'level')

admin.site.register(User, UserAdmin)