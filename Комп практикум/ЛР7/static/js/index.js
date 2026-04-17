let currentUrl = '';
let urlModal = null;

// Инициализация модального окна Bootstrap
document.addEventListener('DOMContentLoaded', function () {
    urlModal = new bootstrap.Modal(document.getElementById('urlModal'));
});

function getPresignedUrl(filename) {
    fetch(`/presigned/${encodeURIComponent(filename)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentUrl = data.url;
                document.getElementById('urlText').value = data.url;
                urlModal.show();
            } else {
                alert('Ошибка: ' + data.error);
            }
        })
        .catch(error => {
            alert('Ошибка при получении URL: ' + error);
        });
}

function closeModal() {
    urlModal.hide();
}

function copyUrl() {
    const urlInput = document.getElementById('urlText');
    urlInput.select();
    urlInput.setSelectionRange(0, 99999); // Для мобильных устройств
    navigator.clipboard.writeText(currentUrl).then(() => {
        // Показываем визуальное подтверждение
        const btn = event.target.closest('button');
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<i class="bi bi-check me-1"></i>Скопировано!';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-success');
        setTimeout(() => {
            btn.innerHTML = originalHTML;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-primary');
        }, 2000);
    }).catch(err => {
        alert('Ошибка при копировании: ' + err);
    });
}