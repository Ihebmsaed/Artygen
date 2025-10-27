from django.urls import path
from .views import EventListView, EventDetailView, event_create, event_update, event_delete
from . import views

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('create/', event_create, name='event_create'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),  # This should be 'event_detail'
    path('<int:pk>/update/', event_update, name='event_update'),
    path('<int:pk>/delete/', event_delete, name='event_delete'),
    path('my-events/', views.my_events_view, name='my_events'),

]
