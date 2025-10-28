// AI Features for Blog: Translation and Sentiment Analysis

// ===== TRADUCTION MULTILINGUE =====
class PostTranslator {
    constructor(postId) {
        this.postId = postId;
        this.originalTitle = null;
        this.originalContent = null;
        this.currentLanguage = 'fr';
        this.translations = {};
    }

    async translatePost(targetLanguage) {
        // Si déjà dans la langue cible, ne rien faire
        if (this.currentLanguage === targetLanguage) {
            return;
        }

        // Sauvegarder l'original si pas encore fait
        if (!this.originalTitle) {
            this.originalTitle = document.querySelector('.post-title')?.textContent;
            this.originalContent = document.querySelector('.post-content')?.textContent;
        }

        // Afficher un loader
        this.showLoader();

        try {
            const response = await fetch(`/blog/post/${this.postId}/translate/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ language: targetLanguage })
            });

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            // Mettre à jour l'affichage
            this.updateDisplay(data.title, data.content);
            this.currentLanguage = targetLanguage;

            // Sauvegarder en cache
            this.translations[targetLanguage] = {
                title: data.title,
                content: data.content
            };

            // Afficher un message de succès
            const cacheStatus = data.cached ? '(depuis le cache)' : '(nouvellement traduit)';
            this.showMessage(`✅ Traduit en ${this.getLanguageName(targetLanguage)} ${cacheStatus}`, 'success');

        } catch (error) {
            console.error('Translation error:', error);
            this.showMessage(`❌ Erreur de traduction: ${error.message}`, 'error');
        } finally {
            this.hideLoader();
        }
    }

    updateDisplay(title, content) {
        const titleElement = document.querySelector('.post-title');
        const contentElement = document.querySelector('.post-content');

        if (titleElement) {
            titleElement.textContent = title;
        }
        if (contentElement) {
            contentElement.textContent = content;
        }
    }

    showLoader() {
        const loader = document.getElementById('translation-loader');
        if (loader) {
            loader.style.display = 'block';
        }
    }

    hideLoader() {
        const loader = document.getElementById('translation-loader');
        if (loader) {
            loader.style.display = 'none';
        }
    }

    showMessage(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '20px';
        alertDiv.style.right = '20px';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.minWidth = '300px';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);

        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    getLanguageName(code) {
        const names = {
            'fr': 'Français',
            'en': 'English',
            'ar': 'العربية',
            'es': 'Español'
        };
        return names[code] || code;
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
    }
}

// ===== ANALYSE DE SENTIMENT =====
class SentimentAnalyzer {
    constructor(postId) {
        this.postId = postId;
    }

    async getSentiment() {
        try {
            const response = await fetch(`/blog/post/${this.postId}/sentiment/`);
            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            this.displaySentiment(data);
        } catch (error) {
            console.error('Sentiment analysis error:', error);
        }
    }

    displaySentiment(data) {
        const container = document.getElementById('sentiment-info');
        if (!container) return;

        const emoji = {
            'positive': '😊',
            'negative': '😔',
            'neutral': '😐'
        }[data.sentiment_label] || '📊';

        const colorClass = {
            'positive': 'success',
            'negative': 'danger',
            'neutral': 'secondary'
        }[data.sentiment_label] || 'info';

        let html = `
            <div class="card border-${colorClass} mb-3">
                <div class="card-body">
                    <h6><i class="fas fa-brain"></i> Analyse IA</h6>
                    <p class="mb-2">
                        <strong>Sentiment :</strong> 
                        <span class="badge bg-${colorClass}">${emoji} ${data.sentiment_label || 'Non analysé'}</span>
                    </p>
        `;

        if (data.sentiment_score !== null) {
            const scorePercent = ((data.sentiment_score + 1) / 2 * 100).toFixed(0);
            html += `
                <div class="progress mb-2" style="height: 20px;">
                    <div class="progress-bar bg-${colorClass}" style="width: ${scorePercent}%">
                        ${scorePercent}%
                    </div>
                </div>
            `;
        }

        if (!data.is_appropriate) {
            html += `
                <div class="alert alert-warning mt-2 mb-0">
                    <small><i class="fas fa-exclamation-triangle"></i> <strong>Modération :</strong> ${data.moderation_reason}</small>
                </div>
            `;
        }

        html += `</div></div>`;
        container.innerHTML = html;
    }

    async reanalyze() {
        const btn = document.getElementById('reanalyze-btn');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyse...';
        }

        try {
            const response = await fetch(`/blog/post/${this.postId}/reanalyze/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            alert('✅ ' + data.message);
            location.reload();

        } catch (error) {
            console.error('Reanalysis error:', error);
            alert('❌ Erreur: ' + error.message);
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-sync"></i> Re-analyser';
            }
        }
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
    }
}

// ===== INITIALISATION =====
function initAIFeatures(postId) {
    const translator = new PostTranslator(postId);
    const analyzer = new SentimentAnalyzer(postId);

    // Boutons de traduction
    document.querySelectorAll('.translate-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const language = this.dataset.lang;
            translator.translatePost(language);
        });
    });

    // Bouton de re-analyse
    const reanalyzeBtn = document.getElementById('reanalyze-btn');
    if (reanalyzeBtn) {
        reanalyzeBtn.addEventListener('click', () => analyzer.reanalyze());
    }

    // Charger l'analyse de sentiment au chargement
    analyzer.getSentiment();
}

// Export pour utilisation globale
if (typeof window !== 'undefined') {
    window.PostTranslator = PostTranslator;
    window.SentimentAnalyzer = SentimentAnalyzer;
    window.initAIFeatures = initAIFeatures;
}
