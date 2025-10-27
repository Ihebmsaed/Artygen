from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from .views import PostListView, PostDetailView, PostCreateView, UserPostListView,edit_post,favouritesDeleteView,PostDetailViewBlog,PostDeleteView,add_comment,delete_comment,GenerateTextView,SuggestionView,UserFavouriteListView
urlpatterns = [ 
 
    path('', PostListView.as_view(),name="post-home"),
    path('post/<int:pk>/', PostDetailView.as_view(),name="post-detail"),
    path('post_Blog/<int:pk>/', PostDetailViewBlog.as_view(),name="post-detail-blog"),

    path('create/new', PostCreateView.as_view(),name="post-Create"),
    path('my-posts/', UserPostListView.as_view(), name="user-posts"),  # Nouvelle URL
    path('post/edit/<int:post_id>/', edit_post, name='edit-post'),  # Ajoutez cette ligne
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    # Ajoutez ces lignes pour les likes et dislikes
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('generate-text/', GenerateTextView.as_view(), name='generate-text'),
    path('suggestions/', SuggestionView.as_view(), name='suggestions'),
    path('save_to_favourites/<int:post_id>/', views.save_to_favourites, name='save_to_favourites'),
    path('favourites/', UserFavouriteListView.as_view(), name='favourites'),
    path('favourites/delete/<int:pk>/', favouritesDeleteView.as_view(), name='favourite-delete'),




] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)