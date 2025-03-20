document.addEventListener('DOMContentLoaded', function() {
    // 设置默认的交互时间为当前时间
    const now = new Date();
    const utcString = now.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
    document.getElementById('interaction_time').value = utcString;
    
    // 预览PDF按钮事件
    document.getElementById('previewPdf').addEventListener('click', function() {
        // 显示加载状态
        const pdfViewer = document.getElementById('pdfViewer');
        pdfViewer.src = '';
        pdfViewer.style.backgroundColor = '#f5f5f5';
        
        // 收集表单数据
        const formData = new FormData(document.getElementById('qslForm'));
        
        // 发送AJAX请求
        fetch('/preview_pdf', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // 在iframe中显示PDF
            pdfViewer.src = data.preview_url;
            pdfViewer.style.backgroundColor = '#fff';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('生成PDF预览时出错，请检查控制台获取详细信息。');
        });
    });
    
    // 生成PDF按钮事件
    document.getElementById('generatePdf').addEventListener('click', function() {
        // 收集表单数据
        const formData = new FormData(document.getElementById('qslForm'));
        
        // 发送表单提交请求
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/generate_qsl';
        
        // 将FormData中的数据添加到表单
        for (const [key, value] of formData.entries()) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = key;
            input.value = value;
            form.appendChild(input);
        }
        
        // 添加表单到文档并提交
        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    });
    
    // 自动调整文本区域高度
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // 初始化高度
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
    });
});
