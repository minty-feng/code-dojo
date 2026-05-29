let statusBubble;
let statusText;
let defaultMessage = '请联系简历主人获取邀请码';

document.addEventListener('DOMContentLoaded', function () {
    const inviteInput = document.getElementById('inviteCode');
    statusBubble = document.getElementById('statusBubble');
    statusText = statusBubble?.querySelector('.status-text');
    defaultMessage = statusText?.textContent?.trim() || defaultMessage;

    inviteInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            verifyInvite();
        }
    });

    inviteInput.addEventListener('input', function () {
        showStatus(defaultMessage);
    });

    showStatus(defaultMessage);
    inviteInput.focus();
});

async function verifyInvite() {
    const codeInput = document.getElementById('inviteCode');
    const code = codeInput.value.trim();
    const authBtn = document.getElementById('authSubmitBtn');

    if (!code) {
        showStatus('请输入邀请码', 'error');
        return;
    }
    if (code.length < 8) {
        showStatus('邀请码格式不正确', 'error');
        return;
    }

    const originalHtml = authBtn.innerHTML;
    authBtn.innerHTML = '<span class="spinner"></span><span class="auth-btn-text">验证中</span>';
    authBtn.disabled = true;
    showStatus('正在验证邀请码…');

    try {
        const response = await fetch('/api/v1/resume/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
            body: JSON.stringify({ key: code }),
        });

        const result = await response.json();

        if (result.success) {
            window.location.href = '/resume';
        } else {
            showStatus(result.message || '邀请码无效', 'error');
            codeInput.value = '';
            codeInput.focus();
        }
    } catch (error) {
        console.error('验证错误:', error);
        showStatus('网络错误，请检查连接后重试', 'error');
    } finally {
        authBtn.innerHTML = originalHtml;
        authBtn.disabled = false;
    }
}

function showStatus(message, type = 'info') {
    if (!statusBubble || !statusText) {
        return;
    }

    const text = message ? message.trim() : defaultMessage;
    statusBubble.classList.toggle('error', type === 'error');
    statusText.textContent = text || defaultMessage;
}
