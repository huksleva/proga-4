const express = require('express')

// Пытаемся взять порт и хост из настроек системы
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || 'localhost';
const app = express()

// Подключаем middleware (промежуточное ПО) для автоматического чтения JSON
app.use(express.json())

// Переменная для хранения количества помпушек
let pompuski = 0




// Регистрируем обработчик для корневого маршрута
app.get('/', (req, res) => {
    res.status(200).json({"Page": "Main page", "Discription": "Для получения информации перейдите на /about, а для добавления помпушек используйте POST запрос на /addPompuski с JSON телом вида {\"count\": число}. Для проверки количества помпушек перейдите на /pompuskiStatus"})
})



app.get('/about', (req, res) => {
    res.status(200).json(
        {"Page": "About page", "Author": "Leonid Tots", "login": 1153307})
})


app.post('/addPompuski', (req, res) => {
    const count = req.body.count
    if (typeof count === 'number' && count >= 0) {
        pompuski += count
        res.status(200).json({"message": `Добавлено ${count} помпушек!`})
    } else {
        res.status(400).json({"error": "Неверный формат данных. 'count' должен быть неотрицательным числом."})
    }
})


app.get('/pompuskiStatus', (req, res) => {
    res.status(200).send(`Текущее количество помпушек на сервере: ${pompuski}`)
})





app.listen(PORT, HOST, () => {
  console.log(`Сервер запущен на http://${HOST}:${PORT}`);
});