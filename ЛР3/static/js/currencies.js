
// Находим форму для добавления подписки пользователя на валюту
const updateCurrenciesButton = document.getElementById('updateCurrenciesButton');

async function updateCurrenciesTable() {
    try {
        // Получаем список валют
        const response = await fetch("/api/currencies", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
            // Не отправляем body, здесь мы ничего не передаём
        });

        if (!response.ok) {
            console.log(`Ошибка ${response.status}: ${response.statusText}`);
        }

        const currencies = await response.json();

        // Находим tbody таблицы
        const tbody = document.querySelector('#currenciesTableBody');
        if (!tbody) {
            console.error('Не найден элемент #currenciesTableBody');
            return;
        }

        // Очищаем текущие строки
        tbody.innerHTML = '';

        // Если валют нет — показываем сообщение
        if (currencies.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center py-4">
                        Таблица пуста
                    </td>
                </tr>
            `;
            return;
        }

        // Создаём строки для каждой валюты
        currencies.forEach(curr => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${curr.id || '—'}</td>
                <td>${curr.code || '—'}</td>
                <td>${curr.name || '—'}</td>
            `;
            tbody.appendChild(row);
        });
        console.log(`Таблица обновлена: ${currencies.length} валют`);

    } catch (e) {
        console.error('Не удалось обновить таблицу:', e);
        // location.reload(); // На крайний случай - полная перезагрузка
    }
}

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

        console.log(result.message)
        console.log("Кол-во обновлённых валют:", result.count)

        // Обновляем таблицу асинхронно
        await updateCurrenciesTable()

    } catch (error) {
        console.error("Ошибка сети:", error);
        alert("Не удалось связаться с сервером");
    }
})