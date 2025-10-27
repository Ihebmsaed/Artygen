from django.contrib import admin
from .models import Category,Subcategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'updated_at']
    search_fields = ['name']

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1  # Number of blank forms for subcategory creation

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')