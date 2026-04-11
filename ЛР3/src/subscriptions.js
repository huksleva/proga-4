
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
const deleteUserSubscription = document.getElementById('deleteUserSubscription');

// Вешаем слушатель на отправку формы
deleteUserSubscription.addEventListener('submit', async function(event) {
    event.preventDefault(); // Блокируем перезагрузку

    // 1. Собираем данные
    const formData = new FormData(deleteUserSubscription);
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
        const result = await response.json();

        // 3. Обрабатываем успех
        if (result.status === 'success') {
            // Ищем таблицу подписок и удаляем строку
            const subscriptionsTable = document.getElementById('subscriptionsList');

            if (subscriptionsTable) {

                // Перебор всех строк таблицы
                for (const row of subscriptionsTable.rows) {
                    if (row.id === "noSubscriptionsRow") continue;

                    // Если id пользователя и валюты совпадают, то удаляем строку и выходим из цикла
                    if ((row.cells[0].textContent.trim() === userId) &&
                        (row.cells[1].textContent.trim() === currencyId)) {
                        row.remove();
                        // console.log("Подписка удалена")
                        break;
                    }
                }

                // Если таблица пуста - добавляем заглушку
                const remainingRows = subscriptionsTable.querySelectorAll('tr:not(#noSubscriptionsRow)');
                if (remainingRows.length === 0) {
                    const emptyRow = document.createElement('tr');
                    emptyRow.id = 'noSubscriptionsRow';
                    emptyRow.innerHTML = '<td colspan="2" class="text-center">Нет активных подписок</td>';
                    subscriptionsTable.appendChild(emptyRow);
                }
            }

            // Очищаем форму и показываем успех
            deleteUserSubscription.reset();
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



