# feedback/urls.py
from django.urls import path
from .views import submit_feedback ,feedback_list,user_badges,feedback_update,feedback_delete,recommendations_view # Assure-toi que cette vue est définie dans feedback/views.py
app_name = 'feedback'  # Ajoutez cette ligne

urlpatterns = [
    path('submit/', submit_feedback, name='submit_feedback'),  # Route pour soumettre le feedback
    path('feedbacks/', feedback_list, name='feedback_list'),
    path('user_badges/', user_badges, name='user_badges'),
    path('update/<int:id>/', feedback_update, name='feedback_update'),  # Chemin pour la mise à jour
    path('delete/<int:id>/', feedback_delete, name='feedback_delete'),  # Chemin pour la suppression
    path('recommendations/', recommendations_view, name='recommendations'),  # Ajoutez cette ligne

]
