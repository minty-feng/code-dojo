// Showcase Page JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Filter functionality
    const filterTabs = document.querySelectorAll('.filter-tab');
    const projectCards = document.querySelectorAll('.project-card');

    filterTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const filter = tab.dataset.filter;

            // Update active tab
            filterTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Filter projects
            projectCards.forEach(card => {
                const category = card.dataset.category;
                
                if (filter === 'all' || category === filter) {
                    card.classList.remove('hidden');
                    // Add animation
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    
                    setTimeout(() => {
                        card.style.transition = 'all 0.3s ease';
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 50);
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });
});

