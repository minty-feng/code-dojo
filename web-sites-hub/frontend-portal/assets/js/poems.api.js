// Poems frontend runtime API settings.
// You can override window.POEMS_API before this script loads.
(function () {
    const defaultApi = {
        baseUrl: "http://127.0.0.1:8300/api/v1",
        pageSize: 100
    };
    window.POEMS_API = Object.assign({}, defaultApi, window.POEMS_API || {});
})();

