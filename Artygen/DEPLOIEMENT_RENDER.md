# 🚀 Guide de Déploiement sur Render

## 📋 Fichiers Créés pour le Déploiement

✅ **Fichiers de configuration ajoutés** :
- `build.sh` - Script de build pour Render
- `render.yaml` - Configuration du service Render
- `runtime.txt` - Version de Python
- `.env.example` - Template des variables d'environnement
- `requirements.txt` - Mis à jour avec les dépendances production

✅ **Modifications de settings.py** :
- Configuration de la base de données PostgreSQL
- Configuration WhiteNoise pour les fichiers statiques
- Variables d'environnement pour la sécurité
- Configuration ALLOWED_HOSTS

---

## 🔧 Étape 1 : Préparer le Repository Git

### 1.1 Vérifier que les secrets ne sont pas dans Git

```powershell
# Vérifier le .gitignore
cat .gitignore

# S'assurer que ces fichiers sont ignorés :
# - secrets_config.py
# - .env
# - db.sqlite3
```

### 1.2 Commit et Push

```powershell
# Ajouter les nouveaux fichiers
git add build.sh render.yaml runtime.txt .env.example requirements.txt
git add artify/settings.py .gitignore

# Commit
git commit -m "🚀 Configure project for Render deployment"

# Push vers GitHub
git push origin integration-v1
```

---

## 🌐 Étape 2 : Créer un Compte Render

1. **Allez sur** : https://render.com
2. **Sign Up** avec GitHub
3. **Autorisez** Render à accéder à votre repository GitHub

---

## 🗄️ Étape 3 : Créer une Base de Données PostgreSQL

1. Dans Render Dashboard, cliquez sur **"New +"**
2. Sélectionnez **"PostgreSQL"**
3. Configurez :
   - **Name** : `artygen-db`
   - **Database** : `artygen`
   - **User** : `artygen`
   - **Region** : Choisissez le plus proche (Europe/Frankfurt)
   - **Plan** : Free (pour commencer)
4. Cliquez sur **"Create Database"**
5. **📝 IMPORTANT** : Copiez l'**Internal Database URL** (vous en aurez besoin)

---

## 🌐 Étape 4 : Créer le Web Service

1. Dans Render Dashboard, cliquez sur **"New +"**
2. Sélectionnez **"Web Service"**
3. Connectez votre repository GitHub **"Artygen"**
4. Configurez :

### Configuration de Base

```
Name: artygen
Region: Frankfurt (EU Central)
Branch: integration-v1
Root Directory: (laisser vide)
Runtime: Python 3
Build Command: ./build.sh
Start Command: gunicorn artify.wsgi:application
```

### Plan
- Sélectionnez **"Free"** pour commencer

---

## 🔑 Étape 5 : Configurer les Variables d'Environnement

Dans la section **"Environment"**, ajoutez ces variables :

### Variables Requises

| Variable | Valeur | Note |
|----------|--------|------|
| `PYTHON_VERSION` | `3.11.0` | Version de Python |
| `SECRET_KEY` | `[AUTO-GÉNÉRÉ]` | Cliquez sur "Generate" |
| `DEBUG` | `False` | Mode production |
| `DATABASE_URL` | `[COPIÉ DE LA DB]` | Internal Database URL de l'étape 3 |
| `GEMINI_API_KEY` | `votre-clé-gemini` | Votre clé API Gemini |
| `API_KEY` | `votre-clé-gemini` | Même que GEMINI_API_KEY |
| `HF_TOKEN` | `votre-token-huggingface` | Votre token Hugging Face |

### Comment Ajouter les Variables

```
1. Cliquez sur "Add Environment Variable"
2. Key: PYTHON_VERSION
   Value: 3.11.0
3. Cliquez sur "Add"
4. Répétez pour chaque variable
```

### ⚠️ IMPORTANT : Vos Clés API

```
GEMINI_API_KEY : Obtenez-en une sur https://makersuite.google.com/app/apikey
HF_TOKEN : Obtenez-en un sur https://huggingface.co/settings/tokens
```

---

## 🚀 Étape 6 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Render va automatiquement :
   - 📥 Cloner votre repository
   - 📦 Installer les dépendances (`pip install -r requirements.txt`)
   - 🔨 Exécuter `build.sh` :
     - Collecter les fichiers statiques
     - Exécuter les migrations
   - ▶️ Démarrer l'application avec Gunicorn

3. **Surveillez les logs** en temps réel dans l'interface Render

---

## ✅ Étape 7 : Vérifier le Déploiement

### 7.1 Attendre la Fin du Build

```
Logs typiques :
==> Cloning from https://github.com/Ihebmsaed/Artygen...
==> Installing dependencies
==> Running build command: ./build.sh
==> Collecting static files
==> Running migrations
==> Starting service
```

### 7.2 Accéder à Votre Site

Votre URL sera :
```
https://artygen.onrender.com
```

### 7.3 Créer un Superutilisateur

Dans Render Dashboard :
1. Allez dans votre service
2. Cliquez sur **"Shell"** (en haut à droite)
3. Exécutez :

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer votre compte admin.

---

## 🔧 Configuration Post-Déploiement

### 1. Accéder à l'Admin Django

```
https://artygen.onrender.com/admin/
```

### 2. Tester les Fonctionnalités

- ✅ Page d'accueil
- ✅ Inscription/Connexion
- ✅ Création de posts
- ✅ Générateur d'images IA
- ✅ Traduction de posts
- ✅ Upload d'images

### 3. Configurer un Domaine Personnalisé (Optionnel)

1. Dans Render Dashboard → Settings
2. Section "Custom Domain"
3. Ajoutez votre domaine

---

## 📊 Surveillance et Logs

### Voir les Logs en Temps Réel

1. Dans Render Dashboard
2. Votre service → **"Logs"**
3. Surveillez les erreurs/avertissements

### Logs Utiles

```bash
# Logs d'application
[INFO] Starting gunicorn
[INFO] Listening at: http://0.0.0.0:10000

# Logs Django
[INFO] "GET / HTTP/1.1" 200
[INFO] "POST /blog/create/ HTTP/1.1" 302
```

---

## 🐛 Dépannage

### Erreur 1 : Build Fails

```
Solution:
- Vérifiez requirements.txt
- Vérifiez que build.sh est exécutable
- Vérifiez les logs de build
```

### Erreur 2 : Database Connection Error

```
Solution:
- Vérifiez que DATABASE_URL est correct
- Vérifiez que la base de données est créée
- Essayez de re-run les migrations dans le Shell
```

### Erreur 3 : Static Files 404

```
Solution:
- Vérifiez STATIC_ROOT dans settings.py
- Re-run: python manage.py collectstatic
- Vérifiez WhiteNoise middleware
```

### Erreur 4 : Internal Server Error (500)

```
Solution:
1. Activez temporairement DEBUG=True
2. Vérifiez les logs Render
3. Vérifiez les variables d'environnement
4. Re-désactivez DEBUG après diagnostic
```

---

## 🔄 Mises à Jour et Redéploiement

### Déploiement Automatique

Render redéploie automatiquement quand vous push sur GitHub :

```powershell
# Faire des modifications
git add .
git commit -m "Update feature"
git push origin integration-v1

# Render détecte le push et redéploie automatiquement
```

### Redéploiement Manuel

1. Dans Render Dashboard
2. Votre service → **"Manual Deploy"**
3. Cliquez sur **"Deploy latest commit"**

---

## 💰 Plans et Tarifs

### Plan Free (Gratuit)
- ✅ 750 heures/mois
- ✅ PostgreSQL 256 MB
- ❌ Se met en veille après 15 min d'inactivité
- ⏱️ Temps de réveil : ~1 minute

### Plan Starter ($7/mois)
- ✅ Toujours actif
- ✅ Plus de ressources
- ✅ PostgreSQL 1 GB

---

## 📝 Checklist Finale

Avant de considérer le déploiement comme terminé :

- [ ] ✅ Site accessible sur l'URL Render
- [ ] ✅ Page d'accueil charge correctement
- [ ] ✅ Inscription/Connexion fonctionne
- [ ] ✅ CSS/JS charge correctement
- [ ] ✅ Images s'uploadent
- [ ] ✅ Génération d'images IA fonctionne
- [ ] ✅ Traduction de posts fonctionne
- [ ] ✅ Admin Django accessible
- [ ] ✅ Variables d'environnement configurées
- [ ] ✅ Base de données fonctionnelle

---

## 🎉 Félicitations !

Votre site **Artygen** est maintenant en ligne sur Render !

**URL de production** : `https://artygen.onrender.com`

### Prochaines Étapes

1. **Ajouter un domaine personnalisé** (optionnel)
2. **Configurer les emails** (SMTP)
3. **Mettre en place un CDN** pour les médias (Cloudinary)
4. **Configurer le monitoring** (Sentry)
5. **Optimiser les performances**

---

## 📞 Support

### Documentation Render
- https://render.com/docs/deploy-django

### En Cas de Problème
1. Vérifiez les logs Render
2. Consultez la doc Django
3. Vérifiez les variables d'environnement
4. Testez en local d'abord

**Votre site est prêt pour le monde ! 🌍**
