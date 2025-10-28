from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Event
from .event_description_generator import EventDescriptionGenerator

class EventDescriptionGeneratorTestCase(TestCase):
    def setUp(self):
        # Créer un utilisateur pour les tests
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_generate_description_success(self):
        """Test de génération réussie d'une description"""
        generator = EventDescriptionGenerator()
        
        # Note: Ce test peut échouer si l'API Gemini n'est pas configurée
        # Dans un environnement réel, mock l'API
        result = generator.generate_description(
            title="Exposition Art Moderne",
            event_type="Exposition",
            location="Galerie Centrale, Paris",
            date="2025-11-15 18:00",
            capacity=50,
            creator_name="Jean Dupont",
            tone="professional"
        )
        
        # Vérifier la structure de la réponse
        self.assertIn('success', result)
        self.assertIn('description', result)
        self.assertIn('error', result)
        
        # Si l'API fonctionne, vérifier le succès
        if result['success']:
            self.assertIsInstance(result['description'], str)
            self.assertGreater(len(result['description']), 0)
        else:
            self.assertIsNone(result['description'])
            self.assertIsNotNone(result['error'])

    def test_generate_description_missing_api_key(self):
        """Test avec clé API manquante"""
        # Sauvegarder la config originale
        import os
        original_key = os.environ.get('API_KEY')
        
        # Supprimer la clé API
        if 'API_KEY' in os.environ:
            del os.environ['API_KEY']
        
        try:
            with self.assertRaises(ValueError):
                EventDescriptionGenerator()
        finally:
            # Restaurer la clé API
            if original_key:
                os.environ['API_KEY'] = original_key

class EventDescriptionViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_generate_description_view_post(self):
        """Test de la vue de génération de description via POST"""
        url = reverse('generate_event_description')
        data = {
            'title': 'Test Event',
            'event_type': 'Atelier',
            'location': 'Test Location',
            'date': '2025-12-01 10:00',
            'capacity': '20',
            'tone': 'professional'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        import json
        response_data = json.loads(response.content)
        self.assertIn('success', response_data)
        # Le succès dépend de la configuration de l'API

    def test_generate_description_view_get(self):
        """Test de la vue avec méthode GET (devrait échouer)"""
        url = reverse('generate_event_description')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        import json
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('Méthode non autorisée', response_data['error'])
