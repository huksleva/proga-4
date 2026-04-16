# Отчёт по проекту: Budget Planner на WebAssembly

## Выполненное задание

### 1. Изучение проекта и принципов работы кода

#### Общее описание проекта

Проект представляет собой веб-приложение для отслеживания расходов (Budget Planner/Expense Tracker), использующее WebAssembly для выполнения вычислений. Приложение позволяет пользователям:

- Добавлять записи о расходах с указанием даты, категории, суммы и описания
- Просматривать все расходы в динамически обновляемой таблице
- Получать общую сумму расходов и разбивку по категориям
- Удалять отдельные записи или очищать все расходы

#### Архитектура приложения

Приложение состоит из трёх основных компонентов:

**1. Backend на C (main.c):**
- Реализует основную бизнес-логику приложения
- Определяет структуры данных:
  - `ExpenseEntry` - запись о расходе (дата, категория, сумма, описание)
  - `CategoryTotal` - общая сумма по категории
- Использует фиксированные массивы для хранения данных (MAX_EXPENSES = 100, MAX_CATEGORIES = 10)
- Экспортирует функции в JavaScript через Emscripten

**2. Frontend HTML (index.html):**
- Предоставляет пользовательский интерфейс
- Содержит форму для ввода расходов
- Отображает таблицу с расходами
- Показывает сводку по расходам и категориям

**3. JavaScript мост (app.js):**
- Связывает WebAssembly модуль с HTML интерфейсом
- Обрабатывает события пользовательского интерфейса
- Управляет выделением и освобождением памяти для строк
- Обновляет DOM на основе данных из WebAssembly модуля

#### Принцип работы

1. При загрузке страницы компилируется C код в WebAssembly
2. JavaScript инициализирует модуль и создаёт связи с C функциями
3. При добавлении расхода:
   - JavaScript валидирует данные формы
   - Выделяет память в WebAssembly для строк
   - Копирует строки в память WebAssembly
   - Вызывает C функцию `jsAddExpense`
   - C функция добавляет расход в массив и пересчитывает итоги
   - C код через `EM_ASM` вызывает JavaScript функции для обновления UI
   - JavaScript получает данные и обновляет таблицу

### 2. Установка компилятора Emscripten

#### Процесс установки

Для компиляции C кода в WebAssembly был использован компилятор Emscripten. Установка выполнялась согласно официальной документации:

```bash
# Клонирование репозитория emsdk
git clone https://github.com/emscripten-core/emsdk.git

# Переход в директорию
cd emsdk

# Установка и активация последней версии
emsdk install latest
emsdk activate latest

# Применение переменных окружения (в CMD)
emsdk_env.bat
```

#### Проверка установки

```bash
emcc --version
```

### 3. Компиляция и запуск приложения

#### Команда компиляции

```bash
emcc main.c -o index.js -s WASM=1 -O2 -s EXPORTED_RUNTIME_METHODS="[\"stringToUTF8\",\"UTF8ToString\"]" -s EXPORTED_FUNCTIONS="[\"_main\",\"_jsAddExpense\",\"_jsDeleteExpense\",\"_jsEditExpense\",\"_jsClearAllExpenses\",\"_jsGetTotalExpenses\",\"_jsGetExpenseCount\",\"_jsGetCategoryCount\",\"_getExpenseJSON\",\"_getCategoryTotalJSON\",\"_freeMemory\",\"_malloc\",\"_free\"]" --shell-file index.html -s ALLOW_MEMORY_GROWTH=1
```

#### Пояснение флагов компиляции:

- `-s WASM=1` - генерация WebAssembly модуля
- `-O2` - оптимизация кода
- `EXPORTED_RUNTIME_METHODS` - экспорт методов для работы со строками
- `EXPORTED_FUNCTIONS` - экспорт C функций для вызова из JavaScript
- `--shell-file index.html` - использование HTML шаблона
- `ALLOW_MEMORY_GROWTH=1` - разрешение динамического роста памяти

#### Запуск приложения

```bash
python -m http.server 8000
```

После запуска сервера приложение доступно по адресу: http://localhost:8000/

### 4. Предложенные улучшения проекта

На основе изучения исходного кода предлагаю следующие улучшения:

#### Улучшение 1: Добавление редактирования расходов

**Проблема:** В текущей версии нет возможности изменить существующую запись о расходе.

**Решение:** Добавить функцию `editExpense` в C код:

```c
/**
 * Function to edit an existing expense entry
 *
 * @param index The index of the expense to edit
 * @param date The new date
 * @param category The new category
 * @param amount The new amount
 * @param description The new description
 * @return 1 if successful, 0 if the index is invalid
 */
int EMSCRIPTEN_KEEPALIVE jsEditExpense(int index, const char* date, 
                                        const char* category, 
                                        double amount, 
                                        const char* description) {
    // Check if the index is valid
    if (index < 0 || index >= expenseCount) {
        return 0; // Failure - invalid index
    }
    
    // Update the expense data
    ExpenseEntry* expense = &expenses[index];
    strncpy(expense->date, date, MAX_STRING_LENGTH - 1);
    expense->date[MAX_STRING_LENGTH - 1] = '\0';
    
    strncpy(expense->category, category, MAX_STRING_LENGTH - 1);
    expense->category[MAX_STRING_LENGTH - 1] = '\0';
    
    expense->amount = amount;
    
    strncpy(expense->description, description, MAX_STRING_LENGTH - 1);
    expense->description[MAX_STRING_LENGTH - 1] = '\0';
    
    // Update category totals and UI
    updateCategoryTotals();
    updateUI();
    
    return 1; // Success
}
```

#### Улучшение 2: Экспорт данных в CSV формат

**Проблема:** Нет возможности экспортировать данные для использования в других приложениях.

**Решение:** Добавить функцию экспорта

**Реализация:**
- **C (main.c)**: Функция `exportToCSV()` формирует CSV строку с заголовками и данными, корректно экранируя специальные символы
- **JavaScript (app.js)**: Функция `handleExportToCSV()` получает данные из WebAssembly, создаёт Blob-объект и инициирует скачивание файла
- **HTML**: Добавлена кнопка "Export to CSV" в форму добавления расхода

**Особенности:**
- Добавлен UTF-8 BOM для корректного отображения кириллицы в Excel на Windows
- Автоматическое формирование имени файла с текущей датой (`expenses_YYYY-MM-DD.csv`)
- Корректное экранирование кавычек и запятых в описании

```c
/**
 * Function to export expenses as CSV format
 *
 * @return A pointer to a string containing CSV data
 */
char* EMSCRIPTEN_KEEPALIVE exportToCSV() {
    // Calculate required buffer size
    int bufferSize = MAX_EXPENSES * (MAX_STRING_LENGTH * 3 + 50);
    char* csv = (char*)malloc(bufferSize);
    if (csv == NULL) {
        return NULL;
    }
    
    // Add CSV header
    strcpy(csv, "Date,Category,Amount,Description\n");
    
    // Add each expense as a CSV row
    for (int i = 0; i < expenseCount; i++) {
        char line[MAX_STRING_LENGTH * 3 + 50];
        sprintf(line, "%s,%s,%.2f,\"%s\"\n",
                expenses[i].date,
                expenses[i].category,
                expenses[i].amount,
                expenses[i].description);
        strcat(csv, line);
    }
    
    return csv;
}
```


#### Улучшение 3: Валидация дат

**Проблема:** В текущей версии нет проверки корректности дат.

**Решение:** Добавить проверку в JavaScript (app.js):

**Реализация:**
- **JavaScript (app.js)**: Функция `validateDate()` проверяет корректность даты и запрещает будущие даты
- **Интеграция**: Проверка добавлена в `handleAddExpense()` перед отправкой данных в WebAssembly
- **Обратная связь**: Пользователь получает мгновенное сообщение об ошибке при вводе некорректной даты
- **Дополнительно**: Добавлена проверка при изменении поля даты (event 'change')

```javascript
function validateDate(dateString) {
    const date = new Date(dateString);
    const today = new Date();
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
        return false;
    }
    
    // Check if date is not in the future
    if (date > today) {
        return false;
    }
    
    return true;
}
```

#### Улучшение 4: Графическое отображение статистики

**Проблема:** Нет визуализации данных о расходах.

**Решение:** Добавить интеграцию с Chart.js для отображения диаграмм:

**Реализация:**
- **HTML**: 
  - Подключена библиотека Chart.js через CDN
  - Добавлен `<canvas id="expensesChart">` для отрисовки графика
  - Добавлен селектор типа диаграммы (Pie/Doughnut/Bar)
  - Добавлена кнопка "Refresh"
  
- **JavaScript (app.js)**:
  - Функция `drawExpensesChart(chartType)` получает данные из WebAssembly через `getCategoryTotalJSON()`
  - Автоматическое обновление графика при изменении данных (обёртывание `updateExpenseTable` и `updateCategoryTotals`)
  - Tooltip с отображением суммы и процента от общего бюджета
  - Корректное управление памятью WebAssembly (освобождение после использования)

**Особенности:**
- Поддержка трёх типов диаграмм (pie, doughnut, bar)
- Адаптивный дизайн (график масштабируется под размер экрана)
- Автоматическая перерисовка при добавлении/удалении/редактировании расходов
- Корректная обработка случая "нет данных" (очистка canvas вместо удаления элемента)

```javascript
function createCategoryChart() {
    const categoryCount = Module._jsGetCategoryCount();
    const labels = [];
    const data = [];
    
    for (let i = 0; i < categoryCount; i++) {
        const categoryJsonPtr = Module._getCategoryTotalJSON(i);
        const categoryJson = Module.UTF8ToString(categoryJsonPtr);
        const category = JSON.parse(categoryJson);
        
        labels.push(category.name);
        data.push(category.total);
        
        Module._freeMemory(categoryJsonPtr);
    }
    
    const ctx = document.getElementById('categoryChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', 
                    '#4BC0C0', '#9966FF', '#FF9F40'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Расходы по категориям'
                }
            }
        }
    });
}
```

### 5. Выводы

В ходе выполнения работы было достигнуто:

1. **Изучена архитектура WebAssembly приложений** - поняты принципы взаимодействия C кода, WebAssembly модуля и JavaScript интерфейса.

2. **Освоена работа с Emscripten** - изучен процесс компиляции C кода в WebAssembly, экспорт функций и работа с памятью.

3. **Поняты особенности межъязыкового взаимодействия**:
   - Передача строк между JavaScript и C требует ручного управления памятью
   - Использование `malloc`/`free` для выделения памяти в WebAssembly
   - Применение `stringToUTF8` и `UTF8ToString` для конвертации строк

4. **Изучены лучшие практики**:
   - Разделение логики приложения (C) и интерфейса (JavaScript/HTML)
   - Валидация данных на обоих уровнях
   - Обработка ошибок и информирование пользователя

5. **Предложены практические улучшения** проекта, которые могут быть реализованы для повышения функциональности приложения.

#### Практическая значимость

Проект демонстрирует реальные преимущества WebAssembly:
- **Производительность**: Вычисления выполняются на скорости, близкой к нативному коду
- **Безопасность**: WebAssembly работает в песочнице браузера
- **Портативность**: Один и тот же C код может работать на разных платформах
- **Интеграция**: Плавная интеграция с существующим JavaScript кодом

#### Перспективы развития

Проект может быть расширен за счёт:
- Добавления локального хранения данных (LocalStorage или IndexedDB)
- Реализации синхронизации с сервером
- Добавления поддержки нескольких валют
- Внедрения системы отчётов и аналитики
- Создания мобильного приложения на основе этой же кодовой базы

**Реализованные улучшения:**
- Редактирование записей — улучшен пользовательский опыт, снижено количество операций
- Валидация дат — предотвращение ввода ошибочных данных
- Экспорт в CSV — возможность сохранения и анализа данных в сторонних приложениях
- Графическая визуализация — наглядное представление статистики расходов

**Освоены технологии:**
- Интеграция библиотеки Chart.js с WebAssembly приложением
- Работа с Blob API для скачивания файлов
- Управление памятью WebAssembly (malloc/free)
- Обёртывание существующих функций для расширения функциональности

## 6. Тестирование реализованных улучшений

### Проверка редактирования расходов:
1. Добавить несколько расходов с разными категориями
2. Нажать кнопку "Edit" у любой записи
3. Форма заполняется данными записи
4. Кнопка меняет текст на "Save Changes"
5. Изменить сумму/описание
6. Нажать "Save Changes" — запись обновляется в таблице

### Проверка валидации дат:
1. Попробовать ввести будущую дату
2. Появляется сообщение: "Please enter a valid date (not in the future)"
3. Форма не отправляется

### Проверка экспорта в CSV:
1. Добавить несколько расходов
2. Нажать кнопку "Export to CSV"
3. Скачивается файл `expenses_YYYY-MM-DD.csv`
4. Открыть файл в Excel — данные отображаются корректно (включая кириллицу)

### Проверка графика:
1. Добавить 3-4 расхода с разными категориями
2. Появляется круговая диаграмма
3. Выбрать "Bar Chart" — отображается столбчатая диаграмма
4. Добавить новый расход — график автоматически обновляется
5. Tooltip показывает сумму и процент

