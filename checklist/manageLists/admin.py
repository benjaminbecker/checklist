from django.contrib import admin

# Register your models here.
from .models import Checklist, ChecklistItem
admin.site.register(Checklist)
admin.site.register(ChecklistItem)
