// Runtime API config for poems page.
// Deployment can override `window.POEMS_API.baseUrl` before `poem.js` loads.
// Examples:
//   local dev:   http://127.0.0.1:8300/api/v1
//   same-origin: /api/v1
(function () {
    window.POEMS_API = window.POEMS_API || {};

    // Prefer explicit override from deploy scripts or manual edits.
    if (!window.POEMS_API.baseUrl) {
        window.POEMS_API.baseUrl = "";
    }
})();
