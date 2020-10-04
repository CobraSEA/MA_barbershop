from django.contrib import auth
from django.db import models
from django.forms import ModelForm
from django.urls import reverse


class NewUserForm(ModelForm):
    class Meta:
        # nic_name = models.CharField(max_length=20)
        model = auth.models.User
        # fields = "__all__"
        fields = ['username', 'password'
        , 'first_name', 'last_name', 'email']
        extra_fields = ['nic_name']
