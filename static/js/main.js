/* ----------------------------------------------------
   Django Blog Platform - Interactive Frontend Scripts
   ---------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Dark Mode / Light Mode Theme Toggle
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Set initial theme
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            let theme = document.documentElement.getAttribute('data-theme');
            let newTheme = (theme === 'dark') ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (!themeIcon) return;
        if (theme === 'dark') {
            themeIcon.className = 'bi bi-sun-fill';
        } else {
            themeIcon.className = 'bi bi-moon-stars-fill';
        }
    }

    // 2. AJAX Liking Functionality
    const likeButton = document.getElementById('likeButton');
    if (likeButton) {
        likeButton.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            const formData = new FormData();
            formData.append('post_id', postId);

            fetch('/like/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const likeIcon = document.getElementById('likeIcon');
                const likeCount = document.getElementById('likeCount');
                
                if (data.liked) {
                    likeIcon.className = 'bi bi-heart-fill btn-like-active';
                } else {
                    likeIcon.className = 'bi bi-heart btn-like-inactive';
                }
                likeCount.innerText = data.total_likes;
            })
            .catch(error => console.error('Error handling post like:', error));
        });
    }

    // 3. AJAX Commenting Functionality
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const contentField = document.getElementById('commentContentField');
            const content = contentField.value.trim();

            if (!content) return;

            const formData = new FormData(this);

            fetch(`/post/${postId}/comment/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    // Create and insert new comment
                    const commentsContainer = document.getElementById('commentsContainer');
                    const noCommentsMsg = document.getElementById('noCommentsMsg');
                    
                    if (noCommentsMsg) {
                        noCommentsMsg.style.display = 'none';
                    }

                    const commentHtml = `
                        <div class="comment-card animate-fade-in">
                            <div class="d-flex align-items-center mb-2">
                                <img src="${data.avatar_url}" alt="${data.username}" class="profile-avatar-sm me-2">
                                <div>
                                    <h6 class="mb-0 text-primary font-weight-bold">${data.username}</h6>
                                    <small class="text-muted">${data.created_on}</small>
                                </div>
                            </div>
                            <p class="mb-0 text-primary" style="white-space: pre-wrap;">${escapeHTML(data.content)}</p>
                        </div>
                    `;
                    
                    commentsContainer.insertAdjacentHTML('afterbegin', commentHtml);
                    
                    // Increment Comment Count badge
                    const commentCountBadge = document.getElementById('commentCountBadge');
                    if (commentCountBadge) {
                        commentCountBadge.innerText = parseInt(commentCountBadge.innerText || 0) + 1;
                    }

                    // Reset form
                    contentField.value = '';
                }
            })
            .catch(error => {
                console.error('Error submitting comment:', error);
                alert('Oops, something went wrong while posting your comment.');
            });
        });
    }

    // 4. Live Markdown Editor Preview
    const markdownTextarea = document.getElementById('id_content');
    const previewArea = document.getElementById('markdownPreview');
    
    if (markdownTextarea && previewArea) {
        const renderPreview = () => {
            const rawText = markdownTextarea.value;
            if (typeof marked !== 'undefined') {
                previewArea.innerHTML = marked.parse(rawText);
            } else {
                // Fallback basic text preview if marked library hasn't loaded
                previewArea.innerText = rawText;
            }
        };

        // Render initially
        renderPreview();

        // Listen for input
        markdownTextarea.addEventListener('input', renderPreview);
    }

    // Helper: Escape HTML strings for safety
    function escapeHTML(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
