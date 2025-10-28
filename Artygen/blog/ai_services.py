"""
Services IA pour le blog : Traduction et Analyse de Sentiment/Modération
"""
import os
import json
import re
from django.conf import settings
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configuration de l'API Gemini
def get_gemini_client():
    """Configure et retourne le client Gemini"""
    api_key = os.getenv("API_KEY") or settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("API key is not set in .env file or settings.py")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


class TranslationService:
    """Service de traduction multilingue avec Gemini"""
    
    SUPPORTED_LANGUAGES = {
        'fr': 'français',
        'en': 'anglais',
        'ar': 'arabe',
        'es': 'espagnol'
    }
    
    @staticmethod
    def translate_post(title, content, target_language='en', source_language='fr'):
        """
        Traduit le titre et le contenu d'un post
        
        Args:
            title: Titre du post
            content: Contenu du post
            target_language: Langue cible (en, fr, ar, es)
            source_language: Langue source (par défaut fr)
            
        Returns:
            dict: {'title': titre_traduit, 'content': contenu_traduit}
        """
        try:
            model = get_gemini_client()
            
            source_lang_name = TranslationService.SUPPORTED_LANGUAGES.get(source_language, 'français')
            target_lang_name = TranslationService.SUPPORTED_LANGUAGES.get(target_language, 'anglais')
            
            prompt = f"""Tu es un traducteur professionnel expert. Traduis le titre et le contenu suivants du {source_lang_name} vers le {target_lang_name}.
Garde le ton artistique et créatif du texte original. Réponds UNIQUEMENT au format JSON suivant, sans aucun texte supplémentaire :

{{
    "title": "titre traduit ici",
    "content": "contenu traduit ici"
}}

Titre original : {title}
Contenu original : {content}
"""
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Nettoyer la réponse pour extraire le JSON
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            # Parser le JSON
            result = json.loads(response_text)
            
            return {
                'title': result.get('title', title),
                'content': result.get('content', content)
            }
            
        except json.JSONDecodeError as e:
            print(f"Erreur de parsing JSON: {e}")
            print(f"Réponse reçue: {response_text}")
            # Fallback : retourner le texte original
            return {'title': title, 'content': content}
        except Exception as e:
            print(f"Erreur lors de la traduction: {e}")
            return {'title': title, 'content': content}
    
    @staticmethod
    def translate_to_all_languages(title, content, source_language='fr'):
        """
        Traduit un post dans toutes les langues supportées
        
        Returns:
            dict: Dictionnaire avec les traductions pour chaque langue
        """
        translations = {}
        
        for lang_code in TranslationService.SUPPORTED_LANGUAGES.keys():
            if lang_code != source_language:
                translation = TranslationService.translate_post(
                    title, content, 
                    target_language=lang_code, 
                    source_language=source_language
                )
                translations[f'title_{lang_code}'] = translation['title']
                translations[f'content_{lang_code}'] = translation['content']
            else:
                # Langue source - garder l'original
                translations[f'title_{lang_code}'] = title
                translations[f'content_{lang_code}'] = content
        
        return translations


class SentimentModerationService:
    """Service d'analyse de sentiment et de modération intelligente"""
    
    # Mots-clés inappropriés (peut être étendu)
    INAPPROPRIATE_KEYWORDS = [
        'violence', 'haine', 'discrimination', 'insulte', 'vulgaire',
        'spam', 'arnaque', 'scam', 'fake'
    ]
    
    @staticmethod
    def analyze_sentiment(text):
        """
        Analyse le sentiment d'un texte
        
        Returns:
            dict: {
                'score': float entre -1 (très négatif) et 1 (très positif),
                'label': 'positive', 'negative', ou 'neutral',
                'confidence': niveau de confiance
            }
        """
        try:
            model = get_gemini_client()
            
            prompt = f"""Analyse le sentiment du texte artistique suivant et détermine s'il est positif, négatif ou neutre.
Réponds UNIQUEMENT au format JSON suivant, sans aucun texte supplémentaire :

{{
    "score": [un nombre entre -1.0 (très négatif) et 1.0 (très positif)],
    "label": "[positive/negative/neutral]",
    "confidence": [un nombre entre 0.0 et 1.0],
    "explanation": "brève explication du sentiment détecté"
}}

Texte à analyser : {text}
"""
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Nettoyer la réponse
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            result = json.loads(response_text)
            
            return {
                'score': float(result.get('score', 0)),
                'label': result.get('label', 'neutral'),
                'confidence': float(result.get('confidence', 0.5)),
                'explanation': result.get('explanation', '')
            }
            
        except Exception as e:
            print(f"Erreur lors de l'analyse de sentiment: {e}")
            return {
                'score': 0.0,
                'label': 'neutral',
                'confidence': 0.0,
                'explanation': 'Analyse non disponible'
            }
    
    @staticmethod
    def moderate_content(text):
        """
        Modère le contenu pour détecter les contenus inappropriés
        
        Returns:
            dict: {
                'is_appropriate': bool,
                'confidence': float,
                'reason': str (si inapproprié),
                'categories': list of str (types de problèmes détectés)
            }
        """
        try:
            model = get_gemini_client()
            
            prompt = f"""Tu es un modérateur de contenu expert. Analyse le texte suivant et détermine s'il est approprié pour une plateforme artistique publique.
Vérifie la présence de :
- Violence explicite ou incitation à la violence
- Discours de haine, discrimination, racisme, sexisme
- Harcèlement ou intimidation
- Contenu sexuellement explicite inapproprié
- Spam ou arnaque
- Fausses informations dangereuses
- Langage vulgaire excessif

Réponds UNIQUEMENT au format JSON suivant, sans aucun texte supplémentaire :

{{
    "is_appropriate": [true/false],
    "confidence": [nombre entre 0.0 et 1.0],
    "reason": "explication si inapproprié, sinon chaine vide",
    "categories": ["liste des catégories de problèmes détectés"],
    "severity": "[low/medium/high/critical]"
}}

Texte à modérer : {text}
"""
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Nettoyer la réponse
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            result = json.loads(response_text)
            
            return {
                'is_appropriate': bool(result.get('is_appropriate', True)),
                'confidence': float(result.get('confidence', 0.5)),
                'reason': result.get('reason', ''),
                'categories': result.get('categories', []),
                'severity': result.get('severity', 'low')
            }
            
        except Exception as e:
            print(f"Erreur lors de la modération: {e}")
            # En cas d'erreur, considérer comme approprié par défaut
            return {
                'is_appropriate': True,
                'confidence': 0.0,
                'reason': '',
                'categories': [],
                'severity': 'low'
            }
    
    @staticmethod
    def analyze_and_moderate(text):
        """
        Combine l'analyse de sentiment et la modération
        
        Returns:
            dict: Résultats combinés des deux analyses
        """
        sentiment = SentimentModerationService.analyze_sentiment(text)
        moderation = SentimentModerationService.moderate_content(text)
        
        return {
            'sentiment': sentiment,
            'moderation': moderation
        }


def process_post_with_ai(post):
    """
    Traite un post avec toutes les fonctionnalités IA :
    - Traduction multilingue
    - Analyse de sentiment
    - Modération intelligente
    
    Args:
        post: Instance du modèle Post
        
    Returns:
        dict: Résultats de tous les traitements
    """
    from datetime import datetime
    
    # Combiner titre et contenu pour l'analyse
    full_text = f"{post.title}. {post.content}"
    
    # 1. Analyse de sentiment et modération
    analysis = SentimentModerationService.analyze_and_moderate(full_text)
    
    # Mettre à jour les champs de sentiment
    post.sentiment_score = analysis['sentiment']['score']
    post.sentiment_label = analysis['sentiment']['label']
    
    # Mettre à jour les champs de modération
    post.is_appropriate = analysis['moderation']['is_appropriate']
    if not analysis['moderation']['is_appropriate']:
        post.moderation_reason = analysis['moderation']['reason']
        post.moderation_date = datetime.now()
    
    # 2. Traduction multilingue
    translations = TranslationService.translate_to_all_languages(
        post.title, 
        post.content, 
        source_language=post.original_language
    )
    
    # Mettre à jour les champs de traduction
    for key, value in translations.items():
        setattr(post, key, value)
    
    # Sauvegarder le post
    post.save()
    
    return {
        'sentiment': analysis['sentiment'],
        'moderation': analysis['moderation'],
        'translations': translations
    }
