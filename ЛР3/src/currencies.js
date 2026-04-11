
// Находим форму для обновления курсов валют
const updateCurrenciesButton = document.getElementById('123');

// Вешаем слушатель на отправку формы
updateCurrenciesButton.addEventListener('click', async function(event) {
    event.preventDefault(); // Блокируем перезагрузку

    try {
        // 2. Отправляем GET-запрос на сервер
        const response = await fetch('/currencies/update', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
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



