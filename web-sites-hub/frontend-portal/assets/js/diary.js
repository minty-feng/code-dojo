// Diary Page JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Load More functionality
    const loadMoreBtn = document.querySelector('.load-more-btn');
    
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            // Show loading state
            const btnText = loadMoreBtn.querySelector('span');
            const btnIcon = loadMoreBtn.querySelector('svg');
            const originalText = btnText.textContent;
            
            btnText.textContent = '加载中...';
            btnIcon.style.animation = 'spin 1s linear infinite';
            loadMoreBtn.disabled = true;
            
            // Simulate loading
            setTimeout(() => {
                btnText.textContent = '暂无更多内容';
                btnIcon.style.animation = '';
                loadMoreBtn.style.opacity = '0.5';
                loadMoreBtn.style.cursor = 'not-allowed';
            }, 1000);
        });
    }

    // Add entrance animation for diary entries
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    entry.target.style.transition = 'all 0.6s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const diaryEntries = document.querySelectorAll('.diary-entry');
    diaryEntries.forEach((entry, index) => {
        // Add stagger delay
        entry.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(entry);
    });
});

// Add spin animation for loading
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

