# Guide d'implémentation du système de modals et toasts
## Pour toutes les pages du projet Artygen

### ✅ Modifications déjà effectuées :

1. **Fichiers créés (réutilisables partout) :**
   - `/static/js/modal-handler.js` - Gestion des toasts et validation
   - `/static/css/custom-forms.css` - Styles des modals et formulaires
   - `/static/templates/modal_base.html` - Template modal réutilisable
   - `/static/templates/messages.html` - Template messages Django
   - `/static/templates/global_includes.html` - Includes globaux

2. **Pages déjà modifiées :**
   - ✅ `artwork/templates/artwork/artwork_list.html` - Modal d'ajout complet
   - ✅ `blog/templates/Blog/blog.html` - Modal amélioré avec validation
   - ✅ `artwork/templates/artwork/gallery_list.html` - Modal de collection
   - ✅ `category/templates/subcategory_list.html` - Modals et validation

### 📋 Instructions pour appliquer aux autres pages :

#### Étape 1 : Dans le `<head>` de chaque page HTML

Ajoutez après les imports Bootstrap existants :

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/custom-forms.css' %}">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
```

#### Étape 2 : Avant la fermeture `</body>`

Ajoutez les scripts et messages :

```html
<!-- Messages Django pour toasts -->
{% if messages %}
    {% for message in messages %}
        <div class="django-message" data-type="{% if 'success' in message.tags %}success{% elif 'error' in message.tags %}error{% elif 'warning' in message.tags %}warning{% else %}info{% endif %}" style="display: none;">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
<script src="{% static 'js/modal-handler.js' %}"></script>

<script>
function handleFormSubmit(event, form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.classList.add('btn-loading');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
}

// Auto-resize textarea
document.querySelectorAll('.auto-resize').forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
});
</script>
```

#### Étape 3 : Remplacer les liens de formulaire par des boutons modal

Au lieu de :
```html
<a href="{% url 'event_create' %}" class="btn btn-primary">Create Event</a>
```

Utilisez :
```html
<button type="button" class="btn btn-custom-primary" data-toggle="modal" data-target="#createEventModal">
    <i class="fas fa-plus-circle"></i> Create Event
</button>
```

#### Étape 4 : Structure de modal à ajouter

```html
<!-- Modal pour créer un [OBJET] -->
<div class="modal fade custom-modal" id="create[Objet]Modal" tabindex="-1" role="dialog" aria-labelledby="create[Objet]ModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="create[Objet]ModalLabel">
                    <i class="fas fa-plus-circle"></i> Create [Objet]
                </h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close" style="color: white; opacity: 1;">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <form method="POST" action="{% url '[url_name]' %}" enctype="multipart/form-data" data-validate="true" onsubmit="handleFormSubmit(event, this)">
                {% csrf_token %}
                <div class="modal-body">
                    
                    <!-- Champ de formulaire exemple -->
                    <div class="custom-form-group">
                        <label for="fieldName" class="custom-form-label">
                            <i class="fas fa-[icon]"></i> Label <span class="required">*</span>
                        </label>
                        <input type="text" class="form-control custom-form-control" id="fieldName" name="field_name" placeholder="Enter..." required minlength="3">
                    </div>

                    <!-- Textarea exemple -->
                    <div class="custom-form-group">
                        <label for="description" class="custom-form-label">
                            <i class="fas fa-align-left"></i> Description <span class="required">*</span>
                        </label>
                        <textarea class="form-control custom-form-control auto-resize" id="description" name="description" rows="4" placeholder="Enter description..." required minlength="10"></textarea>
                    </div>

                    <!-- Select exemple -->
                    <div class="custom-form-group">
                        <label for="category" class="custom-form-label">
                            <i class="fas fa-folder"></i> Category <span class="required">*</span>
                        </label>
                        <select class="form-control custom-form-control custom-select" id="category" name="category" required>
                            <option value="">Choose...</option>
                            {% for item in items %}
                            <option value="{{ item.id }}">{{ item.name }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- File input exemple -->
                    <div class="custom-form-group">
                        <label for="file" class="custom-form-label">
                            <i class="fas fa-image"></i> File
                        </label>
                        <input type="file" class="form-control custom-form-control" id="file" name="file" accept="image/*">
                        <small class="form-text text-muted">Optional: Upload an image</small>
                    </div>

                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-custom-secondary" data-dismiss="modal">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                    <button type="submit" class="btn btn-custom-primary">
                        <i class="fas fa-save"></i> Save
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
```

### 🎨 Classes CSS disponibles :

- **Boutons :**
  - `btn-custom-primary` - Bouton principal (doré)
  - `btn-custom-secondary` - Bouton secondaire (gris)
  - `btn-custom-danger` - Bouton danger (rouge)

- **Formulaires :**
  - `custom-form-group` - Groupe de champ
  - `custom-form-label` - Label stylisé
  - `custom-form-control` - Input/textarea/select stylisé
  - `auto-resize` - Textarea qui s'agrandit automatiquement
  - `custom-select` - Select avec flèche personnalisée

- **Modals :**
  - `custom-modal` - Classe principale pour modal
  - `required` - Astérisque rouge pour champs obligatoires

### 🔔 Utiliser les toasts dans les vues Python :

```python
from django.contrib import messages

# Success
messages.success(request, "✅ Opération réussie!")

# Error
messages.error(request, "❌ Une erreur s'est produite")

# Warning
messages.warning(request, "⚠️ Attention!")

# Info
messages.info(request, "ℹ️ Information")
```

### ✅ Validation automatique :

Le système valide automatiquement :
- Champs requis (`required`)
- Longueur minimale (`minlength`)
- Emails (`type="email"`)
- URLs (`type="url"`)
- Nombres avec min/max (`type="number" min="1" max="100"`)

### 📱 Responsive :

Tous les styles sont responsive et s'adaptent automatiquement aux mobiles.

### 🎯 Pages restantes à modifier :

1. Events - event_list.html
2. Gallery - gallery_list.html (déjà partiellement fait)
3. Category - category_list.html
4. Feedback - feedback pages
5. Toutes les pages avec formulaires d'édition

### 💡 Conseils :

1. Toujours utiliser `data-validate="true"` sur les formulaires
2. Ajouter `onsubmit="handleFormSubmit(event, this)"` pour l'état de chargement
3. Utiliser les icônes Font Awesome pour une meilleure UX
4. Tester la validation avant de soumettre

---

**Fichiers créés et prêts à l'emploi !** 🚀
