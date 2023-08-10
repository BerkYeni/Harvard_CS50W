from django.contrib import admin
from .models import Entry

# Register your models here.
class EntryAdmin(admin.ModelAdmin):
  pass


admin.site.register(Entry, EntryAdmin)