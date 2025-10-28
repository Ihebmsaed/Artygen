"""
Générateur de Descriptions d'Événements par IA
Utilise Google Gemini pour créer des descriptions d'événements engageantes
"""

import os
import google.generativeai as genai
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()


class EventDescriptionGenerator:
    """
    Génère des descriptions d'événements personnalisées basées sur les détails de l'événement
    """

    def __init__(self):
        # Configuration de l'API Gemini
        api_key = os.getenv("API_KEY") or getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            raise ValueError("API key not configured for event description generation")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def generate_description(self, title, event_type, location, date, capacity, creator_name='', tone='professional'):
        """
        Génère une description d'événement personnalisée

        Args:
            title: Titre de l'événement
            event_type: Type d'événement (ex: "Exposition", "Atelier", "Vernissage")
            location: Lieu de l'événement
            date: Date et heure de l'événement (format string)
            capacity: Capacité maximale
            creator_name: Nom du créateur (optionnel)
            tone: Ton de la description ('professional', 'casual', 'creative')
            language: Langue de la description ('fr', 'en')

        Returns:
            dict: {
                'description': str (texte de la description générée),
                'success': bool,
                'error': str (si erreur)
            }
        """
        try:
            # Construire le prompt selon le ton souhaité
            if tone == 'professional':
                tone_instruction = "Ton professionnel et élégant, descriptif et informatif"
            elif tone == 'casual':
                tone_instruction = "Ton décontracté et amical, engageant et accessible"
            else:  # creative
                tone_instruction = "Ton créatif et poétique, évocateur et inspirant"

            # Prompt pour Gemini
            prompt = f"""
Tu es un expert en rédaction de descriptions d'événements artistiques pour une plateforme d'art nommée Artygen.

Crée une description d'événement engageante et attrayante pour cet événement artistique :

INFORMATIONS DE L'ÉVÉNEMENT :
- Titre : {title}
- Type d'événement : {event_type}
- Lieu : {location}
- Date et heure : {date}
- Capacité : {capacity} personnes
- Créateur/Organisateur : {creator_name if creator_name else "Non spécifié"}

INSTRUCTIONS :
1. Longueur : 100-200 mots maximum
2. Langue : Français
3. {tone_instruction}
4. Mets en avant l'aspect artistique et créatif de l'événement
5. Incorpore naturellement tous les détails fournis (titre, type, lieu, date, capacité)
6. Crée une atmosphère invitante et excitante
7. Termine par une invitation claire à participer
8. IMPORTANT : Ne pas inventer de fausses informations ou détails non fournis
9. Reste authentique et crédible
10. Adapte le contenu selon le type d'événement (exposition, atelier, vernissage, etc.)

EXEMPLES DE STRUCTURE :
- Introduction accrocheuse avec le titre et le type
- Description du contenu et de l'ambiance
- Détails pratiques (lieu, date, capacité)
- Invitation à participer

Génère maintenant une description unique et captivante :
"""

            # Appel à l'API Gemini
            response = self.model.generate_content(prompt)
            description_text = response.text.strip()

            # Nettoyer la description (enlever guillemets potentiels)
            description_text = description_text.replace('"', '').replace("'", "'")

            return {
                'description': description_text,
                'success': True,
                'error': None
            }

        except Exception as e:
            print(f"❌ Erreur lors de la génération de description d'événement : {e}")
            return {
                'description': None,
                'success': False,
                'error': str(e)
            }

    def regenerate_description_with_different_tone(self, title, event_type, location, date, capacity, creator_name='', current_tone='professional'):
        """
        Régénère une description avec un ton différent

        Returns:
            dict avec 3 versions (professional, casual, creative)
        """
        tones = ['professional', 'casual', 'creative']
        descriptions = {}

        for tone in tones:
            if tone != current_tone:
                result = self.generate_description(title, event_type, location, date, capacity, creator_name, tone=tone)
                if result['success']:
                    descriptions[tone] = result['description']

        return descriptions


# Instance globale
_event_description_generator_instance = None

def get_event_description_generator():
    """Retourne une instance singleton du générateur de description d'événement"""
    global _event_description_generator_instance
    if _event_description_generator_instance is None:
        _event_description_generator_instance = EventDescriptionGenerator()
    return _event_description_generator_instance