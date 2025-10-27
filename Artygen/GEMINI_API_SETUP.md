# Configuration de l'API Google Gemini

## Problème actuel
Erreur 429 : Le quota de l'API Google Gemini a été dépassé (quota_limit_value: 0).

## Solutions

### Option 1 : Obtenir une nouvelle clé API Google Gemini (RECOMMANDÉ)

1. **Visitez Google AI Studio** :
   - Allez sur : https://makersuite.google.com/app/apikey
   - OU : https://aistudio.google.com/app/apikey

2. **Créez une nouvelle clé API** :
   - Connectez-vous avec votre compte Google
   - Cliquez sur "Create API Key"
   - Choisissez un projet existant ou créez-en un nouveau
   - Copiez la clé API générée

3. **Mettez à jour votre fichier .env** :
   ```
   API_KEY=VOTRE_NOUVELLE_CLE_API_ICI
   ```

4. **Redémarrez le serveur Django** :
   ```powershell
   python manage.py runserver
   ```

### Option 2 : Activer la facturation sur Google Cloud

Si vous souhaitez augmenter les quotas :

1. Allez sur : https://console.cloud.google.com/
2. Sélectionnez votre projet (project_number: 606110160548)
3. Activez la facturation pour augmenter les limites de quota
4. Configurez les quotas dans "APIs & Services" > "Quotas"

### Option 3 : Utiliser une API alternative temporairement

Vous pouvez modifier le code pour utiliser OpenAI à la place :

1. Obtenez une clé API OpenAI : https://platform.openai.com/api-keys
2. Modifiez le code dans `blog/views.py` pour utiliser OpenAI au lieu de Gemini

### Option 4 : Attendre le renouvellement du quota

Les quotas gratuits de Google Gemini se renouvellent :
- Par minute : attendez 1 minute
- Par jour : attendez jusqu'au lendemain (UTC)

## Vérification de la clé API actuelle

La clé API actuelle dans `.env` :
```
API_KEY=AIzaSyBcXW88FxInvkjf98C5jjDpxzIufDvthtc
```

La clé API dans `settings.py` :
```
GEMINI_API_KEY=AIzaSyDRys-PkwoyPksHIGM0AO8XMYhqrYcZIQI
```

## Test de l'API

Pour tester si votre clé API fonctionne :

```python
import google.generativeai as genai

genai.configure(api_key="VOTRE_CLE_API")
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Bonjour")
print(response.text)
```

## Limites du quota gratuit de Google Gemini

- **Gratuit** : 15 requêtes par minute, 1500 requêtes par jour
- **Payant** : Quotas beaucoup plus élevés selon votre plan

## Support

Pour demander une augmentation de quota :
https://cloud.google.com/docs/quotas/help/request_increase
