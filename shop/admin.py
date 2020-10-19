from django.contrib import admin
from .models import Comments, Procedures, Orders

from django import forms


class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedures
        fields = ('name', 'duration', 'price')


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    form = ProcedureForm


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('master', 'client', 'procedure', 'status', 'start_datetime', 'end_datetime')
    ordering = ('-start_datetime', )

admin.site.register(Procedures, ProcedureAdmin)
admin.site.register(Comments)
admin.site.register(Orders, OrdersAdmin)
# admin.site.register(ProcedureAdmin)
