from django.contrib import admin
from .models import Comments, Procedures

from django import forms


class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedures
        fields = ('name', 'duration', 'price')


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    form = ProcedureForm


admin.site.register(Procedures, ProcedureAdmin)
admin.site.register(Comments)
# admin.site.register(ProcedureAdmin)
