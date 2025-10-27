// Gestion centralisée des modals et toasts
document.addEventListener('DOMContentLoaded', function() {
    
    // Configuration des toasts
    const toastConfig = {
        success: {
            icon: 'fas fa-check-circle',
            color: '#28a745',
            duration: 3000
        },
        error: {
            icon: 'fas fa-exclamation-circle',
            color: '#dc3545',
            duration: 5000
        },
        warning: {
            icon: 'fas fa-exclamation-triangle',
            color: '#ffc107',
            duration: 4000
        },
        info: {
            icon: 'fas fa-info-circle',
            color: '#17a2b8',
            duration: 3000
        }
    };

    // Fonction pour afficher un toast
    window.showToast = function(message, type = 'success') {
        const config = toastConfig[type] || toastConfig.success;
        
        // Créer le conteneur de toasts s'il n'existe pas
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 10px;
            `;
            document.body.appendChild(toastContainer);
        }

        // Créer le toast
        const toast = document.createElement('div');
        toast.className = 'custom-toast';
        toast.style.cssText = `
            background: white;
            border-left: 4px solid ${config.color};
            border-radius: 8px;
            padding: 15px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 300px;
            max-width: 400px;
            animation: slideInRight 0.3s ease-out;
            cursor: pointer;
        `;

        toast.innerHTML = `
            <i class="${config.icon}" style="color: ${config.color}; font-size: 24px;"></i>
            <span style="flex: 1; color: #333; font-size: 14px;">${message}</span>
            <i class="fas fa-times" style="color: #999; cursor: pointer;"></i>
        `;

        // Ajouter l'animation CSS
        if (!document.getElementById('toast-animations')) {
            const style = document.createElement('style');
            style.id = 'toast-animations';
            style.textContent = `
                @keyframes slideInRight {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                @keyframes slideOutRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        // Fermer le toast au clic
        toast.onclick = function() {
            closeToast(toast);
        };

        toastContainer.appendChild(toast);

        // Auto-fermeture
        setTimeout(() => {
            closeToast(toast);
        }, config.duration);
    };

    function closeToast(toast) {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }

    // Afficher les messages Django
    const djangoMessages = document.querySelectorAll('.django-message');
    djangoMessages.forEach(msg => {
        const type = msg.dataset.type || 'info';
        const message = msg.textContent.trim();
        if (message) {
            showToast(message, type);
        }
        msg.remove();
    });

    // Validation personnalisée des formulaires
    const forms = document.querySelectorAll('form[data-validate="true"]');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        
        inputs.forEach(input => {
            // Style personnalisé
            input.style.cssText += `
                border: 2px solid #e0e0e0;
                transition: all 0.3s ease;
                border-radius: 5px;
                padding: 10px;
            `;

            // Validation en temps réel
            input.addEventListener('blur', function() {
                validateField(this);
            });

            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });

        form.addEventListener('submit', function(e) {
            let isValid = true;
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                showToast('Veuillez corriger les erreurs dans le formulaire', 'error');
            }
        });
    });

    function validateField(field) {
        const errorDiv = field.parentElement.querySelector('.field-error');
        if (errorDiv) errorDiv.remove();

        field.classList.remove('is-valid', 'is-invalid');
        field.style.borderColor = '#e0e0e0';

        let isValid = true;
        let errorMessage = '';

        // Validation requis
        if (field.hasAttribute('required') && !field.value.trim()) {
            isValid = false;
            errorMessage = 'Ce champ est requis';
        }
        // Validation email
        else if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                isValid = false;
                errorMessage = 'Adresse email invalide';
            }
        }
        // Validation longueur minimale
        else if (field.hasAttribute('minlength')) {
            const minLength = parseInt(field.getAttribute('minlength'));
            if (field.value.length < minLength) {
                isValid = false;
                errorMessage = `Minimum ${minLength} caractères requis`;
            }
        }
        // Validation nombre
        else if (field.type === 'number') {
            const min = field.getAttribute('min');
            const max = field.getAttribute('max');
            const value = parseFloat(field.value);
            
            if (min && value < parseFloat(min)) {
                isValid = false;
                errorMessage = `La valeur doit être supérieure ou égale à ${min}`;
            } else if (max && value > parseFloat(max)) {
                isValid = false;
                errorMessage = `La valeur doit être inférieure ou égale à ${max}`;
            }
        }
        // Validation URL
        else if (field.type === 'url' && field.value) {
            try {
                new URL(field.value);
            } catch (_) {
                isValid = false;
                errorMessage = 'URL invalide';
            }
        }

        if (!isValid) {
            field.classList.add('is-invalid');
            field.style.borderColor = '#dc3545';
            
            const error = document.createElement('div');
            error.className = 'field-error';
            error.style.cssText = `
                color: #dc3545;
                font-size: 12px;
                margin-top: 5px;
                display: flex;
                align-items: center;
                gap: 5px;
            `;
            error.innerHTML = `<i class="fas fa-exclamation-circle"></i>${errorMessage}`;
            field.parentElement.appendChild(error);
        } else if (field.value) {
            field.classList.add('is-valid');
            field.style.borderColor = '#28a745';
        }

        return isValid;
    }

    // Gestion des modals Bootstrap existants
    $('.modal').on('shown.bs.modal', function() {
        const firstInput = $(this).find('input, textarea, select').first();
        firstInput.focus();
    });

    // Fermer les modals avec Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                $(modal).modal('hide');
            });
        }
    });
});
