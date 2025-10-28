"""
AI Event Description Generator
Uses Google Gemini to create engaging event descriptions in English
"""

import os
import google.generativeai as genai
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()


class EventDescriptionGenerator:
    """
    Generates personalized event descriptions based on event details using AI
    """

    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv("API_KEY") or getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            raise ValueError("API key not configured for event description generation")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def generate_description(self, title, event_type, location, date, capacity, creator_name='', tone='professional'):
        """
        Generate a personalized event description in English

        Args:
            title: Event title
            event_type: Type of event (e.g., "Exhibition", "Workshop", "Opening")
            location: Event location
            date: Event date and time (string format)
            capacity: Maximum capacity
            creator_name: Creator/Organizer name (optional)
            tone: Description tone ('professional', 'casual', 'creative')

        Returns:
            dict: {
                'description': str (generated description text),
                'success': bool,
                'error': str (if error)
            }
        """
        try:
            # Construire le prompt selon le ton souhaité
            if tone == 'professional':
                tone_instruction = "Professional and elegant tone, descriptive and informative"
            elif tone == 'casual':
                tone_instruction = "Casual and friendly tone, engaging and accessible"
            else:  # creative
                tone_instruction = "Creative and poetic tone, evocative and inspiring"

            # Prompt for Gemini
            prompt = f"""
You are an expert in writing descriptions for artistic events on an art platform called Artygen.

Create an engaging and attractive event description for this artistic event:

EVENT INFORMATION:
- Title: {title}
- Event Type: {event_type}
- Location: {location}
- Date and Time: {date}
- Capacity: {capacity} people
- Creator/Organizer: {creator_name if creator_name else "Not specified"}

INSTRUCTIONS:
1. Length: 100-200 words maximum
2. Language: English
3. {tone_instruction}
4. Highlight the artistic and creative aspect of the event
5. Naturally incorporate all provided details (title, type, location, date, capacity)
6. Create an inviting and exciting atmosphere
7. End with a clear invitation to participate
8. IMPORTANT: Do not invent false information or unprovided details
9. Remain authentic and credible
10. Adapt content according to event type (exhibition, workshop, opening, etc.)

STRUCTURE EXAMPLES:
- Catchy introduction with title and type
- Description of content and ambiance
- Practical details (location, date, capacity)
- Invitation to participate

Generate a unique and captivating description now:
"""

            # Call Gemini API
            response = self.model.generate_content(prompt)
            description_text = response.text.strip()

            # Clean the description (remove potential quotes)
            description_text = description_text.replace('"', '').replace("'", "'")

            return {
                'description': description_text,
                'success': True,
                'error': None
            }

        except Exception as e:
            print(f"❌ Error generating event description: {e}")
            return {
                'description': None,
                'success': False,
                'error': str(e)
            }

    def regenerate_description_with_different_tone(self, title, event_type, location, date, capacity, creator_name='', current_tone='professional'):
        """
        Regenerate description with different tones

        Returns:
            dict with 3 versions (professional, casual, creative)
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
    """Return a singleton instance of the event description generator"""
    global _event_description_generator_instance
    if _event_description_generator_instance is None:
        _event_description_generator_instance = EventDescriptionGenerator()
    return _event_description_generator_instance