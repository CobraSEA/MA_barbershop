from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ModelForm
from django.urls import reverse


class NewUserForm(ModelForm):
    class Meta:
        model = get_user_model()
        # fields = "__all__"
        fields = ['username', 'password'
        , 'first_name', 'last_name', 'email']
