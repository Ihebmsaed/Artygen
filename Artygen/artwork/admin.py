from django.contrib import admin
from .models import Artwork
from .models import ArtCollection

admin.site.register(Artwork)
admin.site.register(ArtCollection)
