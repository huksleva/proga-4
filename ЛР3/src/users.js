
// Находим форму создания пользователя
const createUserForm = document.getElementById('createUserForm');

// Вешаем слушатель на отправку формы
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
        if (result.status === "success") {
            // Удаляем строку "Таблица пуста", если она есть
            const emptyRow = document.getElementById('emptyRow');
            if (emptyRow) emptyRow.remove();

            // Обновляем страницу без перезагрузки (добавляем элемент в список)
            const newRow = document.createElement('tr');

            newRow.innerHTML = `
                <td>${result.id}</td>
                <td><a href="/users/${result.id}">${result.username}</a></td>
                <td>${result.email}</td>
                <td>${result.created_at}</td>
            `

            // Добавляем строку в tbody
            document.getElementById('userList').appendChild(newRow);

            // Очищаем форму
            createUserForm.reset();

            // Выводим сообщение на экран
            alert(result.msg);
        } else {
            alert("Ошибка: " + result.msg);
        }

    } catch (error) {
        console.error("Ошибка сети:", error);
    }
})



// Находим форму удаления пользователя
const deleteUserForm = document.getElementById('deleteUserForm');

// Вешаем слушатель на отправку формы
deleteUserForm.addEventListener('submit', async function(event) {
    // Запрещаем стандартную отправку формы (перезагрузку страницы)
    event.preventDefault();

    // Получаем ID из поля формы
    const userId = deleteUserForm.querySelector('[name="user_id"]').value;

    try {
        // Отправляем DELETE на /users/{id}, а не на /users
        const response = await fetch(`/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json' // Гарантируем, что сервер вернёт JSON
            }
            // Не отправляем body: для DELETE с path-параметром он не нужен
        });


        // Получаем JSON ответ
        const result = await response.json();

        // Обрабатываем ответ
        if (result.status === "success") {
            // Удаляем строку из таблицы визуально (по ID)
            const row = document.querySelector(`#userList tr td:first-child:nth-child(1):contains('${userId}')`)?.closest('tr');
            // Проще: перебираем все строки и сравниваем текст первой ячейки
            const rows = document.querySelectorAll('#userList tr');
            for (const row of rows) {
                const idCell = row.querySelector('td:first-child');
                if (idCell && idCell.textContent === userId) {
                    row.remove();
                    break;
                }
            }

            // Очищаем ИМЕННО эту форму
            deleteUserForm.reset();
            alert(result.msg);

        } else {
            alert("Ошибка: " + result.msg);
        }

    } catch (error) {
        console.error("Ошибка сети:", error);
        alert("Не удалось связаться с сервером");
    }

})

