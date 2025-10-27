"""
Générateur de Bio de Profil par IA
Utilise Google Gemini pour créer des bios professionnelles
"""

import os
import google.generativeai as genai
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()


class BioGenerator:
    """
    Génère des bios de profil personnalisées basées sur les intérêts de l'utilisateur
    """
    
    def __init__(self):
        # Configuration de l'API Gemini
        api_key = os.getenv("API_KEY") or settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("API key not configured for bio generation")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_bio(self, username, first_name, last_name, art_style='', art_interests='', tone='professional', language='fr'):
        """
        Génère une bio de profil personnalisée
        
        Args:
            username: Nom d'utilisateur de l'artiste
            first_name: Prénom
            last_name: Nom de famille
            art_style: Style artistique (ex: "Peinture abstraite, Art digital")
            art_interests: Intérêts et mots-clés (ex: "nature, couleurs vives, émotions")
            tone: Ton de la bio ('professional', 'casual', 'creative')
            language: Langue de la bio ('fr', 'en')
        
        Returns:
            dict: {
                'bio': str (texte de la bio générée),
                'success': bool,
                'error': str (si erreur)
            }
        """
        try:
            # Préparer les informations
            full_name = f"{first_name} {last_name}".strip()
            
            # Construire le prompt selon le ton souhaité
            if tone == 'professional':
                tone_instruction = "Ton professionnel et élégant, à la 3ème personne"
            elif tone == 'casual':
                tone_instruction = "Ton décontracté et amical, à la 1ère personne"
            else:  # creative
                tone_instruction = "Ton créatif et poétique, style libre"
            
            # Prompt pour Gemini
            prompt = f"""
Tu es un expert en rédaction de bios professionnelles pour artistes sur une plateforme d'art nommée Artygen.

Crée une bio de profil engageante et professionnelle pour cet artiste:

INFORMATIONS DE L'ARTISTE:
- Nom d'artiste/Username: {username}
- Nom complet: {full_name}
- Style artistique: {art_style if art_style else "Non spécifié - à deviner selon les intérêts"}
- Intérêts et mots-clés: {art_interests if art_interests else "Artiste polyvalent"}

INSTRUCTIONS:
1. Longueur: 80-120 mots maximum
2. Langue: Français
3. {tone_instruction}
4. Mets en avant la passion et l'unicité de l'artiste
5. Incorpore naturellement le style et les intérêts mentionnés
6. Crée une connexion émotionnelle avec le lecteur
7. Termine par une note inspirante ou une invitation à découvrir les œuvres
8. IMPORTANT: Ne pas inventer de fausses informations (expositions, prix, etc.)
9. Reste authentique et crédible
10. Si peu d'informations sont fournies, reste sobre et élégant

EXEMPLES DE STRUCTURE:
- Pour un artiste avec beaucoup d'infos: Introduction → Style/Spécialité → Inspiration/Thèmes → Invitation
- Pour un artiste débutant: Passion → Exploration → Vision artistique → Bienvenue

Génère maintenant une bio unique et captivante:
"""

            # Appel à l'API Gemini
            response = self.model.generate_content(prompt)
            bio_text = response.text.strip()
            
            # Nettoyer la bio (enlever guillemets potentiels)
            bio_text = bio_text.replace('"', '').replace("'", "'")
            
            return {
                'bio': bio_text,
                'success': True,
                'error': None
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération de bio: {e}")
            return {
                'bio': None,
                'success': False,
                'error': str(e)
            }
    
    def regenerate_bio_with_different_tone(self, username, first_name, last_name, art_style='', art_interests='', current_tone='professional'):
        """
        Régénère une bio avec un ton différent
        
        Returns:
            dict avec 3 versions (professional, casual, creative)
        """
        tones = ['professional', 'casual', 'creative']
        bios = {}
        
        for tone in tones:
            if tone != current_tone:
                result = self.generate_bio(username, first_name, last_name, art_style, art_interests, tone=tone)
                if result['success']:
                    bios[tone] = result['bio']
        
        return bios


# Instance globale
_bio_generator_instance = None

def get_bio_generator():
    """Retourne une instance singleton du générateur de bio"""
    global _bio_generator_instance
    if _bio_generator_instance is None:
        _bio_generator_instance = BioGenerator()
    return _bio_generator_instance
