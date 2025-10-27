from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category-list'),
    path('categories/new/', views.category_create, name='category-create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category-update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),
    path('subcategories/<int:category_id>/', views.subcategory_list, name='subcategory-list'),


    path('categories/<int:category_id>/subcategories/', views.subcategory_list, name='subcategory-list'),
    path('categories/<int:category_id>/subcategories/create/', views.subcategory_create, name='subcategory-create'),
    path('categories/<int:category_id>/subcategories/update/<int:pk>/', views.subcategory_update, name='subcategory-update'),
    path('categories/<int:category_id>/subcategories/delete/<int:pk>/', views.subcategory_delete, name='subcategory-delete'),
    path('categories/<int:category_id>/subcategories/generate/', views.generate_subcategories, name='subcategory-generate'),
    path('categories/<int:category_id>/subcategories/get_art_subcategories/', views.get_art_subcategories, name='get_art_subcategories'),




]
