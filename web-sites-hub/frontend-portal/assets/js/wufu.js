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
        fuDisplay.style.fontSize = `${state.size / 10}rem`;
        
        previewArea.style.backgroundColor = state.bgColor;
        
        // Update doufang border
        doufang.style.borderColor = state.borderColor; // Outer diamond
        // Pseudo element for dashed border needs to be updated via custom property usually, 
        // but simple border color on parent works for the solid part.
        // For the dashed part:
        const sheet = document.styleSheets[0];
        // Note: Changing pseudo-element styles from JS is tricky. 
        // We actally used a ::before on .doufang in CSS.
        // Let's replace the logic to use CSS Variables for easy updates.
        previewArea.style.setProperty('--border-color', state.borderColor);
        doufang.style.borderColor = state.borderColor;
        // In JS we can modify inline style for custom property if we update CSS to use it
        // OR we just toggle classes. But let's stick to inline styles where possible.
        // Quick fix: Set inner HTML for doufang to include a real div instead of pseudo if needed,
        // but for now, let's assume the outer border is enough customization.
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
        deck.forEach(fontMeta => {
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
            
            // Slight rotation for natural look (accumulate with any transform in style)
            // If style has transform, we need to append
            const randomRotate = (Math.random() * 10 - 5).toFixed(1);
            if (content.style.transform) {
                content.style.transform += ` rotate(${randomRotate}deg)`;
            } else {
                content.style.transform = `rotate(${randomRotate}deg)`;
            }

            // Tooltip
            const tooltip = document.createElement('div');
            tooltip.className = 'fu-tooltip';
            tooltip.innerHTML = `
                <span class="font-name">${fontMeta.name}</span>
                <span class="font-desc">${fontMeta.desc}</span>
            `;

            card.appendChild(content);
            card.appendChild(tooltip);
            
            // Add click handler to "adopt" this style
            card.addEventListener('click', () => {
                // Copy style to main editor
                state.font = font;
                
                // Copy other visual properties if we want strict What-You-See-Is-What-You-Get
                // Note: The main editor logic is simpler, so we mainly copy the Font Family.
                // If we wanted to copy Bold/Italic, we'd need to update State to support it.
                // For now, let's stick to copying the Font Family.
                
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
                // Scroll to top
                previewArea.scrollIntoView({ behavior: 'smooth' });
            });

            fragment.appendChild(card);
        });

        fuGrid.innerHTML = ''; // Clear existing
        fuGrid.appendChild(fragment);
    }

    init();
});
