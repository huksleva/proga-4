
// Находим форму
const createUserForm = document.getElementById('createUserForm');

// Вешаем слушатель на отправку
createUserForm.addEventListener('submit', async function(event) {
    // Запрещаем стандартную отправку формы (перезагрузку страницы)
    event.preventDefault();

    // 3. Собираем данные из полей
    const formData = new FormData(createUserForm);

    try {
        // 4. Отправляем запрос на сервер
        const response = await fetch('/users', {
            method: 'POST',
            body: formData // Отправляем как form-data (сервер поймет Form(...))
        });

        // 5. Получаем JSON ответ
        const result = await response.json();

        // 6. Обрабатываем ответ
        if (result.success) {
            // Удаляем строку "Таблица пуста", если она есть
            const emptyRow = document.getElementById('emptyRow');
            if (emptyRow) emptyRow.remove();

            // Обновляем страницу без перезагрузки (добавляем элемент в список)
            const newRow = document.createElement('tr');

            newRow.innerHTML = `
                <td>${result.id}</td>
                <td><a href="/users/${result.id}">${result.name}</a></td>
                <td>${result.email}</td>
                <td>${result.created_at}</td>
            `

            // Добавляем строку в tbody
            document.getElementById('userList').appendChild(newRow);

            // Очищаем форму
            createUserForm.reset();

            // Выводим сообщение на экран
            alert(result.message);
        } else {
            alert("Ошибка: " + result.message);
        }

    } catch (error) {
        console.error("Ошибка сети:", error);
    }
});
