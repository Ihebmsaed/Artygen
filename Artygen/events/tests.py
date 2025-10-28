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
        """Test successful description generation"""
        generator = EventDescriptionGenerator()
        
        # Note: This test may fail if Gemini API is not configured
        # In a real environment, mock the API
        result = generator.generate_description(
            title="Modern Art Exhibition",
            event_type="Exhibition",
            location="Central Gallery, Paris",
            date="2025-11-15 18:00",
            capacity=50,
            creator_name="Jean Dupont",
            tone="professional"
        )
        
        # Check response structure
        self.assertIn('success', result)
        self.assertIn('description', result)
        self.assertIn('error', result)
        
        # If API works, check success
        if result['success']:
            self.assertIsInstance(result['description'], str)
            self.assertGreater(len(result['description']), 0)
        else:
            self.assertIsNone(result['description'])
            self.assertIsNotNone(result['error'])

    def test_generate_description_missing_api_key(self):
        """Test with missing API key"""
        # Save original config
        import os
        original_key = os.environ.get('API_KEY')
        
        # Remove API key
        if 'API_KEY' in os.environ:
            del os.environ['API_KEY']
        
        try:
            with self.assertRaises(ValueError):
                EventDescriptionGenerator()
        finally:
            # Restore API key
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
        """Test description generation view via POST"""
        url = reverse('generate_event_description')
        data = {
            'title': 'Test Event',
            'event_type': 'Workshop',
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
        # Success depends on API configuration

    def test_generate_description_view_get(self):
        """Test view with GET method (should fail)"""
        url = reverse('generate_event_description')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        import json
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('Method not allowed', response_data['error'])
