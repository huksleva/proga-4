
let currentUrl = '';

function getPresignedUrl(filename) {
    fetch(`/presigned/${encodeURIComponent(filename)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentUrl = data.url;
                document.getElementById('urlText').textContent = data.url;
                document.getElementById('urlModal').style.display = 'block';
            } else {
                alert('Ошибка: ' + data.error);
            }
        })
        .catch(error => {
            alert('Ошибка при получении URL: ' + error);
        });
}

function closeModal() {
    document.getElementById('urlModal').style.display = 'none';
}

function copyUrl() {
    navigator.clipboard.writeText(currentUrl).then(() => {
        alert('URL скопирован в буфер обмена!');
    }).catch(err => {
        alert('Ошибка при копировании: ' + err);
    });
}

// Закрытие модалки при клике вне её
window.onclick = function (event) {
    const modal = document.getElementById('urlModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}