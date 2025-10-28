from django.urls import path
from . import views


urlpatterns = [
    path('', views.artwork_list, name='artwork_list'),
    path('all/', views.all_artworks, name='all_artworks'),  
    path('<int:pk>/', views.artwork_detail, name='artwork_detail'),
    path('public/<int:pk>/', views.artwork_public_detail, name='artwork_public_detail'),  # Vue pour tout le monde
    path('create/', views.artwork_create, name='artwork_create'),
    path('<int:pk>/edit/', views.artwork_update, name='artwork_update'),
    path('<int:pk>/delete/', views.artwork_delete, name='artwork_delete'),
    path('<int:artwork_id>/add-to-gallery/', views.add_to_gallery, name='add_to_gallery'),  # URL pour ajouter à la galerie
    path('galleries/', views.collection_list, name='collection_list'),  # This should point to your gallery_list view
    path('galleries/<int:gallery_id>/', views.collection_detail, name='collection_detail'),
    path('galleries/<int:gallery_id>/remove-artwork/<int:artwork_id>/', views.remove_artwork_from_gallery, name='remove_artwork_from_gallery'),
    path('gallery/delete/<int:gallery_id>/', views.collection_delete, name='collection_delete'),  # URL pour supprimer une galerie

]
