from django.contrib import admin
from django.forms import ModelChoiceField

from .models import Comments, Procedures, Orders, MasterProcedure
from users.models import User
from django import forms


class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedures
        fields = ('name', 'duration', 'price')


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    form = ProcedureForm


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('master', 'client', 'procedure', 'status', 'start_datetime', 'end_datetime', 'rate')
    ordering = ('-start_datetime', )


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'rate', 'insert_datetime')
    ordering = ('-insert_datetime', )


class MasterProcedureForm(forms.ModelForm):
    master = ModelChoiceField(queryset=User.objects.filter(is_master=True))

    class Meta:
        model = MasterProcedure
        fields = ['master', 'procedure']
        exclude = []


class MasterProcedureAdmin(admin.ModelAdmin):
    # master = admin.ModelAdmin.formfield_for_choice_field(queryset=User.objects.filter(is_master=True))
    form = MasterProcedureForm
    list_display = ('master', 'procedure')
    ordering = ('master', )


admin.site.register(MasterProcedure, MasterProcedureAdmin)
admin.site.register(Procedures, ProcedureAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Orders, OrdersAdmin)
# admin.site.register(ProcedureAdmin)
