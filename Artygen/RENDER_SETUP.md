# 🚀 Configuration Render - Guide Complet

## ✅ Variables d'environnement à ajouter sur Render

Allez sur: https://dashboard.render.com → Votre service "Artygen" → Environment

### Variables OBLIGATOIRES:

1. **SECRET_KEY** (déjà configuré par Render automatiquement)
2. **DEBUG** = `False`
3. **DATABASE_URL** (fourni automatiquement par Render)
4. **PYTHON_VERSION** = `3.11.0`

### Variables API (déjà configurées):

5. **GEMINI_API_KEY** = `votre-clé-gemini`
6. **API_KEY** = `votre-clé-gemini`
7. **HF_TOKEN** = `votre-token-huggingface`

### Variables CLOUDINARY (À AJOUTER):

8. **CLOUDINARY_CLOUD_NAME** = `dndkxukvc`
9. **CLOUDINARY_API_KEY** = `775151114658655`
10. **CLOUDINARY_API_SECRET** = `R0qagTNETRX004qijaBYTHLR_eg`

---

## 📋 Étapes pour ajouter les variables Cloudinary:

1. Connectez-vous à Render: https://dashboard.render.com
2. Cliquez sur votre service **Artygen**
3. Dans le menu à gauche, cliquez sur **Environment**
4. Cliquez sur **Add Environment Variable**
5. Ajoutez chaque variable une par une:
   - KEY: `CLOUDINARY_CLOUD_NAME` → VALUE: `dndkxukvc`
   - KEY: `CLOUDINARY_API_KEY` → VALUE: `775151114658655`
   - KEY: `CLOUDINARY_API_SECRET` → VALUE: `R0qagTNETRX004qijaBYTHLR_eg`
6. Cliquez sur **Save Changes**
7. Render va redéployer automatiquement (2-3 minutes)

---

## 🎯 Après le déploiement:

### Testez ces URLs:

1. **Page d'accueil**: https://artygen.onrender.com/
2. **Génération d'images**: https://artygen.onrender.com/generate/
3. **Inscription**: https://artygen.onrender.com/accounts/register/
4. **Connexion**: https://artygen.onrender.com/accounts/login/
5. **Blog**: https://artygen.onrender.com/blog/

### Fonctionnalités activées:

✅ Génération d'images AI avec Hugging Face FLUX.1-schnell
✅ Traduction automatique du blog (FR/EN/AR/ES) avec Google Gemini
✅ Analyse de sentiment des posts
✅ Stockage des images dans Cloudinary (cloud)
✅ Base de données PostgreSQL
✅ Fichiers statiques servis par WhiteNoise

---

## 🔍 En cas de problème:

### Vérifier les logs sur Render:

1. Allez dans votre service Artygen
2. Cliquez sur **Logs** dans le menu
3. Cherchez les erreurs (lignes en rouge)

### Erreurs communes:

- **"HF_TOKEN not configured"**: Ajoutez HF_TOKEN aux variables d'environnement
- **"Cloudinary not configured"**: Ajoutez les 3 variables CLOUDINARY_*
- **500 Internal Server Error**: Vérifiez les logs pour voir l'erreur exacte
- **Static files not loading**: Exécutez `python manage.py collectstatic` (déjà dans build.sh)

---

## 📸 Test de génération d'image:

1. Allez sur: https://artygen.onrender.com/generate/
2. Entrez un prompt (ex: "a beautiful sunset over mountains")
3. Choisissez un style (ex: "Realistic", "Abstract", "Digital Art")
4. Cliquez sur "Generate"
5. L'image sera générée et automatiquement uploadée sur Cloudinary
6. Vous pouvez sauvegarder l'artwork dans votre galerie

---

## 🌐 URLs importantes:

- **Site en production**: https://artygen.onrender.com
- **Dashboard Render**: https://dashboard.render.com
- **Dashboard Cloudinary**: https://console.cloudinary.com
- **Repository GitHub**: https://github.com/Ihebmsaed/Artygen

---

## ⚠️ IMPORTANT:

**N'utilisez JAMAIS localhost (127.0.0.1:8000) pour accéder au site déployé!**

Utilisez toujours: **https://artygen.onrender.com**

Le site est hébergé sur Render, pas sur votre ordinateur local.
