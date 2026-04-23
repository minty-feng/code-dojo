/**
 * Gold desk — spot poll, CNY/g helper, position P&L, local alerts.
 * Configure window.FUND_API.baseUrl before this script for a fixed API root.
 */
(function () {
    const OZ_GRAMS = 31.1034768;
    const LS_ALERTS = "gold-desk-alerts-v1";
    const LS_LAST = "gold-desk-last-cross-v1";
    const POLL_MS = 45000;

    const cfg = window.FUND_API || {};

    function resolveApiBaseUrl() {
        const explicit = String(cfg.baseUrl || "").trim();
        if (explicit) return explicit.replace(/\/+$/, "");
        const { protocol, hostname, origin } = window.location;
        const isLocal = hostname === "127.0.0.1" || hostname === "localhost";
        const isFile = protocol === "file:";
        if (isFile || isLocal) return "http://127.0.0.1:8300/api/v1";
        return `${origin}/api/v1`;
    }

    const apiBase = resolveApiBaseUrl();
    const quoteUrl = `${apiBase}/market/gold/quote`;
    const state = {
        lastPrice: null,
        history: [],
        dailyHistory: [],
        dailySummary: null,
        dailySource: "--",
        dailyDemo: true,
        dailyGranularity: "daily",
        historyTab: "chart",
        historyDays: 3650,
        lineUnit: "usd",
        lineHoverIndex: null,
        pollTimer: null,
        lastCross: loadJson(LS_LAST, {}),
    };

    function readNumber(id) {
        const val = Number(document.getElementById(id)?.value);
        return Number.isFinite(val) ? val : NaN;
    }

    function calcCnyPerGram(usdPerOz, fx) {
        if (!Number.isFinite(usdPerOz) || !Number.isFinite(fx) || fx <= 0) return NaN;
        return (usdPerOz / OZ_GRAMS) * fx;
    }

    function getInputState() {
        return {
            fx: readNumber("inp-fx"),
            domesticQuote: readNumber("inp-domestic-quote"),
            grams: readNumber("inp-grams"),
            cost: readNumber("inp-cost"),
            fee: readNumber("inp-fee"),
            planAddTarget: readNumber("inp-plan-add-target"),
            planReduceTarget: readNumber("inp-plan-reduce-target"),
            planStepGrams: readNumber("inp-plan-step-grams"),
            scenarioGold: readNumber("inp-scenario-gold"),
            scenarioFx: readNumber("inp-scenario-fx"),
            scenarioAddGrams: readNumber("inp-scenario-add-grams"),
            scenarioAddPrice: readNumber("inp-scenario-add-price"),
            scenarioFee: readNumber("inp-scenario-fee"),
        };
    }

    function getCurrentMetrics(inputs = getInputState()) {
        const spot = state.lastPrice;
        if (!Number.isFinite(spot)) return null;
        const cnyPerG = calcCnyPerGram(spot, inputs.fx);
        if (!Number.isFinite(cnyPerG)) return null;
        const grams = Number.isFinite(inputs.grams) && inputs.grams >= 0 ? inputs.grams : NaN;
        const cost = Number.isFinite(inputs.cost) && inputs.cost >= 0 ? inputs.cost : NaN;
        const fee = Number.isFinite(inputs.fee) && inputs.fee >= 0 ? inputs.fee : 0;
        const marketVal = Number.isFinite(grams) ? grams * cnyPerG : NaN;
        const costBasis = Number.isFinite(grams) && Number.isFinite(cost) ? grams * cost + fee : NaN;
        const pnl = Number.isFinite(marketVal) && Number.isFinite(costBasis) ? marketVal - costBasis : NaN;
        const pnlPct = Number.isFinite(costBasis) && costBasis > 0 ? (pnl / costBasis) * 100 : NaN;
        return { spot, cnyPerG, grams, cost, fee, marketVal, costBasis, pnl, pnlPct };
    }

    function getHistoryStats() {
        const list = Array.isArray(state.dailyHistory) ? state.dailyHistory : [];
        if (!list.length) return null;
        const closes = list.map((item) => Number(item.close_usd_oz)).filter((v) => Number.isFinite(v) && v > 0);
        if (!closes.length) return null;
        const low = Math.min(...closes);
        const high = Math.max(...closes);
        const first = closes[0];
        const last = closes[closes.length - 1];
        const amplitudePct = low > 0 ? ((high / low) - 1) * 100 : NaN;
        const spanPct = first > 0 ? ((last / first) - 1) * 100 : NaN;
        const current = Number.isFinite(state.lastPrice) ? state.lastPrice : last;
        const positionPct = high > low ? ((current - low) / (high - low)) * 100 : 50;
        return {
            low,
            high,
            firstDate: list[0]?.date || "--",
            lastDate: list[list.length - 1]?.date || "--",
            amplitudePct,
            spanPct,
            positionPct: Math.max(0, Math.min(100, positionPct)),
        };
    }

    function getEstimateStats(inputs = getInputState()) {
        const summary = state.dailySummary;
        if (!summary) return null;
        const expected = Number(summary.next_day_expected ?? summary.next_30m_expected);
        const rangeRaw = summary.next_day_range_1sigma ?? summary.next_30m_range_1sigma;
        const range = Array.isArray(rangeRaw) ? rangeRaw.map((x) => Number(x)) : [expected, expected];
        if (!Number.isFinite(expected) || !range.every((x) => Number.isFinite(x))) return null;
        return {
            expectedUsd: expected,
            rangeUsd: range,
            expectedCny: calcCnyPerGram(expected, inputs.fx),
            rangeCny: range.map((x) => calcCnyPerGram(x, inputs.fx)),
        };
    }

    function buildValuationSignal(inputs = getInputState()) {
        const metrics = getCurrentMetrics(inputs);
        const hist = getHistoryStats();
        const estimate = getEstimateStats(inputs);
        const domestic = Number.isFinite(inputs.domesticQuote) ? inputs.domesticQuote : NaN;
        let score = 0;
        const reasons = [];
        if (metrics && Number.isFinite(domestic)) {
            const premiumPct = ((domestic / metrics.cnyPerG) - 1) * 100;
            if (premiumPct >= 1.5) {
                score += 1;
                reasons.push(`国内报价较理论价高 ${fmtNum(premiumPct, 2)}%`);
            } else if (premiumPct <= -1.5) {
                score -= 1;
                reasons.push(`国内报价较理论价低 ${fmtNum(Math.abs(premiumPct), 2)}%`);
            }
        }
        if (hist) {
            if (hist.positionPct >= 80) {
                score += 1;
                reasons.push(`位于历史区间上沿 ${fmtNum(hist.positionPct, 0)}%`);
            } else if (hist.positionPct <= 20) {
                score -= 1;
                reasons.push(`位于历史区间下沿 ${fmtNum(hist.positionPct, 0)}%`);
            }
        }
        if (metrics && estimate && Number.isFinite(metrics.spot)) {
            if (metrics.spot > estimate.rangeUsd[1]) {
                score += 1;
                reasons.push("现价高于预估上沿");
            } else if (metrics.spot < estimate.rangeUsd[0]) {
                score -= 1;
                reasons.push("现价低于预估下沿");
            }
        }
        if (score >= 2) return { label: "偏贵", note: reasons.join("；") || "偏离上沿，宜控制节奏" };
        if (score <= -2) return { label: "偏便宜", note: reasons.join("；") || "偏离下沿，可观察加仓" };
        return { label: "中性", note: reasons.join("；") || "现价处于可观察区间内" };
    }

    function loadJson(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            if (!raw) return fallback;
            return JSON.parse(raw);
        } catch {
            return fallback;
        }
    }

    function saveJson(key, val) {
        try {
            localStorage.setItem(key, JSON.stringify(val));
        } catch {
            /* ignore */
        }
    }

    function showToast(message) {
        const host = document.getElementById("toast-host");
        if (!host) return;
        const el = document.createElement("div");
        el.className = "toast";
        el.textContent = message;
        host.appendChild(el);
        setTimeout(() => {
            el.remove();
        }, 5200);
    }

    function fmtNum(n, digits = 2) {
        if (n == null || Number.isNaN(n)) return "--";
        return Number(n).toLocaleString("zh-CN", {
            minimumFractionDigits: digits,
            maximumFractionDigits: digits,
        });
    }

    function fmtTime(ms) {
        if (!ms) return "--";
        const d = new Date(ms);
        return d.toLocaleString("zh-CN", { hour12: false });
    }

    function fmtPct(n, digits = 2) {
        if (n == null || Number.isNaN(n)) return "--";
        const value = Number(n);
        return `${value >= 0 ? "+" : ""}${fmtNum(value, digits)}%`;
    }

    function renderSparkline() {
        const wrap = document.getElementById("spark-wrap");
        if (!wrap) return;
        wrap.innerHTML = "";
        const pts = state.history.slice(-36);
        if (pts.length < 2) {
            wrap.setAttribute("aria-hidden", "true");
            return;
        }
        wrap.removeAttribute("aria-hidden");
        const prices = pts.map((p) => p.price);
        const lo = Math.min(...prices);
        const hi = Math.max(...prices);
        const span = Math.max(hi - lo, 0.01);
        pts.forEach((p) => {
            const h = 12 + ((p.price - lo) / span) * 88;
            const bar = document.createElement("div");
            bar.className = "spark-bar";
            bar.style.height = `${h}%`;
            wrap.appendChild(bar);
        });
    }

    function renderHistoryTable() {
        const panel = document.getElementById("history-table-panel");
        const metaEl = document.getElementById("history-table-meta");
        const body = document.getElementById("history-table-body");
        if (!panel || !metaEl || !body) return;

        const list = Array.isArray(state.dailyHistory) ? state.dailyHistory : [];
        if (!list.length) {
            metaEl.textContent = "暂无历史样本";
            body.innerHTML = '<tr><td colspan="4">暂无历史数据</td></tr>';
            return;
        }

        const fx = Number(document.getElementById("inp-fx")?.value) || 0;
        const startIndex = Math.max(0, list.length - 12);
        const recent = list.slice(startIndex);
        metaEl.textContent = `${state.dailyGranularity === "monthly" ? "月均样本" : "日线样本"} · 最近 ${recent.length} 条`;
        body.innerHTML = recent.slice().reverse().map((item, index) => {
            const usd = Number(item.close_usd_oz);
            const cny = fx > 0 && Number.isFinite(usd) ? (usd / OZ_GRAMS) * fx : null;
            const originalIndex = startIndex + (recent.length - 1 - index);
            const prev = originalIndex > 0 ? list[originalIndex - 1] : null;
            const prevUsd = Number(prev?.close_usd_oz);
            const pct = Number.isFinite(prevUsd) && prevUsd > 0 ? ((usd / prevUsd) - 1) * 100 : null;
            return `
                <tr>
                    <td>${item.date || "--"}</td>
                    <td>${fmtNum(usd, 2)}</td>
                    <td>${cny != null ? fmtNum(cny, 2) : "--"}</td>
                    <td>${fmtPct(pct, 2)}</td>
                </tr>
            `;
        }).join("");
    }

    function renderHistoryTab() {
        document.querySelectorAll("[data-history-tab]").forEach((button) => {
            const tab = button.getAttribute("data-history-tab");
            button.classList.toggle("active", tab === state.historyTab);
        });
        const mapping = {
            chart: "history-panel-chart",
            stats: "history-panel-stats",
            table: "history-panel-table",
        };
        Object.values(mapping).forEach((id) => {
            document.getElementById(id)?.classList.remove("active");
        });
        document.getElementById(mapping[state.historyTab] || mapping.chart)?.classList.add("active");
    }

    function renderOverview() {
        const inputs = getInputState();
        const metrics = getCurrentMetrics(inputs);
        const hist = getHistoryStats();
        const estimate = getEstimateStats(inputs);
        const signal = buildValuationSignal(inputs);
        const domesticPremiumPct = metrics && Number.isFinite(inputs.domesticQuote) && metrics.cnyPerG > 0
            ? ((inputs.domesticQuote / metrics.cnyPerG) - 1) * 100
            : NaN;
        const planHint = Number.isFinite(inputs.planAddTarget) || Number.isFinite(inputs.planReduceTarget)
            ? `${Number.isFinite(inputs.planAddTarget) ? `加 ${fmtNum(inputs.planAddTarget, 0)}` : "--"} / ${Number.isFinite(inputs.planReduceTarget) ? `减 ${fmtNum(inputs.planReduceTarget, 0)}` : "--"}`
            : "未设目标";

        const setText = (id, value) => {
            const el = document.getElementById(id);
            if (el) el.textContent = value;
        };

        setText("overview-market-main", metrics ? `${fmtNum(metrics.spot, 2)} USD/oz` : "--");
        setText("overview-market-sub", metrics ? `${fmtNum(metrics.cnyPerG, 2)} 元/克` : "--");
        setText("overview-market-tag", state.dailyDemo ? "演示" : "实盘源");
        setText("overview-market-note", Number.isFinite(inputs.fx) ? `汇率 ${fmtNum(inputs.fx, 4)}，${state.dailyDemo ? "当前为回退序列" : "报价已连接"}` : "请先输入汇率");

        setText("overview-holding-main", metrics && Number.isFinite(metrics.pnl) ? `${metrics.pnl >= 0 ? "+" : ""}${fmtNum(metrics.pnl, 2)} 元` : "--");
        setText("overview-holding-sub", metrics && Number.isFinite(metrics.marketVal) ? `市值 ${fmtNum(metrics.marketVal, 0)}` : "市值 --");
        setText("overview-holding-cost", metrics && Number.isFinite(metrics.costBasis) ? `成本 ${fmtNum(metrics.costBasis, 0)}` : "成本 --");
        setText("overview-holding-note", metrics && Number.isFinite(metrics.pnlPct) ? `当前收益率 ${fmtPct(metrics.pnlPct, 2)}` : "输入持仓克重与成本后显示");

        setText("overview-range-main", hist ? `${fmtNum(hist.positionPct, 0)}% 区间位` : "--");
        setText("overview-range-sub", hist ? `${fmtNum(hist.low, 0)} / ${fmtNum(hist.high, 0)}` : "--");
        setText("overview-est-sub", estimate && estimate.rangeCny.every((x) => Number.isFinite(x)) ? `${fmtNum(estimate.rangeCny[0], 0)}-${fmtNum(estimate.rangeCny[1], 0)}` : "--");
        setText("overview-range-note", hist ? `${hist.firstDate} -> ${hist.lastDate}` : "等待历史样本");

        setText("overview-signal-main", signal.label);
        setText("overview-signal-sub", Number.isFinite(domesticPremiumPct) ? `偏离 ${fmtPct(domesticPremiumPct, 2)}` : "偏离 --");
        setText("overview-signal-plan", planHint);
        setText("overview-signal-note", signal.note);

        setText("spot-quick-stance", signal.label);
        setText("spot-side-position", hist ? `${fmtNum(hist.positionPct, 0)}%` : "--");
        setText("spot-side-estimate", estimate && estimate.rangeCny.every((x) => Number.isFinite(x)) ? `${fmtNum(estimate.rangeCny[0], 0)}-${fmtNum(estimate.rangeCny[1], 0)}` : "--");
        setText("spot-side-premium", Number.isFinite(domesticPremiumPct) ? fmtPct(domesticPremiumPct, 2) : "--");
        setText("spot-side-pnl", metrics && Number.isFinite(metrics.pnl) ? `${metrics.pnl >= 0 ? "+" : ""}${fmtNum(metrics.pnl, 0)}` : "--");
        setText("spot-dashboard-note", signal.note || "等待行情和历史样本后，这里会汇总当前盘面位置与估值结论。");
    }

    function renderDomesticDeviation() {
        const out = document.getElementById("domestic-out");
        if (!out) return;
        const inputs = getInputState();
        const metrics = getCurrentMetrics(inputs);
        if (!metrics) {
            out.textContent = "等待现价与汇率后再判断国内报价偏离。";
            return;
        }
        if (!Number.isFinite(inputs.domesticQuote) || inputs.domesticQuote <= 0) {
            out.textContent = "输入国内参考报价后，这里会给出相对理论克价的升贴水。";
            return;
        }
        const diff = inputs.domesticQuote - metrics.cnyPerG;
        const diffPct = metrics.cnyPerG > 0 ? (diff / metrics.cnyPerG) * 100 : NaN;
        const side = diff > 0 ? "偏贵" : diff < 0 ? "偏便宜" : "接近公允";
        out.innerHTML = `
            国内参考报价：<span class="hl">${fmtNum(inputs.domesticQuote, 2)}</span> 元/克<br>
            理论公允克价：<span class="hl">${fmtNum(metrics.cnyPerG, 2)}</span> 元/克<br>
            当前偏离：<span class="hl ${diff > 0 ? "neg" : "pos"}">${diff >= 0 ? "+" : ""}${fmtNum(diff, 2)}</span> 元/克（${fmtPct(diffPct, 2)}）<br>
            结论：<span class="hl">${side}</span>；可结合历史区间和预估区间一起判断。
        `;
    }

    function renderTargetPlan() {
        const out = document.getElementById("target-plan-out");
        if (!out) return;
        const inputs = getInputState();
        const metrics = getCurrentMetrics(inputs);
        if (!metrics || !Number.isFinite(metrics.grams) || !Number.isFinite(metrics.costBasis)) {
            out.textContent = "输入持仓参数后，这里会计算目标价的加仓 / 减仓计划。";
            return;
        }
        const step = Number.isFinite(inputs.planStepGrams) && inputs.planStepGrams > 0 ? inputs.planStepGrams : 0;
        const parts = [];
        if (Number.isFinite(inputs.planAddTarget) && inputs.planAddTarget > 0) {
            const cashNeed = step * inputs.planAddTarget;
            const newTotalGrams = metrics.grams + step;
            const newCostBasis = metrics.costBasis + cashNeed;
            const newAvgCost = newTotalGrams > 0 ? newCostBasis / newTotalGrams : NaN;
            parts.push(`加仓观察位 <span class="hl">${fmtNum(inputs.planAddTarget, 2)}</span> 元/克；按 <span class="hl">${fmtNum(step, 2)}</span> 克执行需资金 <span class="hl">${fmtNum(cashNeed, 2)}</span> 元，新均价约 <span class="hl">${fmtNum(newAvgCost, 2)}</span> 元/克。`);
        }
        if (Number.isFinite(inputs.planReduceTarget) && inputs.planReduceTarget > 0) {
            const sellPnl = metrics.grams * inputs.planReduceTarget - metrics.costBasis;
            parts.push(`减仓观察位 <span class="hl">${fmtNum(inputs.planReduceTarget, 2)}</span> 元/克；若当前仓位在此附近止盈，累计盈亏约为 <span class="hl ${sellPnl >= 0 ? "pos" : "neg"}">${sellPnl >= 0 ? "+" : ""}${fmtNum(sellPnl, 2)}</span> 元。`);
        }
        if (!parts.length) {
            out.textContent = "设置加仓观察价或减仓观察价后，这里会给出目标价计划。";
            return;
        }
        const signal = buildValuationSignal(inputs);
        out.innerHTML = `${parts.join("<br>")}<br>当前判断：<span class="hl">${signal.label}</span>，${signal.note}`;
    }

    function renderScenario() {
        const out = document.getElementById("scenario-out");
        if (!out) return;
        const inputs = getInputState();
        const metrics = getCurrentMetrics(inputs);
        if (!metrics || !Number.isFinite(metrics.grams) || !Number.isFinite(metrics.costBasis)) {
            out.textContent = "输入当前持仓后，这里会推演目标金价和加仓计划。";
            return;
        }
        const scenarioGold = Number.isFinite(inputs.scenarioGold) && inputs.scenarioGold > 0 ? inputs.scenarioGold : metrics.spot;
        const scenarioFx = Number.isFinite(inputs.scenarioFx) && inputs.scenarioFx > 0 ? inputs.scenarioFx : inputs.fx;
        const scenarioCny = calcCnyPerGram(scenarioGold, scenarioFx);
        if (!Number.isFinite(scenarioCny)) {
            out.textContent = "请先输入有效汇率，再进行情景推演。";
            return;
        }
        const addGrams = Number.isFinite(inputs.scenarioAddGrams) && inputs.scenarioAddGrams > 0 ? inputs.scenarioAddGrams : 0;
        const addPrice = Number.isFinite(inputs.scenarioAddPrice) && inputs.scenarioAddPrice > 0 ? inputs.scenarioAddPrice : 0;
        const extraFee = Number.isFinite(inputs.scenarioFee) && inputs.scenarioFee > 0 ? inputs.scenarioFee : 0;
        const totalGrams = metrics.grams + addGrams;
        const newCostBasis = metrics.costBasis + addGrams * addPrice + extraFee;
        const newAvgCost = totalGrams > 0 ? newCostBasis / totalGrams : NaN;
        const scenarioMarketValue = totalGrams * scenarioCny;
        const scenarioPnl = scenarioMarketValue - newCostBasis;
        const deltaPnl = Number.isFinite(metrics.pnl) ? scenarioPnl - metrics.pnl : NaN;
        out.innerHTML = `
            目标情景克价：<span class="hl">${fmtNum(scenarioCny, 2)}</span> 元/克（${fmtNum(scenarioGold, 2)} USD/oz × ${fmtNum(scenarioFx, 4)}）<br>
            情景后总持仓：<span class="hl">${fmtNum(totalGrams, 2)}</span> 克；新均价约 <span class="hl">${fmtNum(newAvgCost, 2)}</span> 元/克<br>
            情景市值：<span class="hl">${fmtNum(scenarioMarketValue, 2)}</span> 元；情景盈亏：<span class="hl ${scenarioPnl >= 0 ? "pos" : "neg"}">${scenarioPnl >= 0 ? "+" : ""}${fmtNum(scenarioPnl, 2)}</span> 元<br>
            相比当前盈亏变化：<span class="hl ${deltaPnl >= 0 ? "pos" : "neg"}">${deltaPnl >= 0 ? "+" : ""}${fmtNum(deltaPnl, 2)}</span> 元
        `;
    }

    function recalc() {
        const inputs = getInputState();
        const out = document.getElementById("calc-out");
        if (!out) return;

        const metrics = getCurrentMetrics(inputs);
        if (!metrics) {
            out.textContent = "等待有效现货价后再计算。";
            renderDomesticDeviation();
            renderTargetPlan();
            renderScenario();
            renderOverview();
            return;
        }
        if (!Number.isFinite(metrics.grams) || !Number.isFinite(metrics.cost) || metrics.grams < 0 || metrics.cost < 0) {
            out.textContent = "请填写有效的汇率与克重。";
            renderDomesticDeviation();
            renderTargetPlan();
            renderScenario();
            renderOverview();
            return;
        }

        out.innerHTML = `
            理论现货：<span class="hl">${fmtNum(metrics.cnyPerG, 2)}</span> 元/克（${fmtNum(metrics.spot, 2)} USD/oz × ${fmtNum(inputs.fx, 4)} ÷ ${OZ_GRAMS.toFixed(4)} g/oz）<br>
            持仓市值（估算）：<span class="hl">${fmtNum(metrics.marketVal, 2)}</span> 元<br>
            成本合计：<span class="hl">${fmtNum(metrics.costBasis, 2)}</span> 元<br>
            浮动盈亏（估算）：<span class="hl ${metrics.pnl >= 0 ? "pos" : "neg"}">${metrics.pnl >= 0 ? "+" : ""}${fmtNum(metrics.pnl, 2)}</span> 元（${fmtPct(metrics.pnlPct, 2)}）
        `;
        renderDailyEstimate();
        renderDomesticDeviation();
        renderTargetPlan();
        renderScenario();
        renderOverview();
    }

    function renderDailyEstimate() {
        const out = document.getElementById("day-estimate-out");
        const sampleEl = document.getElementById("day-sample-size");
        const meanEl = document.getElementById("day-mean-ret");
        const volEl = document.getElementById("day-vol");
        const sourceEl = document.getElementById("day-source");
        const sampleLabelEl = document.getElementById("day-sample-label");
        const meanLabelEl = document.getElementById("day-mean-label");
        const volLabelEl = document.getElementById("day-vol-label");
        if (!out || !sampleEl || !meanEl || !volEl || !sourceEl) return;

        const sample = state.dailyHistory.length;
        sampleEl.textContent = String(sample || "--");
        sourceEl.textContent = state.dailySource || "--";
        if (sampleLabelEl) sampleLabelEl.textContent = state.dailyGranularity === "monthly" ? "样本月数" : "样本数量";
        if (meanLabelEl) meanLabelEl.textContent = state.dailyGranularity === "monthly" ? "近20期均收益" : "近20期均收益";
        if (volLabelEl) volLabelEl.textContent = state.dailyGranularity === "monthly" ? "近20期波动率" : "近20期波动率";

        const summary = state.dailySummary;
        const expectedValue = Number(summary?.next_day_expected ?? summary?.next_30m_expected);
        if (!summary || !Number.isFinite(expectedValue)) {
            meanEl.textContent = "--";
            volEl.textContent = "--";
            out.textContent = "暂无可用历史样本。";
            return;
        }
        const mean = Number(summary.mean_daily_return ?? summary.mean_30m_return ?? 0);
        const vol = Number(summary.volatility_daily ?? summary.volatility_30m ?? 0);
        meanEl.textContent = `${mean >= 0 ? "+" : ""}${fmtNum(mean * 100, 3)}%`;
        volEl.textContent = `${fmtNum(vol * 100, 3)}%`;

        const fx = Number(document.getElementById("inp-fx")?.value) || 0;
        const expected = expectedValue;
        const rangeRaw = summary.next_day_range_1sigma ?? summary.next_30m_range_1sigma;
        const rng = Array.isArray(rangeRaw)
            ? rangeRaw.map((x) => Number(x))
            : [expected, expected];
        const cnyExpected = fx > 0 ? (expected / OZ_GRAMS) * fx : null;
        const cnyLo = fx > 0 ? (rng[0] / OZ_GRAMS) * fx : null;
        const cnyHi = fx > 0 ? (rng[1] / OZ_GRAMS) * fx : null;
        const hist = state.dailyHistory;
        let spanNote = "样本不足";
        if (hist.length >= 2) {
            const first = Number(hist[0].close_usd_oz || 0);
            const last = Number(hist[hist.length - 1].close_usd_oz || 0);
            if (first > 0 && last > 0) {
                const pct = ((last / first) - 1) * 100;
                spanNote = `${hist[0].date} -> ${hist[hist.length - 1].date} 累计 ${pct >= 0 ? "+" : ""}${fmtNum(pct, 2)}%`;
            }
        }

        const stance = mean > 0.001 ? "偏多日" : mean < -0.001 ? "偏空日" : "震荡日";
        out.innerHTML = `
            预测中枢（下一交易日）：<span class="hl">${fmtNum(expected, 2)}</span> USD/oz<br>
            1σ 区间（下一交易日）：<span class="hl">${fmtNum(rng[0], 2)} - ${fmtNum(rng[1], 2)}</span> USD/oz<br>
            折算区间：<span class="hl">${cnyLo != null ? fmtNum(cnyLo, 2) : "--"} - ${cnyHi != null ? fmtNum(cnyHi, 2) : "--"}</span> 元/克（按当前汇率）<br>
            区间信号：<span class="hl">${stance}</span>（均收益 ${mean >= 0 ? "+" : ""}${fmtNum(mean * 100, 3)}%，波动 ${fmtNum(vol * 100, 3)}%）<br>
            历史区间：<span class="hl">${spanNote}</span>
            ${state.dailyDemo ? "<br>注：当前为演示回退历史序列，请勿用于实盘决策。" : ""}
        `;
        if (cnyExpected && Number.isFinite(cnyExpected)) {
            const spotCny = document.getElementById("spot-cny-g");
            if (spotCny && (spotCny.textContent || "").trim() === "--") {
                spotCny.textContent = fmtNum(cnyExpected, 2);
            }
        }
        renderHistoryStats();
        renderOverview();
    }

    function renderHistoryStats() {
        const stats = getHistoryStats();
        const setText = (id, value) => {
            const el = document.getElementById(id);
            if (el) el.textContent = value;
        };
        if (!stats) {
            setText("hist-stat-lowhigh", "--");
            setText("hist-stat-position", "--");
            setText("hist-stat-amplitude", "--");
            setText("hist-stat-span", "--");
            return;
        }
        setText("hist-stat-lowhigh", `${fmtNum(stats.low, 2)} / ${fmtNum(stats.high, 2)} USD`);
        setText("hist-stat-position", `${fmtNum(stats.positionPct, 0)}% 区间位`);
        setText("hist-stat-amplitude", fmtPct(stats.amplitudePct, 2));
        setText("hist-stat-span", fmtPct(stats.spanPct, 2));
    }

    function loadAlertsToForm() {
        const a = loadJson(LS_ALERTS, {});
        const hi = document.getElementById("inp-alert-high");
        const lo = document.getElementById("inp-alert-low");
        if (hi && a.high != null) hi.value = a.high;
        if (lo && a.low != null) lo.value = a.low;
    }

    function saveAlertsFromForm() {
        const hi = document.getElementById("inp-alert-high");
        const lo = document.getElementById("inp-alert-low");
        const highV = (hi?.value || "").trim();
        const lowV = (lo?.value || "").trim();
        const high = highV === "" ? null : Number(highV);
        const low = lowV === "" ? null : Number(lowV);
        saveJson(LS_ALERTS, { high, low });
        state.lastCross = {};
        saveJson(LS_LAST, state.lastCross);
        showToast("已保存本机提醒条件");
    }

    function maybeNotify(title, body) {
        if (typeof Notification === "undefined") return;
        if (Notification.permission === "granted") {
            try {
                new Notification(title, { body, silent: false });
            } catch {
                /* ignore */
            }
        }
        showToast(`${title}：${body}`);
    }

    function checkAlerts(price, prev) {
        if (price == null || !Number.isFinite(price)) return;
        const a = loadJson(LS_ALERTS, {});
        const hi = a.high;
        const lo = a.low;

        if (Number.isFinite(hi)) {
            const key = `hi:${hi}`;
            if (price >= hi && prev != null && prev < hi && state.lastCross[key] !== "fired") {
                maybeNotify("黄金提醒", `现货已上破 ${hi} USD/oz（当前 ${price.toFixed(2)}）`);
                state.lastCross[key] = "fired";
            }
            if (price < hi - 0.25) delete state.lastCross[key];
        }
        if (Number.isFinite(lo)) {
            const key = `lo:${lo}`;
            if (price <= lo && prev != null && prev > lo && state.lastCross[key] !== "fired") {
                maybeNotify("黄金提醒", `现货已下破 ${lo} USD/oz（当前 ${price.toFixed(2)}）`);
                state.lastCross[key] = "fired";
            }
            if (price > lo + 0.25) delete state.lastCross[key];
        }
        saveJson(LS_LAST, state.lastCross);
    }

    async function fetchQuote() {
        const ep = document.getElementById("spot-api-endpoint");
        if (ep) ep.textContent = quoteUrl;

        let data = null;
        try {
            const res = await fetch(quoteUrl, { signal: AbortSignal.timeout(12000) });
            const json = await res.json();
            if (json && json.success && json.data) data = json.data;
        } catch (e) {
            const st = document.getElementById("spot-status");
            if (st) {
                st.textContent = `请求失败（${e?.message || "网络错误"}）。请确认后端已启动且 Nginx 已反代 /api/v1。`;
            }
            return;
        }

        if (!data) {
            const st = document.getElementById("spot-status");
            if (st) st.textContent = "接口返回异常。";
            return;
        }

        const price = Number(data.price_usd_oz);
        const chp = Number(data.change_percent);
        const demo = Boolean(data.demo);
        const err = Boolean(data.upstream_error);

        const prev = state.lastPrice;
        state.lastPrice = price;
        state.history.push({ price, t: data.as_of_ms || Date.now() });
        state.history = state.history.slice(-120);

        const priceEl = document.getElementById("spot-price");
        const chEl = document.getElementById("spot-change");
        const timeEl = document.getElementById("spot-time");
        const badge = document.getElementById("spot-source-badge");
        const cnyG = document.getElementById("spot-cny-g");
        const pollEl = document.getElementById("spot-poll");
        const status = document.getElementById("spot-status");

        priceEl.textContent = fmtNum(price, 2);
        priceEl.classList.remove("up", "down");
        if (Number.isFinite(chp)) {
            if (chp > 0) priceEl.classList.add("up");
            if (chp < 0) priceEl.classList.add("down");
        }

        const sign = chp > 0 ? "+" : "";
        chEl.textContent = Number.isFinite(chp) ? `${sign}${fmtNum(chp, 3)}%（24h 估算涨跌）` : "--";
        timeEl.textContent = `报价时间 ${fmtTime(data.as_of_ms)}`;

        badge.textContent = demo ? "演示数据" : "行情源";
        badge.className = "badge " + (demo ? "demo" : "live");

        const fx = Number(document.getElementById("inp-fx")?.value) || 0;
        if (fx > 0 && Number.isFinite(price)) {
            const cpg = (price / OZ_GRAMS) * fx;
            cnyG.textContent = fmtNum(cpg, 2);
        } else {
            cnyG.textContent = "--";
        }

        pollEl.textContent = new Date().toLocaleTimeString("zh-CN", { hour12: false });
        status.textContent = demo
            ? `当前为服务端演示序列（${err ? "上游曾失败，已回退" : "未配置 GOLDAPI_IO_TOKEN"}）。`
            : "实时行情已连接。";

        renderSparkline();
        recalc();
        checkAlerts(price, prev);
    }

    async function fetchDailyHistory() {
        const historyUrl = `${apiBase}/market/gold/history?days=${state.historyDays}`;
        const ep = document.getElementById("day-api-endpoint");
        if (ep) ep.textContent = historyUrl;
        const status = document.getElementById("day-status");
        try {
            const res = await fetch(historyUrl, { signal: AbortSignal.timeout(12000) });
            const json = await res.json();
            const data = json?.data;
            if (!json?.success || !data) {
                throw new Error("响应结构异常");
            }
            state.dailyHistory = Array.isArray(data.items) ? data.items : [];
            state.dailySummary = data.summary || null;
            state.dailyGranularity = data.granularity === "monthly" ? "monthly" : "daily";
            state.dailySource = state.dailyGranularity === "monthly" ? "月均样本" : "日线样本";
            state.dailyDemo = Boolean(data.demo);
            if (status) {
                status.textContent = data.demo
                    ? "历史数据为演示回退序列（免费源不可用或网络失败）。"
                    : (state.dailyGranularity === "monthly" ? "历史月均样本已加载。" : "历史日线样本已加载。");
            }
            state.lineHoverIndex = null;
            renderDailyEstimate();
            renderHistoryLineChart();
            renderHistoryTable();
            renderHistoryStats();
        } catch (e) {
            state.dailyHistory = [];
            state.dailySummary = null;
            state.dailySource = "--";
            state.dailyGranularity = "daily";
            state.dailyDemo = true;
            if (status) {
                status.textContent = `历史接口请求失败（${e?.message || "网络错误"}）`;
            }
            state.lineHoverIndex = null;
            renderDailyEstimate();
            renderHistoryLineChart();
            renderHistoryTable();
            renderHistoryStats();
        }
    }

    function chooseTimeUnitByRange(days) {
        if (days <= 45) return "日";
        if (days <= 400) return "月";
        return "年";
    }

    function formatDateByUnit(dateStr, unit) {
        const d = new Date(`${dateStr}T00:00:00`);
        if (Number.isNaN(d.getTime())) return dateStr;
        if (unit === "日") return `${d.getMonth() + 1}/${d.getDate()}`;
        if (unit === "月") return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
        return String(d.getFullYear());
    }

    function renderHistoryLineChart() {
        const canvas = document.getElementById("history-line-canvas");
        const unitEl = document.getElementById("line-time-unit");
        const seriesEl = document.getElementById("line-series-name");
        const tipEl = document.getElementById("line-hover-tip");
        const floatTipEl = document.getElementById("line-float-tip");
        if (!canvas || !unitEl) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        const list = Array.isArray(state.dailyHistory) ? state.dailyHistory : [];
        const days = state.historyDays || 3650;
        const timeUnit = chooseTimeUnitByRange(days);
        unitEl.textContent = timeUnit;

        const w = canvas.width;
        const h = canvas.height;
        ctx.clearRect(0, 0, w, h);

        if (list.length < 2) {
            if (floatTipEl) floatTipEl.style.display = "none";
            ctx.fillStyle = "#8b93a7";
            ctx.font = "14px sans-serif";
            ctx.fillText("暂无足够历史数据", 20, 32);
            return;
        }

        const fx = Number(document.getElementById("inp-fx")?.value) || 0;
        const prices = list
            .map((x) => {
                const usd = Number(x.close_usd_oz);
                if (!Number.isFinite(usd)) return NaN;
                if (state.lineUnit === "cny") {
                    if (!(fx > 0)) return NaN;
                    return (usd / OZ_GRAMS) * fx;
                }
                return usd;
            })
            .filter((x) => Number.isFinite(x));
        if (prices.length < 2) return;
        if (seriesEl) seriesEl.textContent = state.lineUnit === "cny" ? "RMB/g" : "USD/oz";
        const min = Math.min(...prices);
        const max = Math.max(...prices);
        const span = Math.max(max - min, 0.01);

        const padL = 56;
        const padR = 16;
        const padT = 14;
        const padB = 30;
        const iw = w - padL - padR;
        const ih = h - padT - padB;

        ctx.strokeStyle = "rgba(255,255,255,0.12)";
        ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i += 1) {
            const y = padT + (ih * i) / 4;
            ctx.beginPath();
            ctx.moveTo(padL, y);
            ctx.lineTo(w - padR, y);
            ctx.stroke();
        }

        ctx.strokeStyle = "#e6c35c";
        ctx.lineWidth = 2;
        ctx.beginPath();
        prices.forEach((p, i) => {
            const x = padL + (iw * i) / (prices.length - 1);
            const y = padT + ih - ((p - min) / span) * ih;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();

        const grad = ctx.createLinearGradient(0, padT, 0, padT + ih);
        grad.addColorStop(0, "rgba(230,195,92,0.30)");
        grad.addColorStop(1, "rgba(230,195,92,0.02)");
        ctx.fillStyle = grad;
        ctx.beginPath();
        prices.forEach((p, i) => {
            const x = padL + (iw * i) / (prices.length - 1);
            const y = padT + ih - ((p - min) / span) * ih;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.lineTo(padL + iw, padT + ih);
        ctx.lineTo(padL, padT + ih);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = "#8b93a7";
        ctx.font = "12px sans-serif";
        ctx.textAlign = "right";
        ctx.fillText(fmtNum(max, 2), padL - 8, padT + 10);
        ctx.fillText(fmtNum(min, 2), padL - 8, padT + ih);

        ctx.textAlign = "center";
        const ticks = 4;
        for (let i = 0; i <= ticks; i += 1) {
            const idx = Math.min(list.length - 1, Math.floor((i / ticks) * (list.length - 1)));
            const x = padL + (iw * idx) / (list.length - 1);
            const label = formatDateByUnit(list[idx].date, timeUnit);
            ctx.fillText(label, x, h - 8);
        }

        const hi = state.lineHoverIndex;
        if (Number.isInteger(hi) && hi >= 0 && hi < prices.length) {
            const px = prices[hi];
            const x = padL + (iw * hi) / (prices.length - 1);
            const y = padT + ih - ((px - min) / span) * ih;
            ctx.save();
            ctx.strokeStyle = "rgba(255,255,255,0.35)";
            ctx.setLineDash([4, 4]);
            ctx.beginPath();
            ctx.moveTo(x, padT);
            ctx.lineTo(x, padT + ih);
            ctx.moveTo(padL, y);
            ctx.lineTo(padL + iw, y);
            ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = "#fcd34d";
            ctx.beginPath();
            ctx.arc(x, y, 3.2, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
            if (tipEl) {
                const label = state.lineUnit === "cny" ? "RMB/g" : "USD/oz";
                tipEl.textContent = `${list[hi].date} · ${fmtNum(px, 2)} ${label}`;
            }
            if (floatTipEl) {
                const label = state.lineUnit === "cny" ? "RMB/g" : "USD/oz";
                floatTipEl.textContent = `${list[hi].date} | ${fmtNum(px, 2)} ${label}`;
                floatTipEl.style.display = "block";
                const cw = canvas.width;
                const preferRight = x < cw * 0.62;
                const left = preferRight ? Math.min(x + 16, cw - 210) : Math.max(8, x - 196);
                const top = Math.max(36, Math.min(y - 24, canvas.height - 54));
                floatTipEl.style.left = `${left}px`;
                floatTipEl.style.top = `${top}px`;
            }
        } else if (tipEl) {
            tipEl.textContent = "移动鼠标查看该点时间与价格（十字线）";
            if (floatTipEl) floatTipEl.style.display = "none";
        }
    }

    function startPoll() {
        fetchQuote();
        fetchDailyHistory();
        if (state.pollTimer) clearInterval(state.pollTimer);
        state.pollTimer = setInterval(fetchQuote, POLL_MS);
    }

    function bind() {
        [
            "inp-fx",
            "inp-domestic-quote",
            "inp-grams",
            "inp-cost",
            "inp-fee",
            "inp-plan-add-target",
            "inp-plan-reduce-target",
            "inp-plan-step-grams",
            "inp-scenario-gold",
            "inp-scenario-fx",
            "inp-scenario-add-grams",
            "inp-scenario-add-price",
            "inp-scenario-fee",
        ].forEach((id) => {
            document.getElementById(id)?.addEventListener("input", () => {
                recalc();
                renderHistoryLineChart();
                renderHistoryTable();
            });
        });
        document.getElementById("day-range")?.addEventListener("change", (e) => {
            const v = Number(e?.target?.value);
            if (Number.isFinite(v) && v >= 365 && v <= 3650) {
                state.historyDays = v;
                fetchDailyHistory();
            }
        });
        document.getElementById("btn-reload-history")?.addEventListener("click", () => {
            fetchDailyHistory();
        });
        document.getElementById("btn-save-alerts")?.addEventListener("click", saveAlertsFromForm);
        document.getElementById("btn-notify")?.addEventListener("click", async () => {
            if (typeof Notification === "undefined") {
                showToast("当前环境不支持浏览器通知");
                return;
            }
            const p = await Notification.requestPermission();
            showToast(p === "granted" ? "已授予通知权限" : "未授予通知权限");
        });
        document.getElementById("line-unit-usd")?.addEventListener("click", () => {
            state.lineUnit = "usd";
            document.getElementById("line-unit-usd")?.classList.add("active");
            document.getElementById("line-unit-cny")?.classList.remove("active");
            renderHistoryLineChart();
        });
        document.getElementById("line-unit-cny")?.addEventListener("click", () => {
            state.lineUnit = "cny";
            document.getElementById("line-unit-cny")?.classList.add("active");
            document.getElementById("line-unit-usd")?.classList.remove("active");
            renderHistoryLineChart();
        });
        document.querySelectorAll("[data-history-tab]").forEach((button) => {
            button.addEventListener("click", () => {
                const tab = button.getAttribute("data-history-tab") || "chart";
                state.historyTab = tab;
                renderHistoryTab();
            });
        });
        document.querySelectorAll("[data-collapse-toggle]").forEach((button) => {
            button.addEventListener("click", () => {
                const block = button.closest(".tool-block");
                if (!block) return;
                block.classList.toggle("collapsed");
            });
        });
        const canvas = document.getElementById("history-line-canvas");
        canvas?.addEventListener("mousemove", (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const list = state.dailyHistory || [];
            if (list.length < 2) return;
            const w = canvas.width;
            const padL = 56;
            const padR = 16;
            const iw = w - padL - padR;
            const ratio = Math.min(1, Math.max(0, (x - padL) / Math.max(iw, 1)));
            state.lineHoverIndex = Math.round(ratio * (list.length - 1));
            renderHistoryLineChart();
        });
        canvas?.addEventListener("mouseleave", () => {
            state.lineHoverIndex = null;
            const floatTipEl = document.getElementById("line-float-tip");
            if (floatTipEl) floatTipEl.style.display = "none";
            renderHistoryLineChart();
        });
        window.addEventListener("resize", () => {
            renderHistoryLineChart();
        });
        renderHistoryTable();
        renderHistoryStats();
        renderHistoryTab();
        renderOverview();
        renderDomesticDeviation();
        renderTargetPlan();
        renderScenario();
    }

    document.addEventListener("DOMContentLoaded", () => {
        bind();
        loadAlertsToForm();
        startPoll();
    });
})();
