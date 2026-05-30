(function () {
    const snippetsApi = window.SNIPPETS_API || {};

    function resolveApiBaseUrl(config) {
        const explicit = String(config?.baseUrl || "").trim();
        if (explicit) return explicit.replace(/\/+$/, "");

        const { protocol, hostname, origin } = window.location;
        const isLocalHost = hostname === "127.0.0.1" || hostname === "localhost";
        const isFileProtocol = protocol === "file:";

        if (isFileProtocol || isLocalHost) {
            return "http://127.0.0.1:8300/api/v1";
        }

        return `${origin}/api/v1`;
    }

    const apiBaseUrl = resolveApiBaseUrl(snippetsApi);
    const listApiUrl = `${apiBaseUrl}/snippets`;

    const treeEl = document.getElementById('snippetTree');
    const titleEl = document.getElementById('snippetTitle');
    const viewerEl = document.getElementById('snippetViewer');
    const copyBtn = document.getElementById('copySnippetBtn');

    let snippets = [];
    let activeCode = '';
    let activeSnippetSlug = null;
    let listLoading = false;
    let viewerOverlayEl = null;

    const HLJS_LIGHT = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css';
    const HLJS_DARK = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css';

    const INITIAL_VIEWER_MARKUP = `
        <div class="snippets-loading" role="status" aria-label="加载中">
            <div class="snippets-spinner"></div>
        </div>`;

    function getSnippetPreview(slug) {
        return snippets.find((item) => item.slug === slug);
    }

    function setTitleLoading(loading) {
        titleEl.classList.toggle('snippets-title--loading', loading);
        if (loading) {
            titleEl.textContent = '';
            if (!titleEl.querySelector('.snippets-title-skeleton')) {
                titleEl.innerHTML = '<span class="snippets-title-skeleton" aria-hidden="true"></span>';
            }
        }
    }

    function setTitleText(text) {
        titleEl.classList.remove('snippets-title--loading');
        titleEl.textContent = text || '';
    }

    const MIN_LOADING_MS = 200;

    function waitNextPaint() {
        return new Promise((resolve) => {
            requestAnimationFrame(() => requestAnimationFrame(resolve));
        });
    }

    function delay(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }

    async function waitMinLoading(startedAt) {
        const elapsed = performance.now() - startedAt;
        if (elapsed < MIN_LOADING_MS) {
            await delay(MIN_LOADING_MS - elapsed);
        }
    }

    function clearViewerOverlay() {
        viewerOverlayEl?.remove();
        viewerOverlayEl = null;
    }

    function showViewerOverlay() {
        clearViewerOverlay();
        const overlay = document.createElement('div');
        overlay.className = 'snippets-viewer-overlay';
        overlay.setAttribute('role', 'status');
        overlay.setAttribute('aria-label', '加载中');
        overlay.innerHTML = '<div class="snippets-spinner" aria-hidden="true"></div>';
        viewerEl.appendChild(overlay);
        viewerOverlayEl = overlay;
    }

    function setViewerBusy(busy) {
        viewerEl.classList.toggle('snippets-viewer--busy', busy);
        if (busy) {
            const hasContent = viewerEl.querySelector('pre, .snippets-empty');
            if (!hasContent) {
                clearViewerOverlay();
                viewerEl.innerHTML = INITIAL_VIEWER_MARKUP;
                viewerEl.classList.add('snippets-viewer--initial');
            } else {
                viewerEl.classList.remove('snippets-viewer--initial');
                showViewerOverlay();
            }
            copyBtn.disabled = true;
            return;
        }
        clearViewerOverlay();
        viewerEl.classList.remove('snippets-viewer--busy', 'snippets-viewer--initial');
        copyBtn.disabled = !activeCode;
    }

    function showViewerMessage(message) {
        clearViewerOverlay();
        viewerEl.classList.remove('snippets-viewer--busy', 'snippets-viewer--initial');
        viewerEl.innerHTML = `<div class="snippets-empty">${message}</div>`;
        setTitleText('');
        activeCode = '';
        activeSnippetSlug = null;
        copyBtn.disabled = true;
    }

    function renderTree() {
        treeEl.innerHTML = '';
        if (!snippets.length) {
            treeEl.innerHTML = '<div class="snippets-empty">暂无片段</div>';
            return;
        }

        const ul = document.createElement('ul');
        snippets.forEach((item) => {
            const li = document.createElement('li');
            li.className = 'snippets-item';
            li.dataset.slug = item.slug;
            li.innerHTML = `<span class="snippets-file-name">${item.file_name}</span>`;
            li.addEventListener('click', () => selectSnippet(item.slug));
            ul.appendChild(li);
        });
        treeEl.appendChild(ul);
    }

    function renderSnippet(snippet) {
        activeSnippetSlug = snippet.slug;
        setTitleText(snippet.title);
        activeCode = snippet.code || '';
        copyBtn.disabled = !activeCode;

        if (!activeCode) {
            showViewerMessage('该片段暂无代码');
            return;
        }

        let html = activeCode;
        if (window.hljs) {
            html = hljs.highlight(activeCode, { language: snippet.lang || 'plaintext' }).value;
        }
        clearViewerOverlay();
        viewerEl.classList.remove('snippets-viewer--busy', 'snippets-viewer--initial');
        viewerEl.innerHTML = `<pre><code class="hljs language-${snippet.lang || 'plaintext'}">${html}</code></pre>`;

        document.querySelectorAll('.snippets-item').forEach((el) => {
            el.classList.toggle('active', el.dataset.slug === snippet.slug);
        });

        const params = new URLSearchParams(window.location.search);
        params.set('id', snippet.slug);
        params.delete('file');
        window.history.replaceState({}, '', `${window.location.pathname}?${params}`);
    }

    async function fetchSnippetDetail(slug) {
        const res = await fetch(`${listApiUrl}/${encodeURIComponent(slug)}`);
        const payload = await res.json().catch(() => ({}));
        if (!res.ok || !payload.success || !payload.data) {
            throw new Error(payload.message || `加载失败 (${res.status})`);
        }
        return payload.data;
    }

    async function selectSnippet(slug, { initial = false, force = false } = {}) {
        if (!force && slug === activeSnippetSlug && activeCode) {
            return;
        }

        const preview = getSnippetPreview(slug);
        if (initial) {
            setTitleLoading(true);
        } else if (preview) {
            setTitleText(preview.title || preview.file_name || '');
        }

        setViewerBusy(true);
        const loadingStarted = performance.now();
        await waitNextPaint();

        try {
            const snippet = await fetchSnippetDetail(slug);
            await waitMinLoading(loadingStarted);
            renderSnippet(snippet);
            syncHljsTheme();
        } catch (error) {
            await waitMinLoading(loadingStarted);
            showViewerMessage(error.message || '加载片段失败');
        } finally {
            setViewerBusy(false);
        }
    }

    async function loadSnippets() {
        if (listLoading) return;
        listLoading = true;
        treeEl.innerHTML = `<div class="snippets-loading snippets-loading--compact" role="status" aria-label="加载中"><div class="snippets-spinner"></div></div>`;
        setTitleLoading(true);
        setViewerBusy(true);

        try {
            const res = await fetch(`${listApiUrl}?page=1&page_size=100`);
            const payload = await res.json().catch(() => ({}));
            if (!res.ok || !payload.success || !payload.data) {
                throw new Error(payload.message || `列表加载失败 (${res.status})`);
            }
            snippets = Array.isArray(payload.data.items) ? payload.data.items : [];
            renderTree();

            const params = new URLSearchParams(window.location.search);
            const wanted = params.get('id')
                || snippets.find((item) => item.file_name === params.get('file'))?.slug;
            const initial = snippets.find((item) => item.slug === wanted) || snippets[0];
            if (initial) {
                await selectSnippet(initial.slug, { initial: true });
            } else {
                showViewerMessage('选择左侧片段');
            }
        } catch (error) {
            snippets = [];
            treeEl.innerHTML = `<div class="snippets-empty">${error.message || '无法加载片段列表'}</div>`;
            showViewerMessage('请确认后端服务已启动（端口 8300）');
        } finally {
            listLoading = false;
        }
    }

    function syncHljsTheme() {
        const link = document.getElementById('hljsTheme');
        if (!link) return;
        const dark = document.documentElement.getAttribute('data-theme') === 'dark';
        link.href = dark ? HLJS_DARK : HLJS_LIGHT;
    }

    copyBtn.addEventListener('click', async () => {
        if (!activeCode) return;
        try {
            await navigator.clipboard.writeText(activeCode);
            copyBtn.textContent = '已复制';
            setTimeout(() => { copyBtn.textContent = '复制代码'; }, 1500);
        } catch {
            copyBtn.textContent = '复制失败';
        }
    });

    document.addEventListener('DOMContentLoaded', () => {
        syncHljsTheme();
        document.getElementById('themeToggle')?.addEventListener('click', () => {
            setTimeout(() => {
                syncHljsTheme();
                if (activeSnippetSlug && activeCode) {
                    const item = getSnippetPreview(activeSnippetSlug);
                    renderSnippet({
                        slug: activeSnippetSlug,
                        title: titleEl.textContent,
                        code: activeCode,
                        lang: item?.lang || 'cpp',
                    });
                    return;
                }
                if (activeSnippetSlug) {
                    selectSnippet(activeSnippetSlug, { force: true });
                }
            }, 0);
        });

        loadSnippets();
    });
})();
