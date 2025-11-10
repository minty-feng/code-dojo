// Resume PDF Download Functionality
document.addEventListener('DOMContentLoaded', function() {
    const downloadPdfBtn = document.getElementById('downloadPdfBtn');
    
    if (downloadPdfBtn) {
        downloadPdfBtn.addEventListener('click', function() {
            downloadResumePDF();
        });
    }
});

function downloadResumePDF() {
    // 显示加载状态
    const btn = document.getElementById('downloadPdfBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinner"><circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle><path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"></path></svg><span>生成中...</span>';
    btn.disabled = true;

    // 获取要转换的内容
    const element = document.querySelector('.resume-main');
    const opt = {
        margin: [10, 10, 10, 10],
        filename: 'minty-feng-resume.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { 
            scale: 2,
            useCORS: true,
            logging: false,
            backgroundColor: null
        },
        jsPDF: { 
            unit: 'mm', 
            format: 'a4', 
            orientation: 'portrait',
            compress: true
        },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    };

    // 根据当前主题设置背景色
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    if (isDark) {
        opt.html2canvas.backgroundColor = '#0a0a0f';
    } else {
        opt.html2canvas.backgroundColor = '#ffffff';
    }

    // 生成 PDF
    html2pdf().set(opt).from(element).save().then(function() {
        // 恢复按钮状态
        btn.innerHTML = originalText;
        btn.disabled = false;
        
        // 显示成功提示
        showNotification('PDF 下载成功！');
    }).catch(function(error) {
        console.error('PDF generation error:', error);
        btn.innerHTML = originalText;
        btn.disabled = false;
        showNotification('PDF 生成失败，请重试', 'error');
    });
}

function showNotification(message, type = 'success') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `pdf-notification ${type}`;
    notification.textContent = message;
    
    // 添加样式
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        padding: 1rem 1.5rem;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        color: var(--text-primary);
        font-size: 0.875rem;
        font-weight: 500;
        z-index: 10000;
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(20px);
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // 3秒后移除
    setTimeout(function() {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(function() {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .spinner {
        animation: spin 1s linear infinite;
        display: inline-block;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

