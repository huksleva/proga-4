# Budget Planner / Expense Tracker WebAssembly Application

## Project Overview

This project demonstrates how to build a complete web application using WebAssembly compiled from C. The Budget Planner application allows users to track their expenses by entering expense details, viewing them in a table, and seeing calculated totals by category.

### Features

- Add expense entries with date, category, amount, and description
- Display expenses in a dynamically updated table
- Calculate and show total expenses and totals by category
- Delete individual expense entries
- Clear all expense entries
- Responsive and user-friendly GUI

## Project Structure

The project consists of the following files:

- **main.c**: Core logic for the expense tracker implemented in C
- **index.html**: HTML structure for the user interface
- **app.js**: Custom JavaScript for DOM manipulation and event handling

## Technical Implementation

### Programming Language & Compilation

The application is built using C as the primary programming language and compiled to WebAssembly using Emscripten. The C code handles all data processing and calculations, while the HTML and JavaScript provide the user interface.

### Data Structures

The C code defines the following data structures:

- `ExpenseEntry`: Represents an individual expense with date, category, amount, and description
- `CategoryTotal`: Stores the total amount for each expense category

### Core Functionality

The C code implements the following functions:

- Add an expense entry
- Delete an expense entry by index
- Clear all expense entries
- Calculate total expenses
- Calculate totals by category

### WebAssembly Integration

The C code is compiled to WebAssembly using Emscripten, which generates JavaScript glue code to interface with the HTML UI. The application uses Emscripten's API to export C functions to JavaScript and to update the HTML UI when data changes.

## Compilation Instructions

To compile the project, you need to have Emscripten installed. Follow these steps:

1. Install Emscripten by following the instructions at [https://emscripten.org/docs/getting_started/downloads.html](https://emscripten.org/docs/getting_started/downloads.html)

2. Clone or download this project to your local machine

3. Navigate to the project directory in your terminal

4. Compile the C code to WebAssembly using the following command:

```bash
emcc main.c -o index.js -s WASM=1 -O2 -s EXPORTED_RUNTIME_METHODS='["stringToUTF8","UTF8ToString"]' -s EXPORTED_FUNCTIONS='["_main","_jsAddExpense","_jsDeleteExpense","_jsClearAllExpenses","_jsGetTotalExpenses","_jsGetExpenseCount","_jsGetCategoryCount","_getExpenseJSON","_getCategoryTotalJSON","_freeMemory","_malloc","_free"]' --shell-file index.html -s ALLOW_MEMORY_GROWTH=1
```

This command:
- Compiles `main.c` to WebAssembly
- Uses `index.html` as a template for the output HTML file
- Exports the necessary C functions to JavaScript
- Enables memory growth for dynamic memory allocation
- Optimizes the code with `-O2`

## Running the Application

To run the application, you need to serve the compiled files using a web server. You can use Python's built-in HTTP server:

```bash
python3 -m http.server 8000
```

Then open your web browser and navigate to `http://localhost:8000/` to use the application.

## Educational Value

This project demonstrates several important concepts:

- WebAssembly compilation from C using Emscripten
- Data structures and memory management in C
- Integration between C, WebAssembly, and JavaScript
- Dynamic UI updates based on data changes
- Form validation and error handling

Students will learn how to:
- Structure a WebAssembly project
- Define and manipulate data structures in C
- Export C functions to JavaScript
- Handle user input and update the UI
- Implement a practical application with real-world utility

## License

This project is provided for educational purposes and can be freely used and modified for academic purposes.
