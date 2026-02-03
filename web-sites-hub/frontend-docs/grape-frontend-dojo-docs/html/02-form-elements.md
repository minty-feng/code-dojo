# 02-表单元素详解

## 📋 学习目标
- 掌握HTML表单的基本结构
- 熟悉各类表单输入控件
- 理解表单验证机制
- 学习表单最佳实践

## 📝 表单基础

### 基本结构
```html
<form action="/submit" method="POST" enctype="multipart/form-data">
    <!-- 表单控件 -->
    <label for="username">用户名：</label>
    <input type="text" id="username" name="username" required>
    
    <button type="submit">提交</button>
</form>
```

### form属性详解
```html
<!-- action：提交地址 -->
<form action="/api/submit">

<!-- method：提交方法 -->
<form method="GET">  <!-- 默认，数据在URL中 -->
<form method="POST"> <!-- 数据在请求体中 -->

<!-- enctype：编码类型 -->
<form enctype="application/x-www-form-urlencoded"> <!-- 默认 -->
<form enctype="multipart/form-data">  <!-- 文件上传必需 -->
<form enctype="text/plain">  <!-- 纯文本 -->

<!-- target：提交目标窗口 -->
<form target="_blank">  <!-- 新窗口 -->
<form target="_self">   <!-- 当前窗口，默认 -->

<!-- autocomplete：自动完成 -->
<form autocomplete="on">  <!-- 启用，默认 -->
<form autocomplete="off"> <!-- 禁用 -->

<!-- novalidate：禁用HTML5验证 -->
<form novalidate>
```

## 🔤 文本输入

### 基本文本框
```html
<!-- 单行文本 -->
<input type="text" 
       name="username" 
       id="username"
       placeholder="请输入用户名"
       value="默认值"
       maxlength="20"
       minlength="3"
       pattern="[A-Za-z0-9]+"
       required
       autofocus
       autocomplete="username">

<!-- 多行文本 -->
<textarea name="comment" 
          id="comment"
          rows="5" 
          cols="40"
          placeholder="请输入评论"
          maxlength="500"
          required></textarea>

<!-- 不可调整大小的textarea -->
<textarea style="resize: none;"></textarea>
```

### 专用输入类型
```html
<!-- 密码 -->
<input type="password" 
       name="password" 
       autocomplete="current-password"
       minlength="8"
       required>

<!-- 邮箱（自动验证格式） -->
<input type="email" 
       name="email"
       placeholder="example@domain.com"
       autocomplete="email"
       required>

<!-- 电话 -->
<input type="tel" 
       name="phone"
       pattern="[0-9]{3}-[0-9]{4}-[0-9]{4}"
       placeholder="138-0000-0000">

<!-- URL -->
<input type="url" 
       name="website"
       placeholder="https://example.com"
       pattern="https://.*">

<!-- 搜索框 -->
<input type="search" 
       name="q"
       placeholder="搜索...">
```

## 🔢 数字和日期

### 数字输入
```html
<!-- 数字 -->
<input type="number" 
       name="age"
       min="0"
       max="120"
       step="1"
       value="18">

<!-- 范围滑块 -->
<input type="range" 
       name="volume"
       min="0"
       max="100"
       step="5"
       value="50">
<output for="volume">50</output>

<!-- 实时显示range值 -->
<input type="range" id="slider" min="0" max="100" value="50"
       oninput="document.getElementById('output').value = this.value">
<output id="output">50</output>
```

### 日期和时间
```html
<!-- 日期 -->
<input type="date" 
       name="birthday"
       min="1900-01-01"
       max="2025-12-31">

<!-- 时间 -->
<input type="time" 
       name="appointment"
       step="900"> <!-- 15分钟间隔 -->

<!-- 日期时间（本地） -->
<input type="datetime-local" 
       name="meeting"
       step="1"> <!-- 包含秒 -->

<!-- 月份 -->
<input type="month" name="start-month">

<!-- 周 -->
<input type="week" name="week">

<!-- 设置默认值 -->
<input type="date" value="2025-10-21">
<input type="time" value="14:30">
<input type="datetime-local" value="2025-10-21T14:30">
```

## ☑️ 选择控件

### 复选框
```html
<!-- 单个复选框 -->
<input type="checkbox" 
       name="agree" 
       id="agree"
       value="yes"
       required>
<label for="agree">我同意服务条款</label>

<!-- 多个复选框 -->
<fieldset>
    <legend>兴趣爱好：</legend>
    <input type="checkbox" name="hobbies" id="reading" value="reading">
    <label for="reading">阅读</label>
    
    <input type="checkbox" name="hobbies" id="sports" value="sports">
    <label for="sports">运动</label>
    
    <input type="checkbox" name="hobbies" id="music" value="music" checked>
    <label for="music">音乐</label>
</fieldset>

<!-- 不确定状态（通过JavaScript） -->
<input type="checkbox" id="indeterminate">
<script>
document.getElementById('indeterminate').indeterminate = true;
</script>
```

### 单选按钮
```html
<fieldset>
    <legend>性别：</legend>
    <input type="radio" name="gender" id="male" value="male" checked>
    <label for="male">男</label>
    
    <input type="radio" name="gender" id="female" value="female">
    <label for="female">女</label>
    
    <input type="radio" name="gender" id="other" value="other">
    <label for="other">其他</label>
</fieldset>
```

**要点**：
- 同一组单选按钮的name属性必须相同
- 使用label提升用户体验（点击文字也能选中）
- checked属性设置默认选中项

### 下拉选择
```html
<!-- 基本下拉框 -->
<select name="city" id="city" required>
    <option value="">请选择城市</option>
    <option value="beijing">北京</option>
    <option value="shanghai" selected>上海</option>
    <option value="guangzhou">广州</option>
    <option value="shenzhen">深圳</option>
</select>

<!-- 分组选项 -->
<select name="country">
    <optgroup label="亚洲">
        <option value="cn">中国</option>
        <option value="jp">日本</option>
        <option value="kr">韩国</option>
    </optgroup>
    <optgroup label="欧洲">
        <option value="uk">英国</option>
        <option value="fr">法国</option>
        <option value="de">德国</option>
    </optgroup>
</select>

<!-- 多选下拉框 -->
<select name="skills" multiple size="5">
    <option value="html">HTML</option>
    <option value="css">CSS</option>
    <option value="js">JavaScript</option>
    <option value="react">React</option>
    <option value="vue">Vue</option>
</select>

<!-- 禁用选项 -->
<select name="role">
    <option value="user">普通用户</option>
    <option value="admin" disabled>管理员（不可选）</option>
</select>
```

## 📁 文件上传

### 文件输入
```html
<!-- 单文件上传 -->
<input type="file" 
       name="avatar" 
       id="avatar"
       accept="image/*">

<!-- 多文件上传 -->
<input type="file" 
       name="photos" 
       multiple
       accept="image/png, image/jpeg, image/jpg">

<!-- 指定文件类型 -->
<input type="file" accept=".pdf,.doc,.docx">
<input type="file" accept="image/*">  <!-- 所有图片 -->
<input type="file" accept="video/*">  <!-- 所有视频 -->
<input type="file" accept="audio/*">  <!-- 所有音频 -->

<!-- 拍照上传（移动端） -->
<input type="file" accept="image/*" capture="camera">
<input type="file" accept="video/*" capture="camcorder">
```

### 文件上传最佳实践
```html
<form enctype="multipart/form-data" method="POST">
    <label for="file-upload">选择文件：</label>
    <input type="file" 
           id="file-upload" 
           name="file"
           accept="image/png,image/jpeg"
           required>
    
    <!-- 文件大小限制通过JavaScript验证 -->
    <p class="help-text">支持PNG、JPEG格式，大小不超过5MB</p>
    
    <button type="submit">上传</button>
</form>

<script>
document.getElementById('file-upload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    if (file && file.size > maxSize) {
        alert('文件大小不能超过5MB');
        this.value = '';
    }
});
</script>
```

## 🎨 其他输入类型

### 颜色选择器
```html
<input type="color" 
       name="theme-color" 
       value="#ff6b6b">
```

### 隐藏字段
```html
<input type="hidden" name="user_id" value="12345">
<input type="hidden" name="csrf_token" value="abc123xyz">
```

## 🔘 按钮

### 按钮类型
```html
<!-- 提交按钮 -->
<button type="submit">提交</button>
<input type="submit" value="提交">

<!-- 重置按钮 -->
<button type="reset">重置</button>
<input type="reset" value="重置">

<!-- 普通按钮 -->
<button type="button" onclick="doSomething()">点击</button>
<input type="button" value="点击" onclick="doSomething()">

<!-- 图片按钮 -->
<input type="image" src="submit-button.png" alt="提交">
```

**推荐使用`<button>`标签**：
- 可以包含HTML内容（图标、文字等）
- 更好的样式控制
- 更语义化

```html
<!-- 带图标的按钮 -->
<button type="submit">
    <svg>...</svg>
    提交表单
</button>
```

## 📋 表单分组

### fieldset和legend
```html
<form>
    <fieldset>
        <legend>基本信息</legend>
        <label for="name">姓名：</label>
        <input type="text" id="name" name="name">
        
        <label for="email">邮箱：</label>
        <input type="email" id="email" name="email">
    </fieldset>
    
    <fieldset disabled>
        <legend>高级设置（已禁用）</legend>
        <input type="checkbox" name="advanced" value="1">
        <label>启用高级功能</label>
    </fieldset>
</form>
```

### 标签关联
```html
<!-- 方式1：for属性关联 -->
<label for="username">用户名：</label>
<input type="text" id="username" name="username">

<!-- 方式2：包裹input -->
<label>
    用户名：
    <input type="text" name="username">
</label>

<!-- 多个label关联同一input -->
<label for="email-input">邮箱地址：</label>
<input type="email" id="email-input" name="email" aria-labelledby="email-label">
<label id="email-label">用于接收通知</label>
```

## ✅ HTML5表单验证

### 内置验证属性
```html
<!-- required：必填 -->
<input type="text" name="username" required>

<!-- pattern：正则验证 -->
<input type="text" 
       pattern="[A-Za-z0-9]{6,12}"
       title="6-12位字母或数字">

<!-- minlength/maxlength：长度限制 -->
<input type="text" minlength="3" maxlength="20">

<!-- min/max：数值范围 -->
<input type="number" min="1" max="100">
<input type="date" min="2025-01-01" max="2025-12-31">

<!-- step：步进值 -->
<input type="number" step="0.01">  <!-- 允许小数 -->
<input type="range" step="5">  <!-- 5的倍数 -->
```

### 验证状态CSS伪类
```css
/* 必填字段 */
input:required {
    border-color: #ff6b6b;
}

/* 可选字段 */
input:optional {
    border-color: #999;
}

/* 验证通过 */
input:valid {
    border-color: #51cf66;
}

/* 验证失败 */
input:invalid {
    border-color: #ff6b6b;
}

/* 范围内 */
input:in-range {
    border-color: #51cf66;
}

/* 超出范围 */
input:out-of-range {
    border-color: #ff6b6b;
}
```

### 自定义验证消息
```html
<input type="email" 
       id="email" 
       required
       oninvalid="this.setCustomValidity('请输入有效的邮箱地址')"
       oninput="this.setCustomValidity('')">

<script>
const emailInput = document.getElementById('email');
emailInput.addEventListener('invalid', function(e) {
    if (this.validity.valueMissing) {
        this.setCustomValidity('邮箱不能为空');
    } else if (this.validity.typeMismatch) {
        this.setCustomValidity('请输入正确的邮箱格式');
    }
});

emailInput.addEventListener('input', function() {
    this.setCustomValidity('');
});
</script>
```

### JavaScript验证API
```javascript
const form = document.getElementById('myForm');
const input = document.getElementById('myInput');

// 检查单个字段
if (input.checkValidity()) {
    console.log('验证通过');
} else {
    console.log('验证失败：', input.validationMessage);
}

// 检查整个表单
if (form.checkValidity()) {
    console.log('表单验证通过');
} else {
    console.log('表单验证失败');
}

// 手动触发验证
form.reportValidity();  // 显示验证错误信息

// validity对象属性
console.log(input.validity.valid);         // 是否有效
console.log(input.validity.valueMissing);  // 是否缺少必填值
console.log(input.validity.typeMismatch);  // 类型不匹配
console.log(input.validity.patternMismatch); // 正则不匹配
console.log(input.validity.tooLong);       // 超过maxlength
console.log(input.validity.tooShort);      // 小于minlength
console.log(input.validity.rangeUnderflow); // 小于min
console.log(input.validity.rangeOverflow);  // 大于max
console.log(input.validity.stepMismatch);   // 不符合step
```

## 🎯 完整表单示例

### 用户注册表单
```html
<form id="registerForm" action="/register" method="POST" novalidate>
    <h2>用户注册</h2>
    
    <!-- 用户名 -->
    <div class="form-group">
        <label for="username">用户名 *</label>
        <input type="text" 
               id="username" 
               name="username"
               pattern="[A-Za-z0-9_]{4,16}"
               title="4-16位字母、数字或下划线"
               required
               autocomplete="username">
        <span class="error-message"></span>
    </div>
    
    <!-- 邮箱 -->
    <div class="form-group">
        <label for="email">邮箱 *</label>
        <input type="email" 
               id="email" 
               name="email"
               required
               autocomplete="email">
        <span class="error-message"></span>
    </div>
    
    <!-- 密码 -->
    <div class="form-group">
        <label for="password">密码 *</label>
        <input type="password" 
               id="password" 
               name="password"
               minlength="8"
               pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
               title="至少8位，包含大小写字母和数字"
               required
               autocomplete="new-password">
        <span class="error-message"></span>
    </div>
    
    <!-- 确认密码 -->
    <div class="form-group">
        <label for="confirm-password">确认密码 *</label>
        <input type="password" 
               id="confirm-password" 
               name="confirm_password"
               required
               autocomplete="new-password">
        <span class="error-message"></span>
    </div>
    
    <!-- 生日 -->
    <div class="form-group">
        <label for="birthday">生日</label>
        <input type="date" 
               id="birthday" 
               name="birthday"
               min="1900-01-01"
               max="2025-12-31">
    </div>
    
    <!-- 性别 -->
    <fieldset>
        <legend>性别</legend>
        <label><input type="radio" name="gender" value="male"> 男</label>
        <label><input type="radio" name="gender" value="female"> 女</label>
        <label><input type="radio" name="gender" value="other"> 其他</label>
    </fieldset>
    
    <!-- 兴趣 -->
    <fieldset>
        <legend>兴趣爱好</legend>
        <label><input type="checkbox" name="hobbies" value="reading"> 阅读</label>
        <label><input type="checkbox" name="hobbies" value="sports"> 运动</label>
        <label><input type="checkbox" name="hobbies" value="music"> 音乐</label>
        <label><input type="checkbox" name="hobbies" value="travel"> 旅游</label>
    </fieldset>
    
    <!-- 同意条款 -->
    <div class="form-group">
        <label>
            <input type="checkbox" name="agree" required>
            我已阅读并同意<a href="/terms">服务条款</a>
        </label>
    </div>
    
    <!-- 按钮 -->
    <div class="form-actions">
        <button type="submit">注册</button>
        <button type="reset">重置</button>
    </div>
</form>

<script>
const form = document.getElementById('registerForm');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm-password');

// 密码确认验证
confirmPassword.addEventListener('input', function() {
    if (this.value !== password.value) {
        this.setCustomValidity('两次密码输入不一致');
    } else {
        this.setCustomValidity('');
    }
});

// 表单提交
form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (this.checkValidity()) {
        const formData = new FormData(this);
        console.log('提交数据：', Object.fromEntries(formData));
        // 实际项目中这里发送AJAX请求
    } else {
        this.reportValidity();
    }
});
</script>
```

## 📚 实践练习

### 练习1：登录表单
创建一个登录表单，包含：
- 用户名/邮箱输入
- 密码输入
- 记住我复选框
- 提交和忘记密码链接
- 实现客户端验证

### 练习2：问卷调查表单
创建一个调查问卷，包含：
- 单选题（满意度评分）
- 多选题（产品功能）
- 文本题（建议反馈）
- 提交后显示结果

### 练习3：文件上传表单
创建文件上传表单，包含：
- 图片预览功能
- 文件大小和类型验证
- 上传进度显示
- 多文件上传支持

## 💡 最佳实践

### 1. 可访问性
- 为所有表单控件添加label
- 使用fieldset和legend分组
- 提供清晰的错误提示
- 支持键盘导航

### 2. 用户体验
- 使用合适的输入类型（自动调起键盘）
- 提供placeholder和提示信息
- 实时验证反馈
- 合理使用autocomplete

### 3. 安全性
- 服务端必须验证所有数据
- 使用CSRF令牌
- 密码字段使用type="password"
- 敏感操作需要二次确认

### 4. 性能优化
- 避免过度的实时验证
- 使用防抖处理输入事件
- 适当使用HTML5验证而非JavaScript
- 表单数据序列化优化

## 📚 参考资料
- [MDN 表单指南](https://developer.mozilla.org/zh-CN/docs/Learn/Forms)
- [W3C Forms规范](https://www.w3.org/TR/html52/sec-forms.html)
- [WCAG表单可访问性](https://www.w3.org/WAI/tutorials/forms/)

