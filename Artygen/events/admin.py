# events/admin.py
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'capacity')  # Customize fields to display in admin
    search_fields = ('title', 'location', 'event_type')  # Add searchable fields
