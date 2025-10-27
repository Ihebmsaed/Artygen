# feedback/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Feedback, Artwork, UserBadge, Badge
from .forms import FeedbackForm
from django.db import models
from django.contrib.auth.models import User  # Ajoute ceci si ce n'est pas déjà présent
import pandas as pd
from artwork.models import Artwork  # Assurez-vous que cela correspond à l'emplacement de votre modèle Artwork
from django.contrib.auth.decorators import login_required
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render

def calculate_recommendations(feedback_df):
    if feedback_df.empty or 'user_id' not in feedback_df.columns or 'rating' not in feedback_df.columns:
        print("Le DataFrame est vide ou manque des colonnes nécessaires.")
        return pd.DataFrame()  # Retourne un DataFrame vide si aucune donnée

    # Calcul des recommandations
    recommendations = feedback_df.groupby('user_id')['rating'].mean().reset_index()
    recommendations = recommendations.sort_values(by='rating', ascending=False)

    # Merge avec le DataFrame original pour inclure les titres
    recommendations = recommendations.merge(feedback_df[['user_id', 'artwork_id', 'artwork__title']], on='user_id', how='left').drop_duplicates()

    return recommendations.head(5)



def recommendations_view(request):
    feedbacks, average_rating_results = collect_feedbacks()  # Assure-toi que cette fonction retourne les feedbacks

    if feedbacks:
        # Convertir en DataFrame
        df = pd.DataFrame(feedbacks)

        # Afficher les colonnes pour le débogage
        print("Colonnes du DataFrame:", df.columns.tolist())  # Utilise .tolist() pour obtenir une liste
        print("Premières lignes du DataFrame:", df.head())

        # Calculer les recommandations
        recommendations = calculate_recommendations(df)

        if recommendations.empty:
            context = {'message': 'Aucune recommandation disponible.'}
        else:
            context = {'recommendations': recommendations.to_dict(orient='records')}
    else:
        context = {'message': 'Aucun feedback trouvé.'}

    return render(request, 'feedback/recommendations.html', 
                  {'feedbacks': feedbacks,          
                   'average_ratings': average_rating_results})  # Met à jour le nom ici


def get_recommendations(user_id, user_item_matrix, similarity_matrix, n_recommendations=5):
    user_index = user_item_matrix.index.get_loc(user_id)
    similar_users = similarity_matrix[user_index]
    
    # Trouver les indices des œuvres déjà notées par l'utilisateur
    rated_items = user_item_matrix.columns[user_item_matrix.loc[user_id] > 0]
    
    # Calculer les scores de recommandations
    scores = similar_users.dot(user_item_matrix) / similar_users.sum()
    
    # Exclure les œuvres déjà notées
    scores = scores[~scores.index.isin(rated_items)]
    
    return scores.nlargest(n_recommendations)

def calculate_similarity(matrix):
    similarity = cosine_similarity(matrix)
    return similarity
def collect_feedbacks():
    # Récupérer tous les feedbacks de la base de données, y compris les titres des œuvres
    feedbacks = Feedback.objects.select_related('artwork_id').values('user_id', 'artwork_id', 'rating', 'artwork__title')

    # Convertir les feedbacks en DataFrame
    df = pd.DataFrame(feedbacks)

    # Vérifier les colonnes
    print(f"Colonnes du DataFrame: {df.columns.tolist()}")
    print(f"Premières lignes du DataFrame: {df.head()}")

    # Identifier les doublons
    duplicates = df.groupby(['user_id', 'artwork_id']).filter(lambda x: len(x) > 1)
    
    if not duplicates.empty:
        print("Duplicate feedback entries found:")
        for _, duplicate in duplicates.iterrows():
            print(f"User ID: {duplicate['user_id']}, Artwork ID: {duplicate['artwork_id']}")

    # Calculer la moyenne pour chaque artwork_id
    average_ratings = df.groupby('artwork_id')['rating'].mean().reset_index()
    # Arrondir les moyennes à l'entier le plus proche
    average_ratings['rating'] = average_ratings['rating'].apply(lambda x: round(x))

    # Créer une liste pour les résultats des moyennes des ratings
    average_rating_results = []
    for _, row in average_ratings.iterrows():
        artwork_id = row['artwork_id']
        avg_rating = row['rating']
        average_rating_results.append({'artwork_id': artwork_id, 'avg_rating': avg_rating})

    return feedbacks, average_rating_results


def create_user_item_matrix(feedbacks):
    df = pd.DataFrame(list(feedbacks))
    
    # Vérifie que le DataFrame contient les colonnes attendues
    print("DataFrame après création:", df)

    if 'user_id' not in df.columns or 'artwork_id' not in df.columns or 'rating' not in df.columns:
        print("Le DataFrame ne contient pas les colonnes nécessaires.")
        return pd.DataFrame()  # Retourne un DataFrame vide si aucune donnée

    # Pivot pour créer la matrice utilisateur-oeuvre
    user_item_matrix = df.pivot(index='user_id', columns='artwork_id', values='rating').fillna(0)
    return user_item_matrix


@login_required
def submit_feedback(request):
    artworks = Artwork.objects.all()  # Retrieve all artworks for dropdown

    if request.method == 'POST':
        # Get the artwork based on the selected title
        artwork_id = request.POST.get('artwork_id')
        artwork = Artwork.objects.get(id=artwork_id)

        # Create and save a new Feedback instance
        feedback = Feedback(
            user=request.user,
            artwork=artwork,
            comment=request.POST['comment'],
            rating=request.POST['rating']
        )
        feedback.save()

        # Badge awarding logic
        feedback_count = Feedback.objects.filter(user=request.user).count()
        badges = Badge.objects.filter(criteria__lte=feedback_count)
        for badge in badges:
            if not UserBadge.objects.filter(user=request.user, badge=badge).exists():
                UserBadge.objects.create(user=request.user, badge=badge)

        return redirect('feedback:feedback_list')

    return render(request, 'feedback/submit_feedback.html', {'artworks': artworks})
    
def feedback_update(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('feedback:feedback_list')  # Correct redirection to feedback list
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedback/feedback_form.html', {'form': form})

# Vue pour supprimer un feedback
def feedback_delete(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == 'POST':
        feedback.delete()
        return redirect('feedback:feedback_list')  # Correct redirection to feedback list

    return render(request, 'feedback/feedback_confirm_delete.html', {'feedback': feedback})

def assign_badges_to_user(user):
    feedback_count = Feedback.objects.filter(user=user).count()
    print(f"Feedback count for {user.username}: {feedback_count}")

    badges = Badge.objects.filter(criteria__lte=feedback_count)
    print(f"Badges eligible for {user.username}: {[badge.name for badge in badges]}")

    for badge in badges:
        if not UserBadge.objects.filter(user=user, badge=badge).exists():
            UserBadge.objects.create(user=user, badge=badge)
            print(f"Badge '{badge.name}' awarded to {user.username}")
        else:
            print(f"Badge '{badge.name}' already awarded to {user.username}")  # Ajoutez cette ligne

@login_required
def feedback_list(request):
    # Retrieve all feedbacks
    feedbacks = Feedback.objects.all()

    # Count the number of feedbacks for the logged-in user
    feedback_count = Feedback.objects.filter(user=request.user).count()
    print(f"Feedback count for {request.user.username}: {feedback_count}")

    # Check and assign badges to the user
    assign_badges_to_user(request.user)

    # Find badges eligible for the logged-in user
    badges = Badge.objects.filter(criteria__lte=feedback_count)
    print(f"Badges eligible for {request.user.username}: {[badge.name for badge in badges]}")

    # Create a list for badges to display
    user_badges = UserBadge.objects.filter(user=request.user)

    # Replace IDs with titles in the feedbacks
    feedbacks_with_titles = []
    for feedback in feedbacks:
        # Safely access the artwork's title, handling cases where artwork does not exist
        try:
            artwork = feedback.artwork  # This will use the reverse relationship
            artwork_title = artwork.title
        except Artwork.DoesNotExist:
            artwork_title = "Artwork not available"

        feedbacks_with_titles.append({
            'id': feedback.id,
            'artwork_title': artwork_title,
            'comment': feedback.comment,
            'rating': feedback.rating,
        })

    return render(request, 'feedback/feedback_list.html', {
        'feedbacks': feedbacks_with_titles,
        'user_badges': user_badges,
    })

 
@login_required
def user_badges(request):
    # Récupérer tous les utilisateurs et leurs badges
    users = User.objects.all()
    user_badges = {user: UserBadge.objects.filter(user=user) for user in users}
    
    return render(request, 'feedback/user_badges.html', {'user_badges': user_badges})





















"""

def submit_feedback(request, artwork_id):
    # Récupérer l'œuvre d'art sélectionnée
    artwork = Artwork.objects.get(id=artwork_id)

    if request.method == 'POST':
        # Créer un nouvel objet Feedback
        feedback = Feedback(
            user=request.user,
            artwork=artwork,
            comment=request.POST['comment'],
            rating=request.POST['rating']
        )
        feedback.save()  # Enregistrer le feedback dans la base de données

        # Vérifier si l'utilisateur a atteint le nombre requis de feedbacks pour un badge
        feedback_count = Feedback.objects.filter(user=request.user).count()
        badges = Badge.objects.filter(criteria__lte=feedback_count)

        # Attribuer des badges à l'utilisateur
        for badge in badges:
            # Vérifiez si l'utilisateur a déjà reçu ce badge
            if not UserBadge.objects.filter(user=request.user, badge=badge).exists():
                UserBadge.objects.create(user=request.user, badge=badge)

        return redirect('feedback:feedback_list')  # Rediriger vers la liste des feedbacks après la soumission

    # Rendre le template avec le titre de l'œuvre d'art
    return render(request, 'feedback/submit_feedback.html', {'artwork': artwork})
"""
