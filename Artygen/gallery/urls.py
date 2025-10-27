# gallery/urls.py
from django.urls import path
from .views import gallery_list, gallery_create, gallery_update, gallery_delete,  my_galleries

urlpatterns = [
    path('', gallery_list, name='gallery_list'),
    path('create/', gallery_create, name='gallery_create'),
    path('update/<int:pk>/', gallery_update, name='gallery_update'),
    path('delete/<int:pk>/', gallery_delete, name='gallery_delete'),
    path('my-galleries/', my_galleries, name='my_galleries'),  # New URL pattern

]
