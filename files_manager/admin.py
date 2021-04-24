from django.contrib import admin
from .models import *


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_filter = 'date_created',
    list_display = 'file_hash', 'date_created',
    search_fields = 'file',
    list_per_page = 50
