from django.contrib import admin
from .models import Feedback, Badge, UserBadge

# Register the Feedback model
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'artwork', 'rating', 'created_at')  # Fields to display in the list view
    search_fields = ('user__username', 'artwork__title', 'comment')  # Enable searching
    list_filter = ('created_at',)  # Add a filter by created_at date
    
    fieldsets = (
        (None, {
            'fields': ('user', 'artwork', 'comment', 'rating')
        }),
        ('Date Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    readonly_fields = ('created_at',)  # Make created_at read-only

# Register the Badge model
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'criteria')  # Fields to display in the list view
    search_fields = ('name',)  # Enable searching
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'criteria')
        }),
    )

# Register the UserBadge model
@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')  # Fields to display in the list view
    search_fields = ('user__username', 'badge__name')  # Enable searching
    
    fieldsets = (
        (None, {
            'fields': ('user', 'badge')
        }),
        ('Awarded Information', {
            'fields': ('awarded_at',),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    readonly_fields = ('awarded_at',)  # Make awarded_at read-only
