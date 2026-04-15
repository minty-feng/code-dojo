// ============================================================
// Section 1: Runtime config and page state
// ============================================================
// Poems page runtime entry.
// Reads API config from window.POEMS_API (injected by poem.config.js).
const poemsApi = window.POEMS_API || {};
const apiBaseUrl = poemsApi.baseUrl || "http://127.0.0.1:8300/api/v1";
const wordcloudApiUrl = `${apiBaseUrl}/poems/meta/wordcloud`;
const STORAGE_KEY_FAVORITES = "poems-favorites-v1";
const STORAGE_KEY_SCRIPT = "poems-script-mode";
let scriptMode = localStorage.getItem(STORAGE_KEY_SCRIPT) || "simplified";
let poems = [];
let listTotal = 0;
let filterMetaLoaded = false;
let metaCategories = [];
let metaDynasties = [];
let favorites = JSON.parse(localStorage.getItem(STORAGE_KEY_FAVORITES) || "{}");
let activeHot = "";
let currentPage = 1;
let currentPageSize = Math.min(Math.max(Number(poemsApi.pageSize || 20), 1), 100);
let listLoading = false;

const fallback = [
    { title: "定风波", title_simplified: "定风波", title_traditional: "定風波", author: "苏轼", author_simplified: "苏轼", author_traditional: "蘇軾", dynasty: "宋", category: "宋词", tags: "豁达", content_simplified: "莫听穿林打叶声，何妨吟啸且徐行。", content_traditional: "莫聽穿林打葉聲，何妨吟嘯且徐行。" },
    { title: "将进酒", title_simplified: "将进酒", title_traditional: "將進酒", author: "李白", author_simplified: "李白", author_traditional: "李白", dynasty: "唐", category: "古诗", tags: "豪放", content_simplified: "君不见，黄河之水天上来。", content_traditional: "君不見，黃河之水天上來。" }
];
const defaultCloudData = {
    ci: [
        ["明月", 56], ["春风", 52], ["江南", 45], ["归来", 44], ["天涯", 41], ["相思", 40],
        ["风流", 38], ["梅花", 35], ["斜阳", 33], ["楼台", 30], ["往事", 29], ["夜雨", 27]
    ],
    shi: [
        ["长安", 58], ["春风", 54], ["明月", 53], ["黄河", 46], ["故人", 44], ["青山", 41],
        ["万里", 39], ["白云", 36], ["江城", 33], ["边塞", 30], ["秋风", 28], ["归舟", 26]
    ],
    poets: [
        ["苏轼", 60], ["陆游", 53], ["辛弃疾", 49], ["杨万里", 43], ["范成大", 40], ["梅尧臣", 37],
        ["王安石", 35], ["欧阳修", 33], ["黄庭坚", 31], ["晏殊", 28], ["曾巩", 26], ["秦观", 24]
    ],
    ci_pai: [
        ["水调歌头", 100], ["念奴娇", 96], ["沁园春", 94], ["满江红", 92], ["临江仙", 90], ["西江月", 88],
        ["鹧鸪天", 86], ["菩萨蛮", 84], ["蝶恋花", 82], ["虞美人", 80], ["青玉案", 78], ["如梦令", 76]
    ]
};
const defaultCloudTitles = {
    ci: "宋词高频词",
    shi: "唐诗高频词",
    poets: "古今诗词作家高频人名",
    ci_pai: "宋词高频词牌"
};
let cloudData = { ...defaultCloudData };

// ============================================================
// Section 2: Shared view helpers
// ============================================================
function applyCloudTitles(titles = defaultCloudTitles) {
    const map = {
        ci: "cloud-title-ci",
        shi: "cloud-title-tang",
        poets: "cloud-title-song",
        ci_pai: "cloud-title-cipai"
    };
    Object.entries(map).forEach(([key, id]) => {
        const el = document.getElementById(id);
        if (el) el.textContent = titles[key] || defaultCloudTitles[key];
    });
}

function keyOf(poem) { return `${poem.title_simplified || ""}__${poem.author_simplified || ""}`; }
function getTitle(poem) { return scriptMode === "traditional" ? (poem.title_traditional || poem.title_simplified || "") : (poem.title_simplified || ""); }
function getAuthor(poem) { return scriptMode === "traditional" ? (poem.author_traditional || poem.author_simplified || "") : (poem.author_simplified || ""); }
function getContent(poem) { return scriptMode === "traditional" ? (poem.content_traditional || poem.content_simplified || "") : (poem.content_simplified || ""); }
function updateTopNavButtons(currentView) {
    const map = {
        landing: "navCloud",
        discover: "navDiscover",
        favorites: "navFavorites",
    };
    Object.entries(map).forEach(([view, id]) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.style.display = view === currentView ? "none" : "inline-flex";
    });
}
function setView(name) {
    ["landing", "discover", "favorites"].forEach((v) => document.getElementById(`${v}View`).classList.toggle("active", v === name));
    updateTopNavButtons(name);
}
function updateScriptButton() {
    const label = document.getElementById("scriptModeLabel");
    const btn = document.getElementById("scriptToggle");
    const isTraditional = scriptMode === "traditional";
    if (label) label.textContent = isTraditional ? "繁" : "简";
    if (btn) {
        btn.title = isTraditional ? "当前繁体，点击切换简体" : "当前简体，点击切换繁体";
        btn.setAttribute("aria-label", btn.title);
    }
}
function saveFavorites() { localStorage.setItem(STORAGE_KEY_FAVORITES, JSON.stringify(favorites)); }

function createHeartSvg() {
    return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.2-4.4-9-8.1C.7 9.9 1.5 5.8 5.2 4.4c2.4-.9 4.6-.1 6 1.6 1.5-1.7 3.7-2.5 6-1.6 3.7 1.4 4.5 5.5 2.2 8.5C18.2 16.6 12 21 12 21z"></path></svg>';
}

function createSeededRandom(seed) {
    let s = seed >>> 0;
    return () => {
        s = (s * 1664525 + 1013904223) >>> 0;
        return s / 4294967296;
    };
}

// ============================================================
// Section 3: Word cloud rendering
// ============================================================
// Render one ellipse word cloud with deterministic placement.
function renderCloud(elId, words, seed) {
    const root = document.getElementById(elId);
    if (!root) return;
    root.innerHTML = "";
    const rand = createSeededRandom(seed);
    const sourceWords = Array.isArray(words) && words.length ? words : [["空白", 10, "#7aa7ff"]];
    const maxWeight = Math.max(...sourceWords.map((x) => Number(x[1]) || 10));
    const minWeight = Math.min(...sourceWords.map((x) => Number(x[1]) || 10));
    const placed = [];
    const rootWidth = root.clientWidth || 420;
    const rootHeight = root.clientHeight || 230;
    const centerX = rootWidth / 2;
    const centerY = rootHeight / 2;
    const measureCanvas = document.createElement("canvas");
    const measureCtx = measureCanvas.getContext("2d");

    function overlap(a, b) {
        return !(a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom);
    }

    function estimateRect(text, fontSize) {
        let width = Math.max(26, text.length * fontSize * 1.02);
        if (measureCtx) {
            measureCtx.font = `700 ${fontSize}px "Noto Serif SC","Songti SC","STSong",serif`;
            width = Math.max(26, measureCtx.measureText(text).width + 2);
        }
        const height = fontSize * 1.18;
        return { width, height };
    }

    function inEllipse(rect) {
        const rx = rootWidth * 0.5 - 14;
        const ry = rootHeight * 0.5 - 12;
        const cx = rootWidth * 0.5;
        const cy = rootHeight * 0.5;
        const points = [
            { x: rect.left, y: rect.top },
            { x: rect.right, y: rect.top },
            { x: rect.left, y: rect.bottom },
            { x: rect.right, y: rect.bottom }
        ];
        return points.every((p) => {
            const nx = (p.x - cx) / rx;
            const ny = (p.y - cy) / ry;
            return nx * nx + ny * ny <= 1;
        });
    }

    function scoreRatio(weight) {
        if (maxWeight === minWeight) return 1;
        return (weight - minWeight) / (maxWeight - minWeight);
    }

    function scoreColor(weight) {
        const ratio = scoreRatio(weight);
        const hue = 210 - Math.round(ratio * 150);
        const saturation = 74;
        const lightness = 78 - Math.round(ratio * 30);
        return `hsl(${hue} ${saturation}% ${lightness}%)`;
    }

    function clamp(v, min, max) {
        return Math.max(min, Math.min(max, v));
    }

    function computeTiltAngle(rect) {
        const itemCx = (rect.left + rect.right) / 2;
        const itemCy = (rect.top + rect.bottom) / 2;
        const dx = itemCx - centerX;
        const dy = itemCy - centerY;
        const maxRadius = Math.hypot(centerX, centerY) || 1;
        const distRatio = Math.min(1, Math.hypot(dx, dy) / maxRadius);
        const absAngle = 2 + distRatio * 10;

        // Quadrant-based direction:
        // Q1(+,-) / Q3(-,+) tilt one way, Q2(-,-) / Q4(+,+) tilt the opposite way.
        const sameSign = (dx >= 0 && dy >= 0) || (dx < 0 && dy < 0);
        return sameSign ? absAngle : -absAngle;
    }

    // Simple and fast uniform placement: golden-angle spiral from center to edge.
    function tryPlaceUniform(size, angleOffset) {
        const maxRadius = Math.max(rootWidth, rootHeight);
        const radialStep = denseMode ? 2.1 : 3.2;
        const goldenAngle = 2.399963229728653;
        let theta = angleOffset;

        for (let r = 0; r < maxRadius; r += radialStep) {
            const x = centerX + r * Math.cos(theta) - size.width / 2;
            const y = centerY + r * Math.sin(theta) - size.height / 2;
            const left = clamp(Math.round(x), 0, Math.max(0, rootWidth - size.width - 2));
            const top = clamp(Math.round(y), 0, Math.max(0, rootHeight - size.height - 2));
            const rect = { left, top, right: left + size.width, bottom: top + size.height };
            const hit = placed.some((p) => overlap(rect, p));
            if (!hit && inEllipse(rect)) return rect;
            theta += goldenAngle;
        }
        return null;
    }

    const sorted = [...sourceWords].sort((a, b) => (Number(b[1]) || 0) - (Number(a[1]) || 0));
    const itemCount = sorted.length;
    const denseMode = itemCount >= 90;
    const maxFontSize = denseMode ? 18 : (itemCount >= 60 ? 30 : 47);
    const baseFontSize = denseMode ? 7 : (itemCount >= 60 ? 10 : 13);
    sorted.forEach(([text, weight, color]) => {
        const item = document.createElement("button");
        item.type = "button";
        item.className = "word-item";
        const numericWeight = Number(weight) || 10;
        const weightRatio = scoreRatio(numericWeight);
        const centerBoost = denseMode ? 1.14 : 1.1;
        // Hard score tiers (no smoothing): higher score gets distinctly larger font.
        let tierBoost = 0;
        if (weightRatio >= 0.95) tierBoost = denseMode ? 20 : 24;
        else if (weightRatio >= 0.9) tierBoost = denseMode ? 16 : 19;
        else if (weightRatio >= 0.85) tierBoost = denseMode ? 10 : 13;
        else if (weightRatio >= 0.8) tierBoost = denseMode ? 8 : 12;
        else if (weightRatio >= 0.7) tierBoost = denseMode ? 5 : 7;
        let fontSize = Math.round((baseFontSize + weightRatio * (maxFontSize - baseFontSize)) * centerBoost + tierBoost);
        item.style.color = color || scoreColor(numericWeight);
        item.textContent = text;
        item.title = `点击检索「${text}」`;
        item.addEventListener("click", () => triggerCloudSearch(text));

        let chosen = null;
        let size = null;
        while (!chosen && fontSize >= baseFontSize) {
            size = estimateRect(text, fontSize);
            chosen = tryPlaceUniform(size, rand() * Math.PI * 2);
            if (!chosen) fontSize -= 1;
        }

        if (!chosen) {
            return;
        }

        item.style.fontSize = `${fontSize}px`;
        placed.push(chosen);
        item.style.left = `${chosen.left}px`;
        item.style.top = `${chosen.top}px`;
        if (denseMode) {
            const softTilt = computeTiltAngle(chosen) * 0.55 + (rand() - 0.5) * 10;
            item.style.transform = `rotate(${softTilt.toFixed(1)}deg)`;
        } else {
            item.style.transform = `rotate(${computeTiltAngle(chosen).toFixed(1)}deg)`;
        }
        root.appendChild(item);
    });
}

function renderLandingClouds() {
    renderCloud("cloud-ci", cloudData.ci, 1103);
    renderCloud("cloud-tang", cloudData.shi, 2207);
    renderCloud("cloud-song", cloudData.poets, 3311);
    renderCloud("cloud-cipai", cloudData.ci_pai, 4417);
}

// ============================================================
// Section 4: Cloud payload normalization and loading
// ============================================================
function normalizeCloudData(payload) {
    const categories = payload?.data?.categories || [];
    const map = {};
    categories.forEach((item) => {
        if (!item?.key || !Array.isArray(item.words)) return;
        const list = item.words
            .map((entry) => {
                if (!Array.isArray(entry) || entry.length < 2) return null;
                return [String(entry[0]), Number(entry[1]) || 10, String(entry[2] || "")];
            })
            .filter(Boolean);
        map[item.key] = list;
    });
    return {
        ci: map.ci?.length ? map.ci : defaultCloudData.ci,
        shi: map.shi?.length ? map.shi : defaultCloudData.shi,
        poets: map.poets?.length ? map.poets : defaultCloudData.poets,
        ci_pai: map.ci_pai?.length ? map.ci_pai : defaultCloudData.ci_pai,
    };
}

// Load cloud payload from backend, with fallback defaults when request fails.
async function loadWordcloudData() {
    try {
        const res = await fetch(wordcloudApiUrl, { signal: AbortSignal.timeout(5000) });
        const payload = await res.json();
        const categories = payload?.data?.categories || [];
        const categoryNameMap = {};
        categories.forEach((item) => {
            if (!item?.key || !item?.name) return;
            categoryNameMap[item.key] = String(item.name);
        });
        applyCloudTitles({
            ci: categoryNameMap.ci,
            shi: categoryNameMap.shi,
            poets: categoryNameMap.poets,
            ci_pai: categoryNameMap.ci_pai
        });
        cloudData = normalizeCloudData(payload);
    } catch {
        applyCloudTitles(defaultCloudTitles);
        cloudData = { ...defaultCloudData };
    }
    renderLandingClouds();
}

// ============================================================
// Section 5: Discover/Favorites rendering
// ============================================================
async function triggerCloudSearch(word) {
    await loadFilterMeta();
    setView("discover");
    document.getElementById("keywordInput").value = word || "";
    document.getElementById("authorInput").value = "";
    document.getElementById("tagInput").value = "";
    document.getElementById("dynastySelect").value = "";
    document.getElementById("categorySelect").value = "";
    document.getElementById("sortSelect").value = "default";
    activeHot = "";
    currentPageSize = Math.min(Math.max(Number(poemsApi.pageSize || 20), 1), 100);
    document.getElementById("pageInput").value = "1";
    syncPageSizeButtons();
    const discoverView = document.getElementById("discoverView");
    if (discoverView) {
        const top = Math.max(0, discoverView.getBoundingClientRect().top + window.scrollY - 12);
        window.scrollTo({ top, behavior: "smooth" });
    }
    await applyFilters();
}

function renderCard(poem, favView = false) {
    const card = document.createElement("article");
    const key = keyOf(poem);
    card.className = "poem-card";
    card.innerHTML = `
        <button class="heart-btn ${favorites[key] ? "active" : ""}" title="收藏">${createHeartSvg()}</button>
        <h3 class="poem-title">${getTitle(poem)}</h3>
        <p class="poem-author">${poem.dynasty ? poem.dynasty + " · " : ""}${getAuthor(poem)}${poem.category ? " · " + poem.category : ""}</p>
        <div class="poem-content">${getContent(poem)}</div>
    `;
    card.querySelector(".heart-btn").addEventListener("click", () => {
        if (favorites[key]) delete favorites[key];
        else {
            favorites[key] = {
                id: poem.id,
                title_simplified: poem.title_simplified,
                title_traditional: poem.title_traditional || poem.title_simplified,
                author_simplified: poem.author_simplified,
                author_traditional: poem.author_traditional || poem.author_simplified,
                dynasty: poem.dynasty,
                category: poem.category,
                content_simplified: poem.content_simplified || "",
                content_traditional: poem.content_traditional || poem.content_simplified || "",
            };
        }
        saveFavorites();
        renderDiscover();
        renderFavorites();
        if (favView && !favorites[key]) card.remove();
    });
    return card;
}

function buildHotWords(list) {
    const map = {};
    list.forEach((p) => String(p.tags || "").split(/[，,、\s]+/).filter(Boolean).forEach((w) => map[w] = (map[w] || 0) + 1));
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 15).map((x) => x[0]);
}

function renderHotWords(list) {
    const root = document.getElementById("hotKeywords");
    root.innerHTML = "";
    const hotWords = buildHotWords(list);
    if (!hotWords.length) {
        root.classList.add("is-empty");
        const empty = document.createElement("span");
        empty.className = "chip-empty";
        empty.textContent = "当前结果暂无高频标签";
        root.appendChild(empty);
        return;
    }
    root.classList.remove("is-empty");
    hotWords.forEach((w) => {
        const chip = document.createElement("button");
        chip.className = `chip ${activeHot === w ? "active" : ""}`;
        chip.textContent = w;
        chip.addEventListener("click", () => {
            activeHot = activeHot === w ? "" : w;
            document.getElementById("tagInput").value = activeHot;
            applyFilters();
        });
        root.appendChild(chip);
    });
}

function escapeAttr(s) {
    return String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
}

function renderSelects() {
    document.getElementById("dynastySelect").innerHTML =
        '<option value="">全部朝代</option>' +
        metaDynasties.map((d) => `<option value="${escapeAttr(d)}">${escapeAttr(d)}</option>`).join("");
    document.getElementById("categorySelect").innerHTML =
        '<option value="">全部分类</option>' +
        metaCategories.map((c) => `<option value="${escapeAttr(c)}">${escapeAttr(c)}</option>`).join("");
}

function sortFavoritesList(list) {
    const mode = document.getElementById("sortSelect").value;
    const arr = [...list];
    if (mode === "title_asc") arr.sort((a, b) => getTitle(a).localeCompare(getTitle(b), "zh-Hans-CN"));
    if (mode === "author_asc") arr.sort((a, b) => (a.author_simplified || "").localeCompare(b.author_simplified || "", "zh-Hans-CN"));
    if (mode === "dynasty_asc") arr.sort((a, b) => (a.dynasty || "").localeCompare(b.dynasty || "", "zh-Hans-CN"));
    return arr;
}

async function loadFilterMeta() {
    if (filterMetaLoaded) return;
    try {
        const [cRes, dRes] = await Promise.all([
            fetch(`${apiBaseUrl}/poems/meta/categories`, { signal: AbortSignal.timeout(8000) }),
            fetch(`${apiBaseUrl}/poems/meta/dynasties`, { signal: AbortSignal.timeout(8000) }),
        ]);
        const cJson = await cRes.json();
        const dJson = await dRes.json();
        metaCategories = Array.isArray(cJson?.data) ? cJson.data : [];
        metaDynasties = Array.isArray(dJson?.data) ? dJson.data : [];
    } catch {
        metaCategories = [];
        metaDynasties = [];
    }
    filterMetaLoaded = true;
    renderSelects();
}

function syncPageSizeButtons() {
    const root = document.getElementById("pageSizeGroup");
    if (!root) return;
    root.querySelectorAll("button[data-page-size]").forEach((btn) => {
        btn.classList.toggle("active", Number(btn.getAttribute("data-page-size")) === currentPageSize);
    });
}

function totalPagesFromTotal() {
    if (listTotal <= 0) return 1;
    return Math.max(1, Math.ceil(listTotal / currentPageSize));
}

function updatePagerChrome() {
    const tp = totalPagesFromTotal();
    const pageInput = document.getElementById("pageInput");
    const totalLabel = document.getElementById("pageTotalLabel");
    const prev = document.getElementById("pagePrev");
    const next = document.getElementById("pageNext");
    if (pageInput) pageInput.value = String(currentPage);
    if (totalLabel) totalLabel.textContent = String(tp);
    if (prev) prev.disabled = currentPage <= 1 || listLoading;
    if (next) next.disabled = currentPage >= tp || listLoading || listTotal === 0;
    syncPageSizeButtons();
}

function buildListQueryString() {
    const qs = new URLSearchParams();
    qs.set("page", String(currentPage));
    qs.set("page_size", String(currentPageSize));
    const keyword = (document.getElementById("keywordInput").value || "").trim();
    const author = (document.getElementById("authorInput").value || "").trim();
    const tag = (document.getElementById("tagInput").value || "").trim();
    const dynasty = document.getElementById("dynastySelect").value;
    const category = document.getElementById("categorySelect").value;
    const sort = document.getElementById("sortSelect").value || "default";
    if (keyword) qs.set("keyword", keyword);
    if (author) qs.set("author", author);
    if (tag) qs.set("tag", tag);
    if (dynasty) qs.set("dynasty", dynasty);
    if (category) qs.set("category", category);
    if (sort && sort !== "default") qs.set("sort", sort);
    return qs.toString();
}

async function fetchPoemList({ resetPage = false } = {}) {
    if (resetPage) currentPage = 1;
    listLoading = true;
    const metaEl = document.getElementById("resultMeta");
    if (metaEl) metaEl.textContent = "加载中…";
    updatePagerChrome();
    const qs = buildListQueryString();
    try {
        const res = await fetch(`${apiBaseUrl}/poems?${qs}`, { signal: AbortSignal.timeout(20000) });
        const payload = await res.json();
        poems = payload?.data?.items || [];
        listTotal = Number(payload?.data?.total) || 0;
        const tp = totalPagesFromTotal();
        if (listTotal > 0 && currentPage > tp) {
            currentPage = tp;
            listLoading = false;
            return fetchPoemList({ resetPage: false });
        }
        if (listTotal === 0) currentPage = 1;
    } catch {
        poems = [...fallback];
        listTotal = poems.length;
        currentPage = 1;
    }
    listLoading = false;
    updatePagerChrome();
    return poems;
}

function renderResultSummary() {
    const el = document.getElementById("resultMeta");
    if (!el) return;
    if (listLoading) {
        el.textContent = "加载中…";
        return;
    }
    const tp = totalPagesFromTotal();
    const start = listTotal === 0 ? 0 : (currentPage - 1) * currentPageSize + 1;
    const end = listTotal === 0 ? 0 : Math.min(listTotal, currentPage * currentPageSize);
    el.innerHTML =
        listTotal === 0
            ? "暂无数据（可放宽筛选或检查接口）"
            : `共 <strong>${listTotal}</strong> 条 · 本页 <strong>${start}–${end}</strong> · 第 <strong>${currentPage}</strong> / ${tp} 页 · 每页 <strong>${currentPageSize}</strong> 条`;
}

async function applyFilters() {
    await fetchPoemList({ resetPage: true });
    renderHotWords(poems);
    renderDiscover();
}

function renderDiscover() {
    const grid = document.getElementById("poemGrid");
    grid.innerHTML = "";
    poems.forEach((p) => grid.appendChild(renderCard(p)));
    document.getElementById("discoverEmpty").style.display = listTotal ? "none" : "block";
    renderResultSummary();
    updatePagerChrome();
    updateScriptButton();
}

function favoriteEntryToPoem(entry) {
    return {
        id: entry.id,
        title_simplified: entry.title_simplified,
        title_traditional: entry.title_traditional,
        author_simplified: entry.author_simplified,
        author_traditional: entry.author_traditional,
        dynasty: entry.dynasty,
        category: entry.category,
        content_simplified: entry.content_simplified || "",
        content_traditional: entry.content_traditional || "",
        tags: "",
    };
}

function renderFavorites() {
    const favList = sortFavoritesList(Object.values(favorites).map(favoriteEntryToPoem));
    const grid = document.getElementById("favoritesGrid");
    grid.innerHTML = "";
    favList.forEach((p) => grid.appendChild(renderCard(p, true)));
    document.getElementById("favoritesEmpty").style.display = favList.length ? "none" : "block";
}

async function ensureDiscoverData() {
    await loadFilterMeta();
    await fetchPoemList({ resetPage: false });
    renderHotWords(poems);
}

function resetFilters() {
    ["keywordInput", "authorInput", "tagInput"].forEach((id) => {
        document.getElementById(id).value = "";
    });
    ["dynastySelect", "categorySelect", "sortSelect"].forEach((id) => {
        document.getElementById(id).value = id === "sortSelect" ? "default" : "";
    });
    activeHot = "";
    currentPage = 1;
    currentPageSize = Math.min(Math.max(Number(poemsApi.pageSize || 20), 1), 100);
    document.getElementById("pageInput").value = "1";
    syncPageSizeButtons();
    fetchPoemList({ resetPage: true }).then(() => {
        renderHotWords(poems);
        renderDiscover();
    });
}

// ============================================================
// Section 6: Event wiring and bootstrap
// ============================================================
function bindEvents() {
    const navCloud = document.getElementById("navCloud");
    const navDiscover = document.getElementById("navDiscover");
    const navFavorites = document.getElementById("navFavorites");
    if (navCloud) navCloud.addEventListener("click", () => setView("landing"));
    if (navDiscover) {
        navDiscover.addEventListener("click", async () => {
            await ensureDiscoverData();
            setView("discover");
            renderDiscover();
        });
    }
    if (navFavorites) {
        navFavorites.addEventListener("click", () => {
            setView("favorites");
            renderFavorites();
        });
    }
    document.getElementById("searchBtn").addEventListener("click", () => applyFilters());
    document.getElementById("resetBtn").addEventListener("click", resetFilters);
    document.getElementById("sortSelect").addEventListener("change", () => applyFilters());
    const pageSizeGroup = document.getElementById("pageSizeGroup");
    if (pageSizeGroup) {
        pageSizeGroup.addEventListener("click", async (e) => {
            const btn = e.target.closest("button[data-page-size]");
            if (!btn) return;
            const sz = Number(btn.getAttribute("data-page-size"));
            if (!Number.isFinite(sz) || sz < 1 || sz > 100 || sz === currentPageSize) return;
            currentPageSize = sz;
            currentPage = 1;
            await fetchPoemList({ resetPage: true });
            renderHotWords(poems);
            renderDiscover();
        });
    }
    document.getElementById("pageInput").addEventListener("change", async () => {
        const pageInput = document.getElementById("pageInput");
        const next = Number(pageInput.value || 1);
        const tp = totalPagesFromTotal();
        const v = Number.isFinite(next) && next > 0 ? Math.floor(next) : 1;
        currentPage = Math.min(Math.max(1, v), tp);
        await fetchPoemList({ resetPage: false });
        renderHotWords(poems);
        renderDiscover();
    });
    const pagePrev = document.getElementById("pagePrev");
    const pageNext = document.getElementById("pageNext");
    if (pagePrev) {
        pagePrev.addEventListener("click", async () => {
            if (currentPage <= 1) return;
            currentPage -= 1;
            await fetchPoemList({ resetPage: false });
            renderHotWords(poems);
            renderDiscover();
        });
    }
    if (pageNext) {
        pageNext.addEventListener("click", async () => {
            const tp = totalPagesFromTotal();
            if (currentPage >= tp || listTotal === 0) return;
            currentPage += 1;
            await fetchPoemList({ resetPage: false });
            renderHotWords(poems);
            renderDiscover();
        });
    }
    document.getElementById("scriptToggle").addEventListener("click", () => {
        scriptMode = scriptMode === "simplified" ? "traditional" : "simplified";
        localStorage.setItem(STORAGE_KEY_SCRIPT, scriptMode);
        renderDiscover();
        renderFavorites();
        updateScriptButton();
    });
    document.getElementById("exportFavoritesBtn").addEventListener("click", () => {
        const exportBtn = document.getElementById("exportFavoritesBtn");
        const exportRoot = document.getElementById("favoritesExport");
        if ((exportRoot.textContent || "").trim()) {
            exportRoot.textContent = "";
            exportBtn.textContent = "导出收藏 JSON";
            return;
        }
        const output = Object.values(favorites).map((f) => ({
            id: f.id,
            title_simplified: f.title_simplified,
            title_traditional: f.title_traditional,
            author_simplified: f.author_simplified,
            author_traditional: f.author_traditional,
            dynasty: f.dynasty,
            category: f.category,
            favorite: true,
        }));
        exportRoot.textContent = JSON.stringify(output, null, 2);
        exportBtn.textContent = "隐藏导出结果";
    });
    document.getElementById("clearFavoritesBtn").addEventListener("click", () => {
        favorites = {};
        saveFavorites();
        document.getElementById("favoritesExport").textContent = "";
        document.getElementById("exportFavoritesBtn").textContent = "导出收藏 JSON";
        renderDiscover();
        renderFavorites();
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadWordcloudData();
    updateScriptButton();
    updateTopNavButtons("landing");
    syncPageSizeButtons();
    bindEvents();
});
