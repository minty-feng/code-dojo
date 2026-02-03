/**
 * 代码块复制功能
 * 在代码块右上角添加复制按钮
 */

(function() {
    'use strict';

    // 复制文本到剪贴板
    function copyToClipboard(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            return navigator.clipboard.writeText(text).then(
                function() {
                    return true;
                },
                function() {
                    // 降级方案
                    return fallbackCopyToClipboard(text);
                }
            );
        } else {
            return Promise.resolve(fallbackCopyToClipboard(text));
        }
    }

    // 降级复制方案（兼容旧浏览器）
    function fallbackCopyToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            const successful = document.execCommand('copy');
            document.body.removeChild(textArea);
            return successful;
        } catch (err) {
            document.body.removeChild(textArea);
            return false;
        }
    }

    // 获取代码块文本
    function getCodeText(codeBlock) {
        // 如果是带行号的表格结构
        const codeCell = codeBlock.querySelector('.code pre, .code code, pre code, code');
        if (codeCell) {
            return codeCell.textContent || codeCell.innerText;
        }
        // 普通代码块
        const pre = codeBlock.querySelector('pre');
        if (pre) {
            return pre.textContent || pre.innerText;
        }
        return codeBlock.textContent || codeBlock.innerText;
    }

    // 创建复制按钮
    function createCopyButton() {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.setAttribute('aria-label', '复制代码');
        button.setAttribute('title', '复制代码');
        
        // 使用SVG图标 - 复制图标（单个方框，居中显示）
        const copyIcon = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: block; margin: 0;">
                <rect x="6" y="6" width="12" height="12" rx="1.5" ry="1.5"></rect>
            </svg>
        `;
        
        // 使用SVG图标 - 成功图标
        const checkIcon = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
        `;
        
        button.innerHTML = copyIcon;
        button.dataset.copyIcon = copyIcon;
        button.dataset.checkIcon = checkIcon;
        
        return button;
    }

    // 添加复制按钮到代码块
    function addCopyButton(codeBlock) {
        // 检查是否已经添加了按钮
        if (codeBlock.querySelector('.copy-button')) {
            return;
        }

        const button = createCopyButton();
        codeBlock.appendChild(button);

        // 绑定点击事件
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const codeText = getCodeText(codeBlock);
            
            copyToClipboard(codeText).then(function(success) {
                if (success) {
                    // 显示成功提示
                    button.classList.add('copied');
                    button.innerHTML = button.dataset.checkIcon;
                    button.setAttribute('title', '已复制！');

                    // 2秒后恢复
                    setTimeout(function() {
                        button.classList.remove('copied');
                        button.innerHTML = button.dataset.copyIcon;
                        button.setAttribute('title', '复制代码');
                    }, 2000);
                } else {
                    // 复制失败提示
                    const errorIcon = `
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="12" y1="8" x2="12" y2="12"></line>
                            <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                    `;
                    button.innerHTML = errorIcon;
                    button.setAttribute('title', '复制失败');
                    setTimeout(function() {
                        button.innerHTML = button.dataset.copyIcon;
                        button.setAttribute('title', '复制代码');
                    }, 2000);
                }
            });
        });
    }

    // 初始化所有代码块
    function initCopyButtons() {
        // 查找所有代码块
        const codeBlocks = document.querySelectorAll(
            '.highlight, .highlighttable, div[class*="highlight"]'
        );

        codeBlocks.forEach(function(block) {
            // 排除行内代码
            if (block.closest('p, li, td, th')) {
                return;
            }
            addCopyButton(block);
        });
    }

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCopyButtons);
    } else {
        initCopyButtons();
    }

    // 监听动态内容加载（如AJAX加载的内容）
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    const codeBlocks = node.querySelectorAll
                        ? node.querySelectorAll('.highlight, .highlighttable, div[class*="highlight"]')
                        : [];
                    codeBlocks.forEach(addCopyButton);
                }
            });
        });
    });

    // 开始观察
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
})();

