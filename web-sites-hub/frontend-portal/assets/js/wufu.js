document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const textInput = document.getElementById('text-input');
    const fuDisplay = document.getElementById('fu-display');
    const previewArea = document.getElementById('preview-area');
    const doufang = document.querySelector('.doufang');
    const fontBtns = document.querySelectorAll('.font-btn');
    const textColorPicker = document.getElementById('text-color');
    const bgColorPicker = document.getElementById('bg-color');
    const borderColorPicker = document.getElementById('border-color');
    const sizeSlider = document.getElementById('size-slider');
    const randomBtn = document.getElementById('random-btn');
    const fuGrid = document.getElementById('fu-grid');

    // State
    const state = {
        text: '福',
        font: "'Ma Shan Zheng', cursive",
        textColor: '#1a0505',
        bgColor: '#d90429', // Default red paper
        borderColor: '#ffb703', // Gold border
        size: 120
    };

    // Font Definitions (Base Families)
    // Combining Google Fonts + System Fonts (Windows/Mac) to approximate variety
    const baseFonts = [
        // 10 Selected Fonts (Matching UI Buttons)
        { family: "'Ma Shan Zheng', cursive", name: "马善政毛笔", desc: "雄健书法" },
        { family: "'Zhi Mang Xing', cursive", name: "志莽行书", desc: "灵动行书" },
        { family: "'Long Cang', cursive", name: "龙苍草书", desc: "狂放草书" },
        { family: "'ZCOOL XiaoWei', serif", name: "站酷小薇", desc: "清秀隶书" },
        { family: "'ZCOOL KuaiLe', cursive", name: "站酷快乐", desc: "俏皮可爱" },
        { family: "'ZCOOL QingKe HuangYou', cursive", name: "站酷黄油", desc: "圆润规整" },
        { family: "KaiTi, STKaiti, '楷体', serif", name: "楷体", desc: "端庄典雅" },
        { family: "'Liu Jian Mao Cao', cursive", name: "流光毛草", desc: "狂草墨迹" },
        { family: "'Noto Serif SC', serif", name: "思源宋体", desc: "现代宋体" },
        { family: "STXingkai, 'Xingkai SC', '行楷', cursive", name: "华文行楷", desc: "流畅行楷" }
    ];

    // 10 Style Variations (10 Fonts x 10 Styles = 100 Items)
    const variations = [
        { suffix: "", style: {}, nameSuffix: "" }, // 1. Original
        { suffix: " (金)", style: { color: '#ffb703', textShadow: '1px 1px 0px #370617' }, nameSuffix: "·金" }, // 2. Gold
        { suffix: " (粗)", style: { fontWeight: 'bold' }, nameSuffix: "·粗" }, // 3. Bold
        { suffix: " (斜)", style: { fontStyle: 'italic' }, nameSuffix: "·斜" }, // 4. Italic
        { suffix: " (长)", style: { transform: 'scaleY(1.2)' }, nameSuffix: "·长" }, // 5. Tall
        { suffix: " (扁)", style: { transform: 'scaleX(1.3)' }, nameSuffix: "·扁" }, // 6. Wide
        { suffix: " (大)", style: { transform: 'scale(1.15)' }, nameSuffix: "·大" }, // 7. Large
        { suffix: " (空)", style: { WebkitTextStroke: '1px #1a0505', color: 'transparent' }, nameSuffix: "·空" }, // 8. Hollow
        { suffix: " (金空)", style: { WebkitTextStroke: '1px #ffb703', color: 'transparent' }, nameSuffix: "·金空" }, // 9. Gold Hollow
        { suffix: " (影)", style: { textShadow: '4px 4px 0px rgba(0,0,0,0.2)' }, nameSuffix: "·影" } // 10. Shadow
    ];

    // Generate accurate 100 fonts
    function generate100FontsMeta() {
        let list = [];
        let count = 0;
        
        // 10 Bases * 10 Variations = 100 Total
        // We want a nice mix. We can iterate variations then bases to scatter them,
        // or just generate all combinations and then the grid generator shuffles them (which it does).
        
        baseFonts.forEach(base => {
            variations.forEach(vari => {
                list.push({
                    family: base.family,
                    name: base.name + vari.nameSuffix,
                    desc: base.desc,
                    style: vari.style, 
                    baseMeta: base
                });
                count++;
            });
        });
        
        return list;
    }

    const fontsMeta = generate100FontsMeta();

    // Helper to get random font from meta (for random button)
    const getRandomFontMeta = () => fontsMeta[Math.floor(Math.random() * fontsMeta.length)];

    const colors = [
        { name: 'Classic Red', bg: '#d90429', text: '#1a0505', border: '#ffb703' },
        { name: 'Gold', bg: '#ffb703', text: '#d90429', border: '#d90429' },
        { name: 'Royal Purple', bg: '#7209b7', text: '#ffd166', border: '#ffd166' },
        { name: 'Midnight', bg: '#03071e', text: '#d90429', border: '#ffba08' }
    ];

    // Initialization
    function init() {
        updateDisplay();
        generateGrid();
        setupEventListeners();
    }

    // Update the main preview
    function updateDisplay() {
        fuDisplay.textContent = state.text;
        fuDisplay.style.fontFamily = state.font;
        fuDisplay.style.color = state.textColor;
        
        // 根据文字长度自动调整字体大小
        const textLength = state.text.length;
        let fontSize;
        if (textLength === 1) {
            fontSize = state.size / 10; // 单个字使用原始大小
        } else if (textLength === 2) {
            fontSize = (state.size * 0.7) / 10; // 两个字缩小到70%
        } else if (textLength === 3) {
            fontSize = (state.size * 0.55) / 10; // 三个字缩小到55%
        } else {
            fontSize = (state.size * 0.45) / 10; // 四个字缩小到45%
        }
        fuDisplay.style.fontSize = `${fontSize}rem`;
        
        previewArea.style.backgroundColor = state.bgColor;
        
        // Update doufang border
        doufang.style.borderColor = state.borderColor;
        previewArea.style.setProperty('--border-color', state.borderColor);
    }

    // Setup Listeners
    function setupEventListeners() {
        textInput.addEventListener('input', (e) => {
            state.text = e.target.value || '福';
            updateDisplay();
        });

        fontBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update UI
                fontBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Update State
                state.font = btn.getAttribute('data-font');
                updateDisplay();
            });
        });

        textColorPicker.addEventListener('input', (e) => {
            state.textColor = e.target.value;
            updateDisplay();
        });

        bgColorPicker.addEventListener('input', (e) => {
            state.bgColor = e.target.value;
            updateDisplay();
        });
        
        borderColorPicker.addEventListener('input', (e) => {
            state.borderColor = e.target.value;
            updateDisplay();
        });

        sizeSlider.addEventListener('input', (e) => {
            state.size = e.target.value;
            updateDisplay();
        });

        randomBtn.addEventListener('click', randomize);
    }

    function randomize() {
        // Random Font
        const randomMeta = getRandomFontMeta();
        state.font = randomMeta.family;
        
        // Random Color Scheme
        const randomScheme = colors[Math.floor(Math.random() * colors.length)];
        state.bgColor = randomScheme.bg;
        state.textColor = randomScheme.text;
        state.borderColor = randomScheme.border;

        // Update Inputs
        textColorPicker.value = state.textColor;
        bgColorPicker.value = state.bgColor;
        borderColorPicker.value = state.borderColor;
        
        // Update UI classes
        fontBtns.forEach(btn => {
            if(btn.getAttribute('data-font') === state.font) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        updateDisplay();
    }

    // Generate the Showcase Grid
    function generateGrid() {
        const gridCount = 100; 
        const fragment = document.createDocumentFragment();

        // Use the pre-generated 100 unique styles
        // Shuffle them for display variety, but ensure all 100 are used once.
        let deck = [...fontsMeta]; 
        
        // Shuffle the deck (Fisher-Yates)
        for (let i = deck.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [deck[i], deck[j]] = [deck[j], deck[i]];
        }

        // 3. Render
        deck.forEach((fontMeta, index) => {
            const card = document.createElement('div');
            card.className = 'fu-card';
            
            const font = fontMeta.family;
            
            const content = document.createElement('span');
            content.className = 'char';
            content.textContent = '福';
            content.style.fontFamily = font;
            
            // Apply special variations (Bold, Italic, Scale, etc.)
            if (fontMeta.style) {
                 Object.assign(content.style, fontMeta.style);
            }
            
            // 保持正方向，不添加随机旋转
            // 如果 style 中已有 transform，保留它

            // Tooltip
            const tooltip = document.createElement('div');
            tooltip.className = 'fu-tooltip';
            tooltip.innerHTML = `
                <span class="font-name">${fontMeta.name}</span>
                <span class="font-desc">${fontMeta.desc}</span>
            `;

            card.appendChild(content);
            card.appendChild(tooltip);
            
            // 创建保存按钮
            const saveBtn = document.createElement('button');
            saveBtn.type = 'button';
            saveBtn.className = 'fu-card-save-btn';
            saveBtn.textContent = '💾 Save';
            saveBtn.onclick = (e) => {
                e.stopPropagation();
                saveFuAsImage(card, getSaveFilename());
                saveBtn.classList.remove('show');
            };
            card.appendChild(saveBtn);
            
            // 阻止左键 mousedown 默认行为，防止点击时页面滚动
            card.addEventListener('mousedown', (e) => {
                if (e.button !== 0 || e.target === saveBtn || saveBtn.contains(e.target)) return;
                e.preventDefault();
            });
            
            // 点击卡片：显示保存按钮
            card.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                // 如果点击的是保存按钮，不处理（由 saveBtn.onclick 处理）
                if (e.target === saveBtn || saveBtn.contains(e.target)) {
                    return;
                }
                
                // 如果刚触发了长按，不执行点击
                if (card._longPressed && card._longPressed()) {
                    return;
                }
                
                // 关闭其他卡片的保存按钮
                document.querySelectorAll('.fu-card-save-btn.show').forEach(btn => {
                    if (btn !== saveBtn) {
                        btn.classList.remove('show');
                    }
                });
                
                // 切换当前卡片的保存按钮
                const isShowing = saveBtn.classList.contains('show');
                if (isShowing) {
                    // 如果已显示，隐藏并应用样式到预览区
                    saveBtn.classList.remove('show');
                    state.font = font;
                    
                    // Find matching button if exists
                    fontBtns.forEach(btn => {
                        const btnFont = btn.getAttribute('data-font');
                        if (btnFont && (font.includes(btnFont.split(',')[0]) || btnFont === font)) {
                            btn.classList.add('active');
                        } else {
                            btn.classList.remove('active');
                        }
                    });

                    updateDisplay();
                } else {
                    // 如果未显示，显示保存按钮
                    saveBtn.classList.add('show');
                }
            });
            
            // 为卡片添加长按/右键保存功能
            setupLongPressSave(card, () => getSaveFilename());

            fragment.appendChild(card);
        });

        fuGrid.innerHTML = ''; // Clear existing
        fuGrid.appendChild(fragment);
    }

    // 生成文件名时间戳：YYYYMMDDHHmmss（如 20260206210003）
    function getSaveTimestamp() {
        const n = new Date();
        const pad = (x) => String(x).padStart(2, '0');
        return `${n.getFullYear()}${pad(n.getMonth() + 1)}${pad(n.getDate())}${pad(n.getHours())}${pad(n.getMinutes())}${pad(n.getSeconds())}`;
    }
    function getSaveFilename() {
        return `wufu_${getSaveTimestamp()}.png`;
    }

    // 保存福字为图片（使用 html2canvas 或 fallback 到 canvas）
    const FU_CARD_OUTPUT_SIZE = 512; // 百福图卡片导出固定尺寸，福字适配填满
    const CHAR_FILL_RATIO = 0.78;    // 福字占画布比例
    
    async function saveFuAsImage(element, filename = null) {
        if (!filename) filename = getSaveFilename();
        const isFuCard = element.classList && element.classList.contains('fu-card');
        
        // 百福图卡片：使用 canvas 固定尺寸导出，福字适配填满
        if (isFuCard) {
            const charEl = element.querySelector('.char');
            if (charEl) {
                const canvas = document.createElement('canvas');
                canvas.width = FU_CARD_OUTPUT_SIZE;
                canvas.height = FU_CARD_OUTPUT_SIZE;
                const ctx = canvas.getContext('2d');
                const cStyle = window.getComputedStyle(element);
                const bgColor = cStyle.backgroundColor || '#d90429';
                ctx.fillStyle = bgColor;
                ctx.fillRect(0, 0, FU_CARD_OUTPUT_SIZE, FU_CARD_OUTPUT_SIZE);
                
                const charStyle = window.getComputedStyle(charEl);
                const fontSize = Math.round(FU_CARD_OUTPUT_SIZE * CHAR_FILL_RATIO);
                ctx.save();
                ctx.translate(FU_CARD_OUTPUT_SIZE / 2, FU_CARD_OUTPUT_SIZE / 2);
                ctx.font = `${charStyle.fontStyle} ${charStyle.fontWeight} ${fontSize}px ${charStyle.fontFamily}`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                const textShadow = charStyle.textShadow;
                if (textShadow && textShadow !== 'none') {
                    const parts = textShadow.split(' ');
                    if (parts.length >= 3) {
                        ctx.shadowOffsetX = parseFloat(parts[0]) * (fontSize / 48);
                        ctx.shadowOffsetY = parseFloat(parts[1]) * (fontSize / 48);
                        ctx.shadowBlur = parseFloat(parts[2]) * (fontSize / 48);
                        ctx.shadowColor = parts[3] || 'rgba(0,0,0,0.2)';
                    }
                }
                
                const stroke = charStyle.webkitTextStroke;
                if (stroke && stroke !== '0px none') {
                    const parts = stroke.split(' ');
                    ctx.strokeStyle = parts[1] || '#1a0505';
                    ctx.lineWidth = (parseFloat(parts[0]) || 1) * (fontSize / 48);
                    ctx.strokeText(charEl.textContent, 0, 0);
                }
                ctx.fillStyle = charStyle.color;
                ctx.fillText(charEl.textContent, 0, 0);
                ctx.restore();
                
                canvas.toBlob((blob) => {
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                }, 'image/png');
                return;
            }
        }
        
        // 预览区域：统一使用 canvas 绘制，确保斗方菱形不超出边界（html2canvas 易出现溢出）
        // 跳过 html2canvas，直接走下方 canvas fallback
        
        // Fallback: 使用纯 canvas 方法（预览区域）
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        const rect = element.getBoundingClientRect();
        const scale = 2;
        canvas.width = rect.width * scale;
        canvas.height = rect.height * scale;
        ctx.scale(scale, scale);
        
        const computedStyle = window.getComputedStyle(element);
        const bgColor = computedStyle.backgroundColor || '#ffffff';
        ctx.fillStyle = bgColor;
        ctx.fillRect(0, 0, rect.width, rect.height);
        
        // 处理预览区域
        if (element.id === 'preview-area') {
            const fuDisplay = element.querySelector('#fu-display');
            const doufang = element.querySelector('.doufang');
            
            if (fuDisplay) {
                // 绘制斗方（菱形）：边长 = 预览区/√2，旋转45度后顶点触及四边中点
                if (doufang) {
                    const size = Math.min(rect.width, rect.height);
                    const diamondSide = size / Math.sqrt(2);
                    const cx = rect.width / 2;
                    const cy = rect.height / 2;
                    ctx.save();
                    ctx.translate(cx, cy);
                    ctx.rotate(45 * Math.PI / 180);
                    ctx.strokeStyle = state.borderColor;
                    ctx.lineWidth = 2;
                    ctx.strokeRect(-diamondSide / 2, -diamondSide / 2, diamondSide, diamondSide);
                    const innerOffset = diamondSide * 0.08;
                    ctx.setLineDash([5, 5]);
                    ctx.lineWidth = 1;
                    ctx.strokeRect(-diamondSide / 2 + innerOffset, -diamondSide / 2 + innerOffset,
                                   diamondSide - innerOffset * 2, diamondSide - innerOffset * 2);
                    ctx.restore();
                }
                
                // 绘制福字
                const fRect = fuDisplay.getBoundingClientRect();
                const fx = fRect.left - rect.left;
                const fy = fRect.top - rect.top;
                const fStyle = window.getComputedStyle(fuDisplay);
                
                ctx.save();
                ctx.translate(fx + fRect.width / 2, fy + fRect.height / 2);
                ctx.font = `${fStyle.fontStyle} ${fStyle.fontWeight} ${fStyle.fontSize} ${fStyle.fontFamily}`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = fStyle.color;
                
                const textShadow = fStyle.textShadow;
                if (textShadow && textShadow !== 'none') {
                    const parts = textShadow.split(' ');
                    if (parts.length >= 3) {
                        ctx.shadowOffsetX = parseFloat(parts[0]);
                        ctx.shadowOffsetY = parseFloat(parts[1]);
                        ctx.shadowBlur = parseFloat(parts[2]);
                        ctx.shadowColor = parts[3] || 'rgba(0,0,0,0.2)';
                    }
                }
                
                ctx.fillText(fuDisplay.textContent, 0, 0);
                ctx.restore();
            }
        } else {
            // 处理福字卡片
            const charEl = element.querySelector('.char');
            if (charEl) {
                const cRect = charEl.getBoundingClientRect();
                const cx = cRect.left - rect.left;
                const cy = cRect.top - rect.top;
                const cStyle = window.getComputedStyle(charEl);
                
                ctx.save();
                ctx.translate(cx + cRect.width / 2, cy + cRect.height / 2);
                
                const transform = cStyle.transform;
                if (transform && transform !== 'none') {
                    try {
                        const matrix = new DOMMatrix(transform);
                        ctx.setTransform(matrix.a, matrix.b, matrix.c, matrix.d, matrix.e, matrix.f);
                    } catch (e) {
                        // 如果 DOMMatrix 不支持，尝试解析 transform
                        const match = transform.match(/rotate\(([^)]+)\)/);
                        if (match) {
                            ctx.rotate(parseFloat(match[1]) * Math.PI / 180);
                        }
                    }
                }
                
                ctx.font = `${cStyle.fontStyle} ${cStyle.fontWeight} ${cStyle.fontSize} ${cStyle.fontFamily}`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                const stroke = cStyle.webkitTextStroke;
                if (stroke && stroke !== '0px none') {
                    const parts = stroke.split(' ');
                    ctx.strokeStyle = parts[1] || '#1a0505';
                    ctx.lineWidth = parseFloat(parts[0]) || 1;
                    ctx.strokeText(charEl.textContent, 0, 0);
                } else {
                    ctx.fillStyle = cStyle.color;
                    ctx.fillText(charEl.textContent, 0, 0);
                }
                
                ctx.restore();
            }
        }
        
        canvas.toBlob((blob) => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 'image/png');
    }
    
    // 长按检测（每个元素独立的 timer）
    const longPressTimers = new WeakMap();
    const LONG_PRESS_DURATION = 500; // 500ms
    
    function setupLongPressSave(element, filenameOrFn) {
        const getFilename = typeof filenameOrFn === 'function' ? filenameOrFn : () => filenameOrFn;
        let longPressed = false;
        
        // 移动端：长按保存
        element.addEventListener('touchstart', (e) => {
            longPressed = false;
            const timer = setTimeout(() => {
                longPressed = true;
                e.preventDefault();
                saveFuAsImage(element, getFilename());
                // 触觉反馈（如果支持）
                if (navigator.vibrate) {
                    navigator.vibrate(50);
                }
                // 视觉反馈
                element.style.opacity = '0.7';
                setTimeout(() => {
                    element.style.opacity = '';
                    longPressed = false;
                }, 300);
            }, LONG_PRESS_DURATION);
            longPressTimers.set(element, timer);
        }, { passive: false });
        
        element.addEventListener('touchend', (e) => {
            const timer = longPressTimers.get(element);
            if (timer) {
                clearTimeout(timer);
                longPressTimers.delete(element);
            }
            // 如果触发了长按，阻止后续的点击事件
            if (longPressed) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
        
        element.addEventListener('touchmove', () => {
            const timer = longPressTimers.get(element);
            if (timer) {
                clearTimeout(timer);
                longPressTimers.delete(element);
            }
        });
        
        // 桌面端：右键保存
        element.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            saveFuAsImage(element, getFilename());
        });
        
        // 添加提示
        element.setAttribute('title', 'Long press or right-click to save');
        
        // 存储长按标志到元素上，供点击事件检查
        element._longPressed = () => longPressed;
    }
    
    // 为预览区域添加保存功能
    setupLongPressSave(previewArea, getSaveFilename);
    
    // 预览区域点击保存按钮
    const savePreviewBtn = document.getElementById('save-preview-btn');
    if (savePreviewBtn) {
        savePreviewBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            saveFuAsImage(previewArea, getSaveFilename());
            savePreviewBtn.classList.remove('show');
        });
        
        // 点击预览区域显示/隐藏保存按钮
        previewArea.addEventListener('click', (e) => {
            if (e.target === savePreviewBtn || savePreviewBtn.contains(e.target)) {
                return;
            }
            savePreviewBtn.classList.toggle('show');
        });
    }
    
    // 点击外部关闭所有保存按钮
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.preview-area') && !e.target.closest('.fu-card')) {
            if (savePreviewBtn) {
                savePreviewBtn.classList.remove('show');
            }
            document.querySelectorAll('.fu-card-save-btn.show').forEach(btn => {
                btn.classList.remove('show');
            });
        }
    });

    init();
});
