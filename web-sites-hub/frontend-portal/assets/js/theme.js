(function (global) {
    'use strict';

    var COOKIE_NAME = 'joketop_theme';
    var STORAGE_KEY = 'theme';

    function getCookie(name) {
        var match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
        return match ? decodeURIComponent(match[1]) : null;
    }

    function cookieDomain() {
        var host = location.hostname;
        if (host === 'joketop.com' || host.endsWith('.joketop.com')) {
            return '.joketop.com';
        }
        return '';
    }

    function normalizeTheme(value) {
        return value === 'light' || value === 'dark' ? value : null;
    }

    function readTheme() {
        var fromCookie = normalizeTheme(getCookie(COOKIE_NAME));
        if (fromCookie) {
            return fromCookie;
        }

        try {
            var fromStorage = normalizeTheme(localStorage.getItem(STORAGE_KEY));
            if (fromStorage) {
                return fromStorage;
            }
        } catch (err) {
            /* ignore private mode / blocked storage */
        }

        var pageDefault = document.documentElement.getAttribute('data-default-theme');
        return normalizeTheme(pageDefault) || 'light';
    }

    function persistTheme(theme) {
        var normalized = normalizeTheme(theme);
        if (!normalized) {
            return;
        }

        try {
            localStorage.setItem(STORAGE_KEY, normalized);
        } catch (err) {
            /* ignore */
        }

        var maxAge = 60 * 60 * 24 * 365;
        var cookie = COOKIE_NAME + '=' + encodeURIComponent(normalized)
            + '; path=/; max-age=' + maxAge + '; SameSite=Lax';
        var domain = cookieDomain();
        if (domain) {
            cookie += '; domain=' + domain;
        }
        document.cookie = cookie;
    }

    function applyTheme(theme) {
        var normalized = normalizeTheme(theme) || 'light';
        document.documentElement.setAttribute('data-theme', normalized);
        return normalized;
    }

    function initTheme() {
        var theme = readTheme();
        applyTheme(theme);
        if (!getCookie(COOKIE_NAME)) {
            persistTheme(theme);
        }
    }

    global.JoketopTheme = {
        readTheme: readTheme,
        persistTheme: persistTheme,
        applyTheme: applyTheme,
        initTheme: initTheme,
    };

    initTheme();
})(window);
