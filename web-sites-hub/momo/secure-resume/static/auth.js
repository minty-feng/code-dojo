document.addEventListener('DOMContentLoaded', function () {
    const inviteInput = document.getElementById('inviteCode');
    const errorDiv = document.getElementById('error');

    inviteInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            verifyInvite();
        }
    });

    inviteInput.addEventListener('input', function () {
        errorDiv.textContent = '';
    });

    inviteInput.focus();
});

async function verifyInvite() {
    const code = document.getElementById('inviteCode').value.trim();
    const errorDiv = document.getElementById('error');
    const authBtn = document.querySelector('.auth-btn');

    errorDiv.textContent = '';

    if (!code) {
        errorDiv.textContent = '请输入邀请码';
        return;
    }
    if (code.length !== 32) {
        errorDiv.textContent = '邀请码应为32位字符';
        return;
    }

    const originalText = authBtn.innerHTML;
    authBtn.innerHTML =
        '<div class="spinner" style="width: 20px; height: 20px; border-width: 2px;"></div> 验证中...';
    authBtn.disabled = true;

    try {
        const response = await fetch('/api/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
            body: JSON.stringify({ code }),
        });

        const result = await response.json();

        if (result.success) {
            window.location.href = '/';
        } else {
            errorDiv.textContent = result.message;
            document.getElementById('inviteCode').value = '';
            document.getElementById('inviteCode').focus();
        }
    } catch (error) {
        console.error('验证错误:', error);
        errorDiv.textContent = '网络错误，请检查连接后重试';
    } finally {
        authBtn.innerHTML = originalText;
        authBtn.disabled = false;
    }
}

