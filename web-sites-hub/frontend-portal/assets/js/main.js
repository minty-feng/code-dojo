// Debug: Check if script is loaded
console.log('✅ main.js loaded');

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

// Check for saved theme preference or default to dark mode (CSS default is dark)
const currentTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', currentTheme);

// Update theme icon based on current theme
function updateThemeIcon() {
    const themeIcon = themeToggle.querySelector('.theme-icon');
    const currentTheme = html.getAttribute('data-theme');
    
    // Update icon path based on theme
    if (currentTheme === 'dark') {
        // Moon icon for dark mode
        themeIcon.innerHTML = `
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        `;
    } else {
        // Sun icon for light mode
        themeIcon.innerHTML = `
            <circle cx="12" cy="12" r="5"></circle>
            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
        `;
    }
}

// Theme toggle handler
themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icon animation
    themeToggle.style.transform = 'rotate(360deg)';
    setTimeout(() => {
        themeToggle.style.transform = 'rotate(0deg)';
        updateThemeIcon();
    }, 300);
});

// Initialize theme icon
updateThemeIcon();

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Animate cards on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe all site cards
document.querySelectorAll('.site-card').forEach(card => {
    observer.observe(card);
});

// Add hover effect for cards
document.querySelectorAll('.site-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Preload images on hover
document.querySelectorAll('.site-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        // Add any preloading logic here if needed
        this.style.willChange = 'transform';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.willChange = 'auto';
    });
});

// Add click tracking (optional - for analytics)
document.querySelectorAll('.site-card, .link-item').forEach(link => {
    link.addEventListener('click', function(e) {
        // You can add analytics tracking here
        console.log('Clicked:', this.href);
    });
});

// Keyboard navigation support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close any modals or menus if needed
        document.activeElement.blur();
    }
});

// Add loading state for external links
document.querySelectorAll('a[href^="http"]').forEach(link => {
    link.addEventListener('click', function(e) {
        // Add a small delay to show loading state
        this.style.opacity = '0.7';
        
        // Reset after navigation
        setTimeout(() => {
            this.style.opacity = '1';
        }, 100);
    });
});

// Add ripple effect on card click
document.querySelectorAll('.site-card').forEach(card => {
    card.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add CSS for ripple effect dynamically
const style = document.createElement('style');
style.textContent = `
    .site-card {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    [data-theme="dark"] .ripple {
        background: rgba(255, 255, 255, 0.1);
    }
`;
document.head.appendChild(style);

// Smooth scroll for hero scroll button
const heroScroll = document.querySelector('.hero-scroll');
if (heroScroll) {
    heroScroll.addEventListener('click', () => {
        document.querySelector('.main').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
}

// Console message
console.log('%c🚀 Welcome to minty-feng\'s personal website!', 'color: #667eea; font-size: 16px; font-weight: bold;');
console.log('%cBuilt with ❤️', 'color: #764ba2; font-size: 12px;');

// 本地/线上链接切换已移至 index.html 内联脚本，优先执行


