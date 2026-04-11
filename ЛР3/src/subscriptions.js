
// Находим форму для добавления подписки пользователя на валюту
const addSubscriptionToUser = document.getElementById('addSubscriptionToUser');

// Вешаем слушатель на отправку формы
addSubscriptionToUser.addEventListener('submit', async function(event) {
    event.preventDefault(); // Блокируем перезагрузку

    // 1. Собираем данные
    const formData = new FormData(addSubscriptionToUser);
    const userId = formData.get('user_id');
    const currencyId = formData.get('currency_id');

    try {
        // 2. Отправляем POST-запрос на сервер
        const response = await fetch('/subscriptions', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: formData
        });

        const result = await response.json();
        // console.log('Ответ сервера:', result);

        // 3. Обрабатываем успех
        if (result.status === 'success') {

            // Ищем таблицу подписок и добавляем новую строку
            const subscriptionsTable = document.getElementById('subscriptionsList');
            if (subscriptionsTable) {
                // Удаляем строку "Нет подписок", если есть
                const emptyRow = document.getElementById('noSubscriptionsRow');
                if (emptyRow) emptyRow.remove();

                // Создаём новую строку
                const newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td>${result.user_id}</td>
                    <td>${result.currency_id}</td>
                `;
                subscriptionsTable.appendChild(newRow);
            }

            // Очищаем форму и показываем успех
            addSubscriptionToUser.reset();
            // alert(result.message || "Подписка добавлена!");

        } else {
            // Обработка ошибки (например, "подписка уже существует")
            alert("Ошибка: " + (result.message || result.msg || "Неизвестная ошибка"));
        }

    } catch (error) {
        console.error("Ошибка сети:", error);
        alert("Не удалось связаться с сервером");
    }


})




// Находим форму для удаления подписки пользователя на валюту
const deleteSubscriptionToUser = document.getElementById('deleteSubscriptionToUser');

// Вешаем слушатель на отправку формы
deleteSubscriptionToUser.addEventListener('submit', async function(event) {
    event.preventDefault(); // Блокируем перезагрузку

    // 1. Собираем данные
    const formData = new FormData(deleteSubscriptionToUser);
    const userId = formData.get('user_id');
    const currencyId = formData.get('currency_id');

    try {
        // 2. Отправляем POST-запрос на сервер
        const response = await fetch('/subscriptions', {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json'
            },
            body: formData
        });



    } catch (error) {
        console.error("Ошибка сети:", error);
        alert("Не удалось связаться с сервером");
    }



})





