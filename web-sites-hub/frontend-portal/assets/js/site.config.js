// Site-wide config. Edit copyright here once; all pages with data-site-copyright use it.
(function () {
    window.SITE_CONFIG = {
        copyrightYear: 2026,
        siteName: 'minty-feng',
    };

    function applySiteCopyright() {
        const year = window.SITE_CONFIG.copyrightYear;
        const name = window.SITE_CONFIG.siteName;
        const text = `\u00A9 ${year} ${name}`;
        document.querySelectorAll('[data-site-copyright]').forEach((el) => {
            el.textContent = text;
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applySiteCopyright);
    } else {
        applySiteCopyright();
    }
})();
