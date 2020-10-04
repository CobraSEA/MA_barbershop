from django.contrib import admin
from .models import masters, procedures

admin.site.register(masters)
admin.site.register(procedures)
# admin.site.register(clients)