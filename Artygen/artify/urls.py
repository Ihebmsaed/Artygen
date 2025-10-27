# artify/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.shortcuts import render


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', lambda request: render(request, 'Modified_Files/home.html'), name='home'),
    path('gallery/', include('gallery.urls')),  # Include gallery URLs
    path('feedback/', include('feedback.urls', namespace='feedback')), 
    path('blog/', include('blog.urls')),
    # Password reset paths
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile_photos/<path:path>/', serve, {'document_root': settings.PROFILE_PHOTOS_ROOT}, name='profile_photos'),  # Add this line
    path('events/', include('events.urls')),
    path('', include('events.urls')),  # Include the events app URLs
    path('events/', include('events.urls')),  # Ensure this line is correct
    path('artwork/', include('artwork.urls')),
    path('generate/', include('generator.urls')),


    #category URLs
    path('category/', include('category.urls')),
    path('subcategory/', include('category.urls')),


    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

