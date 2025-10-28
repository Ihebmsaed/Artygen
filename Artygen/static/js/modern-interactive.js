// Modern Interactive JavaScript

// Smooth scroll to sections
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Form validation with modern feedback
    const forms = document.querySelectorAll('form[data-validate="true"]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');
                    showFieldError(input, 'Ce champ est requis');
                } else {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                    hideFieldError(input);
                }
            });

            if (!isValid) {
                e.preventDefault();
                showAlert('Veuillez remplir tous les champs requis', 'danger');
            }
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('is-invalid');
                    showFieldError(this, 'Ce champ est requis');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                    hideFieldError(this);
                }
            });

            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.value.trim()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                    hideFieldError(this);
                }
            });
        });
    });

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert[data-auto-dismiss="true"]');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Image preview for file uploads
    const fileInputs = document.querySelectorAll('input[type="file"][data-preview]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const previewId = this.getAttribute('data-preview');
            const preview = document.getElementById(previewId);
            
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // Tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = createTooltip(tooltipText);
            this.appendChild(tooltip);
        });

        element.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.tooltip');
            if (tooltip) tooltip.remove();
        });
    });

    // Loading button state
    const loadingButtons = document.querySelectorAll('[data-loading-text]');
    loadingButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                const originalText = this.textContent;
                const loadingText = this.getAttribute('data-loading-text');
                this.textContent = loadingText;
                this.disabled = true;
                
                // Re-enable after form submission (fallback)
                setTimeout(() => {
                    this.textContent = originalText;
                    this.disabled = false;
                }, 10000);
            }
        });
    });

    // Password visibility toggle
    const passwordToggles = document.querySelectorAll('[data-toggle-password]');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-toggle-password');
            const input = document.getElementById(targetId);
            
            if (input) {
                if (input.type === 'password') {
                    input.type = 'text';
                    this.textContent = '🙈';
                } else {
                    input.type = 'password';
                    this.textContent = '👁️';
                }
            }
        });
    });

    // Confirm dialogs
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
});

// Helper Functions
function showFieldError(input, message) {
    let errorDiv = input.parentElement.querySelector('.field-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'field-error text-danger mt-1';
        errorDiv.style.fontSize = '0.875rem';
        input.parentElement.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

function hideFieldError(input) {
    const errorDiv = input.parentElement.querySelector('.field-error');
    if (errorDiv) errorDiv.remove();
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.style.animation = 'slideInRight 0.3s';
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

function createTooltip(text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.style.position = 'absolute';
    tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    tooltip.style.color = 'white';
    tooltip.style.padding = '0.5rem 1rem';
    tooltip.style.borderRadius = '6px';
    tooltip.style.fontSize = '0.875rem';
    tooltip.style.bottom = '100%';
    tooltip.style.left = '50%';
    tooltip.style.transform = 'translateX(-50%)';
    tooltip.style.marginBottom = '8px';
    tooltip.style.whiteSpace = 'nowrap';
    tooltip.style.zIndex = '1000';
    return tooltip;
}

// Debounce helper for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Copy to clipboard utility
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copié dans le presse-papier!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showAlert('Copié dans le presse-papier!', 'success');
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);

console.log('✅ Modern Interactive JS loaded successfully!');
