// Загрузка последнего файла при открытии страницы
window.onload = async () => {
    const r = await fetch('/lastUpload');
    if (r.ok) {
        const d = await r.json();
        document.getElementById('lastUploadResult').innerHTML =
            `<h3>Последний файл:</h3><img src="${d.image_url}" style="max-width:400px"><p>${d.filename}</p>`;
    }
};

// Обработчик Form2
document.querySelector('[name="Form2"]').onsubmit = async e => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const r = await fetch('/showPicture', {method:'POST', body:formData});
    const d = await r.json();

    const result = d.image_url
        ? `<img src="${d.image_url}" style="max-width:400px">`
        : d.result;

    document.getElementById('result').innerHTML = result;

    if (d.image_url) {
        document.getElementById('lastUploadResult').innerHTML =
            `<h3>Последний файл:</h3>${result}<p>Загружен только что</p>`;
    }
};