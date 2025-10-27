# Configuration de l'API Hugging Face pour la génération d'images

## Problème actuel
Le token Hugging Face actuel est invalide ou expiré, ce qui empêche la génération d'images.

## Solution : Obtenir un nouveau token Hugging Face

### Étape 1 : Créer un compte Hugging Face
1. Allez sur : https://huggingface.co/join
2. Créez un compte gratuit (ou connectez-vous si vous en avez déjà un)

### Étape 2 : Générer un token API
1. Allez sur : https://huggingface.co/settings/tokens
2. Cliquez sur "New token"
3. Donnez-lui un nom (ex: "Artygen-Generator")
4. Sélectionnez le type : **"Read"** (suffisant pour la génération d'images)
5. Cliquez sur "Generate token"
6. **COPIEZ le token immédiatement** (vous ne pourrez plus le voir après)

### Étape 3 : Ajouter le token dans votre projet

Ouvrez le fichier `.env` et ajoutez cette ligne :

```env
HF_TOKEN=votre_token_ici
```

Exemple :
```env
API_KEY=AIzaSyDRyS1gBkkiauaY75GvzGdu0iubNzwXjm0
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Étape 4 : Redémarrer le serveur
```powershell
python manage.py runserver
```

## Modèles disponibles

Le projet est configuré pour utiliser :
- **runwayml/stable-diffusion-v1-5** : Modèle principal (recommandé)

Si vous rencontrez des problèmes, vous pouvez essayer d'autres modèles :
- `stabilityai/stable-diffusion-2-1`
- `CompVis/stable-diffusion-v1-4`

Pour changer de modèle, modifiez `API_URL` dans `generator/views.py`.

## Vérifier que votre token fonctionne

Exécutez cette commande dans un terminal :

```powershell
python -c "import requests; headers = {'Authorization': 'Bearer VOTRE_TOKEN'}; response = requests.post('https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5', headers=headers, json={'inputs': 'a cat'}); print('Status:', response.status_code)"
```

Si vous voyez "Status: 200" ou "Status: 503" (modèle en chargement), le token fonctionne!

## Limites de l'API gratuite Hugging Face

- **Requêtes** : Limitées mais généreuses pour un usage personnel
- **Temps de chargement** : Le modèle peut mettre ~20-30 secondes à se charger la première fois
- **Taille des images** : Images générées en 512x512 pixels

## Alternative : Utiliser l'API Gemini pour la génération d'images

Google Gemini peut aussi générer des images. Si Hugging Face ne fonctionne pas, contactez-moi pour configurer Gemini.

## Support

En cas de problème :
- Token invalide : Créez un nouveau token sur Hugging Face
- Modèle ne charge pas : Attendez 30 secondes et réessayez
- Erreur 404 : Le modèle n'existe plus, changez de modèle dans le code
