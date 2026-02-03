// --- State Management ---
const state = {
    funds: [],
    filter: 'all',
    search: '',
    loading: true
};

// --- Mock Data Generator ---
function generateData() {
    const types = ["股票型", "混合型", "债券型", "指数型"];
    const names_prefix = ["华夏", "易方达", "汇添富", "广发", "南方"];
    const names_suffix = ["成长", "价值", "创新", "科技", "消费"];
    const data = [];

    for (let i = 0; i < 95; i++) {
        const fType = types[Math.floor(Math.random() * types.length)];
        const name = `${names_prefix[Math.floor(Math.random() * names_prefix.length)]}${names_suffix[Math.floor(Math.random() * names_suffix.length)]}${fType}`;
        const nav = (Math.random() * 4 + 0.5);
        const growth = (Math.random() * 10 - 5);
        
        data.push({
            code: Math.floor(Math.random() * 1000000).toString().padStart(6, '0'),
            name: name,
            nav: nav,
            estimated_nav: nav * (1 + growth/100),
            growth_rate: parseFloat(growth.toFixed(2)),
            last_update: new Date().toISOString().replace('T', ' ').substring(0, 19),
            type: fType
        });
    }
    return data;
}

// --- Render Functions ---
function renderList() {
    const tbody = document.getElementById('fund-table-body');
    const totalCountEl = document.getElementById('total-count');
    tbody.innerHTML = '';

    let filtered = state.funds.filter(f => {
        const matchesType = state.filter === 'all' || f.type === state.filter;
        const matchesSearch = !state.search || f.name.includes(state.search) || f.code.includes(state.search);
        return matchesType && matchesSearch;
    });

    totalCountEl.textContent = filtered.length;

    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:3rem; color:var(--text-secondary)">未找到匹配的基金</td></tr>';
        return;
    }

    // Simple pagination (show top 20 for demo)
    filtered = filtered.slice(0, 20);

    filtered.forEach(fund => {
        const isUp = fund.growth_rate > 0;
        const trendClass = isUp ? 'trend-up' : (fund.growth_rate < 0 ? 'trend-down' : '');
        const sign = isUp ? '+' : '';
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="code-cell">${fund.code}</td>
            <td style="font-weight:500">${fund.name}</td>
            <td><span class="badge">${fund.type}</span></td>
            <td>${fund.nav.toFixed(4)}</td>
            <td>${fund.estimated_nav.toFixed(4)}</td>
            <td class="${trendClass}">${sign}${fund.growth_rate}%</td>
            <td style="color:var(--text-secondary); font-size:0.9rem">${fund.last_update.split(' ')[1]}</td>
        `;
        tr.onclick = () => showDetail(fund);
        tbody.appendChild(tr);
    });
}

function showDetail(fund) {
    const detailContainer = document.getElementById('detail-container');
    const isUp = fund.growth_rate > 0;
    const trendClass = isUp ? 'trend-up' : (fund.growth_rate < 0 ? 'trend-down' : '');
    
    // Generate chart bars
    let chartHtml = '';
    for(let i=0; i<30; i++) {
        const h = 20 + Math.random() * 80;
        const color = h > 50 ? '#ef4444' : '#10b981';
        chartHtml += `<div class="chart-bar" style="height:${h}%; background:${color}"></div>`;
    }

    detailContainer.innerHTML = `
        <div class="detail-header" style="margin-bottom:2rem">
            <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.5rem">
                <h2>${fund.name}</h2>
                <span class="badge" style="font-size:1rem">${fund.type}</span>
            </div>
            <div style="color:var(--text-secondary); font-family:monospace; font-size:1.2rem">代码: ${fund.code}</div>
        </div>

        <div class="market-overview">
            <div class="overview-card">
                <div class="icon-box" style="background:#e0f2fe; color:#3b82f6">💰</div>
                <div>
                    <h3 style="margin:0 0 5px 0; color:var(--text-secondary)">当前单位净值</h3>
                    <div class="card-value">${fund.nav.toFixed(4)}</div>
                    <div style="font-size:0.9rem; color:var(--text-secondary)">昨日收盘</div>
                </div>
            </div>
            <div class="overview-card">
                <div class="icon-box" style="background:${isUp ? '#fef2f2' : '#ecfdf5'}; color:${isUp ? '#ef4444' : '#10b981'}">📊</div>
                <div>
                    <h3 style="margin:0 0 5px 0; color:var(--text-secondary)">实时估算净值</h3>
                    <div class="card-value ${trendClass}">${fund.estimated_nav.toFixed(4)}</div>
                    <div class="${trendClass}" style="font-size:0.9rem">${fund.growth_rate > 0 ? '+' : ''}${fund.growth_rate}%</div>
                </div>
            </div>
             <div class="overview-card">
                <div class="icon-box" style="background:#f3e8ff; color:#8b5cf6">🕒</div>
                <div>
                    <h3 style="margin:0 0 5px 0; color:var(--text-secondary)">数据更新时间</h3>
                    <div class="card-value" style="font-size:1.5rem">${fund.last_update.split(' ')[1]}</div>
                     <div style="font-size:0.9rem; color:var(--text-secondary)">${fund.last_update.split(' ')[0]}</div>
                </div>
            </div>
        </div>

        <div class="detail-content">
            <h3 style="margin-top:0">业绩走势 (模拟)</h3>
            <div class="chart-placeholder">
                ${chartHtml}
            </div>
        </div>
    `;
    
    toggleView('detail');
}

function toggleView(viewName) {
    if (viewName === 'detail') {
        document.getElementById('view-list').classList.add('hidden');
        document.getElementById('view-detail').classList.remove('hidden');
        window.scrollTo(0,0);
    } else {
        document.getElementById('view-detail').classList.add('hidden');
        document.getElementById('view-list').classList.remove('hidden');
    }
}

// --- Init & Events ---
document.addEventListener('DOMContentLoaded', () => {
    // Generate Data
    state.funds = generateData();
    renderList();

    // Search Event
    document.getElementById('search-input').addEventListener('input', (e) => {
        state.search = e.target.value;
        renderList();
    });

    // Filter Event
    document.getElementById('filter-container').addEventListener('click', (e) => {
        if (e.target.classList.contains('filter-btn')) {
            // Update Active State
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            // Update Filter State
            state.filter = e.target.getAttribute('data-type');
            renderList();
        }
    });

    // Back Button
    document.getElementById('btn-back-to-list').addEventListener('click', () => {
        toggleView('list');
    });
});
