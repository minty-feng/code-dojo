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
        updateThemeIcon(); // Update icon after animation
        // Reinitialize effects when theme changes
        initializeDarkModeEffects();
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

// Particle Background Effect
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;
    
    const particleCount = 50;
    const particles = [];
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 4 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = 'rgba(255, 255, 255, 0.3)';
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.pointerEvents = 'none';
        particle.style.transition = 'all 0.3s ease';
        
        particlesContainer.appendChild(particle);
        particles.push({
            element: particle,
            x: Math.random() * 100,
            y: Math.random() * 100,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5
        });
    }
    
    function animateParticles() {
        particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            if (particle.x < 0 || particle.x > 100) particle.vx *= -1;
            if (particle.y < 0 || particle.y > 100) particle.vy *= -1;
            
            particle.element.style.left = particle.x + '%';
            particle.element.style.top = particle.y + '%';
        });
        
        requestAnimationFrame(animateParticles);
    }
    
    animateParticles();
}

// Initialize particles when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createParticles);
} else {
    createParticles();
}

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

// Snowflakes Effect - Only in dark mode
function createSnowflakes() {
    const snowflakesContainer = document.getElementById('snowflakes');
    if (!snowflakesContainer) return;
    
    const snowflakeSymbols = ['❅', '❆', '❄', '✻', '✼', '✽', '✾', '✿', '❀', '❁'];
    const snowflakeCount = 20;
    
    // Clear existing snowflakes
    snowflakesContainer.innerHTML = '';
    
    for (let i = 0; i < snowflakeCount; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        snowflake.textContent = snowflakeSymbols[Math.floor(Math.random() * snowflakeSymbols.length)];
        snowflake.style.fontSize = (Math.random() * 10 + 10) + 'px';
        snowflake.style.opacity = Math.random() * 0.5 + 0.5;
        snowflakesContainer.appendChild(snowflake);
    }
}

// Fireflies Effect - Only in dark mode
function createFireflies() {
    const firefliesContainer = document.getElementById('fireflies');
    if (!firefliesContainer) {
        console.warn('Fireflies container not found');
        return;
    }
    
    const fireflyCount = 20;
    
    // Clear existing fireflies
    firefliesContainer.innerHTML = '';
    
    for (let i = 0; i < fireflyCount; i++) {
        const firefly = document.createElement('div');
        firefly.className = 'firefly';
        
        // Random starting position
        const startX = Math.random() * window.innerWidth;
        const startY = Math.random() * window.innerHeight;
        firefly.style.left = startX + 'px';
        firefly.style.top = startY + 'px';
        
        // Random size (larger so they're more visible)
        const size = Math.random() * 4 + 6; // 6-10px
        firefly.style.width = size + 'px';
        firefly.style.height = size + 'px';
        
        // Random initial opacity
        firefly.style.opacity = Math.random() * 0.5 + 0.5;
        
        // Random direction
        const angle = Math.random() * Math.PI * 2;
        const distance = Math.random() * 300 + 200; // 200-500px
        firefly.style.setProperty('--firefly-dx', Math.cos(angle) * distance + 'px');
        firefly.style.setProperty('--firefly-dy', Math.sin(angle) * distance + 'px');
        
        // Random animation duration
        const duration = Math.random() * 8 + 8; // 8-16s
        firefly.style.animationDuration = duration + 's';
        firefly.style.animationDelay = Math.random() * 2 + 's';
        
        firefliesContainer.appendChild(firefly);
        
        // Restart animation with new position
        const restartAnimation = () => {
            if (!firefly.parentNode) return;
            
            const newX = Math.random() * window.innerWidth;
            const newY = Math.random() * window.innerHeight;
            firefly.style.left = newX + 'px';
            firefly.style.top = newY + 'px';
            
            const newAngle = Math.random() * Math.PI * 2;
            const newDistance = Math.random() * 300 + 200;
            firefly.style.setProperty('--firefly-dx', Math.cos(newAngle) * newDistance + 'px');
            firefly.style.setProperty('--firefly-dy', Math.sin(newAngle) * newDistance + 'px');
            
            firefly.style.animation = 'none';
            setTimeout(() => {
                firefly.style.animation = '';
            }, 10);
        };
        
        // Restart periodically
        setInterval(restartAnimation, duration * 1000);
    }
    
    console.log(`Created ${fireflyCount} fireflies`);
}

// Initialize effects based on theme
function initializeDarkModeEffects() {
    console.log('initializeDarkModeEffects called');
    const currentTheme = html.getAttribute('data-theme');
    console.log('Current theme:', currentTheme);
    console.log('HTML element:', html);
    
    const firefliesContainer = document.getElementById('fireflies');
    console.log('Fireflies container:', firefliesContainer);
    
    if (!firefliesContainer) {
        console.error('❌ Fireflies container not found!');
        return;
    }
    
    // CSS default is dark theme, so if theme is 'light', hide effects
    // Otherwise (dark or empty), show effects
    if (currentTheme === 'light') {
        // Clear effects in light mode
        const snowflakesContainer = document.getElementById('snowflakes');
        if (snowflakesContainer) snowflakesContainer.innerHTML = '';
        if (firefliesContainer) firefliesContainer.innerHTML = '';
        console.log('Light mode: effects cleared');
    } else {
        // Show effects in dark mode (default)
        console.log('Dark mode: creating effects');
        createSnowflakes();
        createFireflies();
    }
}

// Handle window resize for fireflies
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        const currentTheme = html.getAttribute('data-theme');
        if (currentTheme !== 'light') {
            createFireflies();
        }
    }, 250);
});


// Initialize effects on page load - use multiple methods to ensure it runs
console.log('Setting up initialization...');
console.log('Document ready state:', document.readyState);
console.log('Fireflies container exists:', !!document.getElementById('fireflies'));

// Method 1: window.onload (fires when all resources are loaded)
window.addEventListener('load', () => {
    console.log('✅ Window loaded event fired');
    setTimeout(() => {
        console.log('✅ Calling initializeDarkModeEffects from window.load');
        initializeDarkModeEffects();
    }, 100);
});

// Method 2: DOMContentLoaded (fires when DOM is ready)
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('✅ DOMContentLoaded event fired');
        setTimeout(() => {
            console.log('✅ Calling initializeDarkModeEffects from DOMContentLoaded');
            initializeDarkModeEffects();
        }, 100);
    });
} else {
    // DOM already loaded
    console.log('✅ DOM already loaded, setting timeout');
    setTimeout(() => {
        console.log('✅ Calling initializeDarkModeEffects from timeout');
        initializeDarkModeEffects();
    }, 1000);
}

// Method 3: Immediate attempt after a delay
setTimeout(() => {
    console.log('✅ Attempting immediate initialization');
    initializeDarkModeEffects();
}, 2000);

// Recreate fireflies periodically for continuous movement
setInterval(() => {
    const currentTheme = html.getAttribute('data-theme');
    if (currentTheme !== 'light') {
        createFireflies();
    }
}, 30000); // Every 30 seconds


// Console message
console.log('%c🚀 Welcome to minty-feng\'s personal website!', 'color: #667eea; font-size: 16px; font-weight: bold;');
console.log('%cBuilt with ❤️', 'color: #764ba2; font-size: 12px;');

// 本地/线上链接切换已移至 index.html 内联脚本，优先执行


