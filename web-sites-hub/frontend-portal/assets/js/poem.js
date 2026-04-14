// ============================================================
// Section 1: Runtime config and page state
// ============================================================
// Poems page runtime entry.
// Reads API config from window.POEMS_API (injected by poem.config.js).
const poemsApi = window.POEMS_API || {};
const apiBaseUrl = poemsApi.baseUrl || "http://127.0.0.1:8300/api/v1";
const pageSize = Math.min(Number(poemsApi.pageSize || 100), 100);
const apiUrl = `${apiBaseUrl}/poems?page=1&page_size=${pageSize}`;
const wordcloudApiUrl = `${apiBaseUrl}/poems/meta/wordcloud`;
const STORAGE_KEY_FAVORITES = "poems-favorites-v1";
const STORAGE_KEY_SCRIPT = "poems-script-mode";
let scriptMode = localStorage.getItem(STORAGE_KEY_SCRIPT) || "simplified";
let poems = [];
let filtered = [];
let loaded = false;
let favorites = JSON.parse(localStorage.getItem(STORAGE_KEY_FAVORITES) || "{}");
let activeHot = "";
let currentPage = 1;
let currentPageSize = 20;

const fallback = [
    { title: "定风波", title_simplified: "定风波", title_traditional: "定風波", author: "苏轼", dynasty: "宋", category: "宋词", tags: "豁达", content_simplified: "莫听穿林打叶声，何妨吟啸且徐行。", content_traditional: "莫聽穿林打葉聲，何妨吟嘯且徐行。" },
    { title: "将进酒", title_simplified: "将进酒", title_traditional: "將進酒", author: "李白", dynasty: "唐", category: "古诗", tags: "豪放", content_simplified: "君不见，黄河之水天上来。", content_traditional: "君不見，黃河之水天上來。" }
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

function keyOf(poem) { return `${poem.title_simplified || poem.title}__${poem.author}`; }
function getTitle(poem) { return scriptMode === "traditional" ? (poem.title_traditional || poem.title) : (poem.title_simplified || poem.title); }
function getContent(poem) { return scriptMode === "traditional" ? (poem.content_traditional || poem.content || "") : (poem.content_simplified || poem.content || ""); }
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
function updateScriptButton() { document.getElementById("scriptToggle").textContent = scriptMode === "traditional" ? "繁体" : "简体"; }
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
    await ensureLoaded();
    setView("discover");
    document.getElementById("keywordInput").value = word || "";
    document.getElementById("tagInput").value = "";
    activeHot = "";
    applyFilters();
}

function renderCard(poem, favView = false) {
    const card = document.createElement("article");
    const key = keyOf(poem);
    card.className = "poem-card";
    card.innerHTML = `
        <button class="heart-btn ${favorites[key] ? "active" : ""}" title="收藏">${createHeartSvg()}</button>
        <h3 class="poem-title">${getTitle(poem)}</h3>
        <p class="poem-author">${poem.dynasty ? poem.dynasty + " · " : ""}${poem.author}${poem.category ? " · " + poem.category : ""}</p>
        <div class="poem-content">${getContent(poem)}</div>
    `;
    card.querySelector(".heart-btn").addEventListener("click", () => {
        if (favorites[key]) delete favorites[key];
        else favorites[key] = { id: poem.id, title_simplified: poem.title_simplified || poem.title, title_traditional: poem.title_traditional || poem.title, author: poem.author, dynasty: poem.dynasty, category: poem.category };
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
    buildHotWords(list).forEach((w) => {
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

function renderSelects() {
    const dSet = [...new Set(poems.map((p) => p.dynasty).filter(Boolean))].sort();
    const cSet = [...new Set(poems.map((p) => p.category).filter(Boolean))].sort();
    document.getElementById("dynastySelect").innerHTML = '<option value="">全部朝代</option>' + dSet.map((d) => `<option value="${d}">${d}</option>`).join("");
    document.getElementById("categorySelect").innerHTML = '<option value="">全部分类</option>' + cSet.map((c) => `<option value="${c}">${c}</option>`).join("");
}

function sortPoems(list) {
    const mode = document.getElementById("sortSelect").value;
    const arr = [...list];
    if (mode === "title_asc") arr.sort((a, b) => getTitle(a).localeCompare(getTitle(b), "zh-Hans-CN"));
    if (mode === "author_asc") arr.sort((a, b) => (a.author || "").localeCompare(b.author || "", "zh-Hans-CN"));
    if (mode === "dynasty_asc") arr.sort((a, b) => (a.dynasty || "").localeCompare(b.dynasty || "", "zh-Hans-CN"));
    return arr;
}

function applyFilters() {
    const keyword = (document.getElementById("keywordInput").value || "").trim();
    const author = (document.getElementById("authorInput").value || "").trim();
    const tag = (document.getElementById("tagInput").value || "").trim();
    const dynasty = document.getElementById("dynastySelect").value;
    const category = document.getElementById("categorySelect").value;
    filtered = poems.filter((p) => {
        const text = `${p.title} ${p.title_simplified || ""} ${p.title_traditional || ""} ${p.author || ""} ${p.content_simplified || ""} ${p.content_traditional || ""} ${p.tags || ""}`;
        return (!keyword || text.includes(keyword)) && (!author || (p.author || "").includes(author)) && (!tag || (p.tags || "").includes(tag)) && (!dynasty || p.dynasty === dynasty) && (!category || p.category === category);
    });
    filtered = sortPoems(filtered);
    currentPage = 1;
    const pageInput = document.getElementById("pageInput");
    if (pageInput) pageInput.value = String(currentPage);
    renderHotWords(filtered.length ? filtered : poems);
    renderDiscover();
}

function renderDiscover() {
    const grid = document.getElementById("poemGrid");
    grid.innerHTML = "";
    const pageSizeSelect = document.getElementById("pageSizeSelect");
    const pageInput = document.getElementById("pageInput");
    if (pageSizeSelect) {
        const parsedSize = Number(pageSizeSelect.value || currentPageSize);
        currentPageSize = Number.isFinite(parsedSize) && parsedSize > 0 ? parsedSize : 20;
    }
    const totalPages = Math.max(1, Math.ceil(filtered.length / currentPageSize));
    currentPage = Math.min(Math.max(1, currentPage), totalPages);
    if (pageInput) pageInput.value = String(currentPage);
    const start = (currentPage - 1) * currentPageSize;
    const end = start + currentPageSize;
    filtered.slice(start, end).forEach((p) => grid.appendChild(renderCard(p)));
    document.getElementById("discoverEmpty").style.display = filtered.length ? "none" : "block";
    document.getElementById("resultMeta").textContent = `筛选结果 ${filtered.length} / 总数 ${poems.length} · 第 ${currentPage}/${totalPages} 页`;
    updateScriptButton();
}

function renderFavorites() {
    const favList = poems.filter((p) => favorites[keyOf(p)]);
    const grid = document.getElementById("favoritesGrid");
    grid.innerHTML = "";
    favList.forEach((p) => grid.appendChild(renderCard(p, true)));
    document.getElementById("favoritesEmpty").style.display = favList.length ? "none" : "block";
}

async function ensureLoaded() {
    if (loaded) return;
    try {
        const res = await fetch(apiUrl, { signal: AbortSignal.timeout(5000) });
        const payload = await res.json();
        poems = payload?.data?.items || [];
        if (!poems.length) poems = fallback;
    } catch {
        poems = fallback;
    }
    loaded = true;
    filtered = [...poems];
    renderSelects();
    renderHotWords(poems);
}

function resetFilters() {
    ["keywordInput", "authorInput", "tagInput"].forEach((id) => document.getElementById(id).value = "");
    ["dynastySelect", "categorySelect", "sortSelect"].forEach((id) => document.getElementById(id).value = id === "sortSelect" ? "default" : "");
    activeHot = "";
    currentPage = 1;
    currentPageSize = 20;
    const pageInput = document.getElementById("pageInput");
    if (pageInput) pageInput.value = "1";
    const pageSizeSelect = document.getElementById("pageSizeSelect");
    if (pageSizeSelect) pageSizeSelect.value = "20";
    filtered = sortPoems([...poems]);
    renderHotWords(poems);
    renderDiscover();
}

// ============================================================
// Section 6: Event wiring and bootstrap
// ============================================================
function bindEvents() {
    const navCloud = document.getElementById("navCloud");
    const navDiscover = document.getElementById("navDiscover");
    const navFavorites = document.getElementById("navFavorites");
    if (navCloud) navCloud.addEventListener("click", () => setView("landing"));
    if (navDiscover) navDiscover.addEventListener("click", async () => { await ensureLoaded(); setView("discover"); renderDiscover(); });
    if (navFavorites) navFavorites.addEventListener("click", async () => { await ensureLoaded(); setView("favorites"); renderFavorites(); });
    document.getElementById("backDiscoverBtn").addEventListener("click", () => setView("discover"));
    document.getElementById("backLandingFromFav").addEventListener("click", () => setView("landing"));
    document.getElementById("searchBtn").addEventListener("click", applyFilters);
    document.getElementById("resetBtn").addEventListener("click", resetFilters);
    document.getElementById("sortSelect").addEventListener("change", applyFilters);
    document.getElementById("pageSizeSelect").addEventListener("change", () => {
        currentPage = 1;
        renderDiscover();
    });
    document.getElementById("pageInput").addEventListener("change", () => {
        const pageInput = document.getElementById("pageInput");
        const next = Number(pageInput.value || 1);
        currentPage = Number.isFinite(next) && next > 0 ? Math.floor(next) : 1;
        renderDiscover();
    });
    document.getElementById("scriptToggle").addEventListener("click", () => {
        scriptMode = scriptMode === "simplified" ? "traditional" : "simplified";
        localStorage.setItem(STORAGE_KEY_SCRIPT, scriptMode);
        if (loaded) { renderDiscover(); renderFavorites(); }
        updateScriptButton();
    });
    document.getElementById("exportFavoritesBtn").addEventListener("click", () => {
        const output = poems.filter((p) => favorites[keyOf(p)]).map((p) => ({ id: p.id, title_simplified: p.title_simplified || p.title, title_traditional: p.title_traditional || p.title, author: p.author, dynasty: p.dynasty, category: p.category, favorite: true }));
        document.getElementById("favoritesExport").textContent = JSON.stringify(output, null, 2);
    });
    document.getElementById("clearFavoritesBtn").addEventListener("click", () => {
        favorites = {};
        saveFavorites();
        if (loaded) { renderDiscover(); renderFavorites(); }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadWordcloudData();
    updateScriptButton();
    updateTopNavButtons("landing");
    bindEvents();
});
