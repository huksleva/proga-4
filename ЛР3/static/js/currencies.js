
// Находим форму для добавления подписки пользователя на валюту
const updateCurrenciesButton = document.getElementById('updateCurrenciesButton');

// Вешаем слушатель на кнопку
updateCurrenciesButton.addEventListener('click', async function(event) {
    event.preventDefault(); // Блокируем перезагрузку

    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch('/currencies/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
            // Не отправляем body, здесь мы ничего не передаём
        })

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail)
            return;
        }

        const count = result.count
        console.log(result.message)





    } catch (error) {
        console.error("Ошибка сети:", error);
        alert("Не удалось связаться с сервером");
    }
})