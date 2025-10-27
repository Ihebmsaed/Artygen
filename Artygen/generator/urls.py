from django.urls import path
from .views import generate_image, save_generated_artwork

urlpatterns = [
    path('', generate_image, name='generate_image'),
    path('save/', save_generated_artwork, name='save_generated_artwork'),
]
