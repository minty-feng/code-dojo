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

    const HLJS_LIGHT = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css';
    const HLJS_DARK = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css';

    function syncHljsTheme() {
        const link = document.getElementById('hljsTheme');
        if (!link) return;
        const dark = document.documentElement.getAttribute('data-theme') === 'dark';
        link.href = dark ? HLJS_DARK : HLJS_LIGHT;
    }

    function showViewerMessage(message) {
        viewerEl.innerHTML = `<div class="snippets-empty">${message}</div>`;
        titleEl.textContent = '—';
        activeCode = '';
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
        titleEl.textContent = snippet.title;
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

    async function selectSnippet(slug) {
        try {
            showViewerMessage('加载中…');
            const snippet = await fetchSnippetDetail(slug);
            renderSnippet(snippet);
            syncHljsTheme();
        } catch (error) {
            showViewerMessage(error.message || '加载片段失败');
        }
    }

    async function loadSnippets() {
        if (listLoading) return;
        listLoading = true;
        treeEl.innerHTML = '<div class="snippets-empty">加载中…</div>';

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
                await selectSnippet(initial.slug);
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
                if (activeSnippetSlug) selectSnippet(activeSnippetSlug);
            }, 0);
        });

        loadSnippets();
    });
})();
