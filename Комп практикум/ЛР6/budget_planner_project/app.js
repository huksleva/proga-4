/**
 * app.js - Custom JavaScript for Budget Planner WebAssembly Application
 * 
 * This file contains the JavaScript code that connects the WebAssembly module
 * with the HTML user interface. It handles UI events, calls exported C functions,
 * and updates the DOM based on the data from the WebAssembly module.
 * 
 * Author: University Professor
 * For: Computer Practicum Course - 2nd Year IT Bachelor Students
 * Date: March 2025
 */

// Wait for the DOM to be fully loaded before initializing the application
document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const expenseForm = document.getElementById('expenseForm');
    const expenseDate = document.getElementById('expenseDate');
    const expenseCategory = document.getElementById('expenseCategory');
    const expenseAmount = document.getElementById('expenseAmount');
    const expenseDescription = document.getElementById('expenseDescription');
    const addExpenseBtn = document.getElementById('addExpenseBtn');
    const clearAllBtn = document.getElementById('clearAllBtn');
    const expenseTableBody = document.getElementById('expenseTableBody');
    const noExpensesRow = document.getElementById('noExpensesRow');
    const totalExpensesElement = document.getElementById('totalExpenses');
    const categoryTotalsElement = document.getElementById('categoryTotals');
    const noCategoriesMessage = document.getElementById('noCategoriesMessage');
    const messageArea = document.getElementById('messageArea');
	
	// Export button reference
	const exportCsvBtn = document.getElementById('exportCsvBtn');
    
    // Set the default date to today
    const today = new Date();
    const formattedDate = today.toISOString().substr(0, 10); // Format: YYYY-MM-DD
    expenseDate.value = formattedDate;
	
	// Chart instance for expenses visualization
	let expensesChart = null;
	
	/**
	 * Function to handle editing an expense
	 *
	 * @param {number} index - The index of the expense to edit
	 */
	function handleEditExpense(index) {
    console.log('📝 Editing expense at index:', index);
    
    // Get the expense data from WebAssembly
    const expenseJsonPtr = Module._getExpenseJSON(index);
    if (expenseJsonPtr === 0) {
        showMessage('Failed to load expense data', 'error');
        return;
    }
    
    // Convert JSON to JavaScript object
    const expenseJson = Module.UTF8ToString(expenseJsonPtr);
    const expense = JSON.parse(expenseJson);
    Module._freeMemory(expenseJsonPtr);
    
    // Fill the form with expense data
    expenseDate.value = expense.date;
    expenseCategory.value = expense.category;
    expenseAmount.value = expense.amount;
    expenseDescription.value = expense.description;
    
    // Store the index of the expense being edited
    expenseForm.dataset.editIndex = index;
    
    // Change the button text
    addExpenseBtn.textContent = '💾 Save Changes';
    
    // Scroll to the form
    expenseForm.scrollIntoView({ behavior: 'smooth' });
    showMessage('Editing expense. Change values and click "Save Changes"', 'success');
}
	
    /**
     * Function to display a message to the user
     * 
     * @param {string} message - The message to display
     * @param {string} type - The type of message ('error' or 'success')
     */
    function showMessage(message, type) {
        messageArea.textContent = message;
        messageArea.className = type === 'error' ? 'error-message' : 'success-message';
        messageArea.classList.remove('hidden');
        
        // Hide the message after 3 seconds
        setTimeout(function() {
            messageArea.classList.add('hidden');
        }, 3000);
    }
    
    /**
     * Function to format a number as currency
     * 
     * @param {number} amount - The amount to format
     * @return {string} The formatted amount
     */
    function formatCurrency(amount) {
        return '$' + amount.toFixed(2);
    }
	
	/**
	 * Function to validate a date string
	 * 
	 * @param {string} dateString - The date string to validate (format: YYYY-MM-DD)
	 * @return {boolean} True if the date is valid and not in the future, false otherwise
	 */
	function validateDate(dateString) {
		const date = new Date(dateString);
		const today = new Date();
		
		// Reset time components for accurate date-only comparison
		today.setHours(0, 0, 0, 0);
		date.setHours(0, 0, 0, 0);
		
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
    
    /**
     * Function to handle the form submission for adding a new expense
     * 
     * @param {Event} event - The form submission event
     */
    function handleAddExpense(event) {
        // Prevent the default form submission
        event.preventDefault();
        
        // Get the form values
        const date = expenseDate.value;
        const category = expenseCategory.value;
        const amountStr = expenseAmount.value;
        const description = expenseDescription.value;
        
		// === НОВАЯ ПРОВЕРКА: Валидация даты ===
		if (!validateDate(date)) {
			showMessage('Please enter a valid date (not in the future)', 'error');
			expenseDate.focus();
			return;
		}
		// ============================================
		
        // Validate the input
        if (!date || !category || !amountStr || !description) {
            showMessage('Please fill in all fields', 'error');
            return;
        }
        
        // Parse the amount as a float
        const amount = parseFloat(amountStr);
        
        // Validate the amount
        if (isNaN(amount) || amount <= 0) {
            showMessage('Please enter a valid positive amount', 'error');
            return;
        }
        
		// === НОВЫЙ БЛОК: Проверка режима редактирования ===
		const editIndex = expenseForm.dataset.editIndex;
		
		if (editIndex !== undefined && editIndex !== '') {
			// EDIT MODE: Update existing expense
			const datePtr = Module._malloc(date.length + 1);
			const categoryPtr = Module._malloc(category.length + 1);
			const descriptionPtr = Module._malloc(description.length + 1);
			
			Module.stringToUTF8(date, datePtr, date.length + 1);
			Module.stringToUTF8(category, categoryPtr, category.length + 1);
			Module.stringToUTF8(description, descriptionPtr, description.length + 1);
			
			// Call the WebAssembly function to edit expense
			const result = Module._jsEditExpense(
				parseInt(editIndex),
				datePtr,
				categoryPtr,
				amount,
				descriptionPtr
			);
			
			Module._free(datePtr);
			Module._free(categoryPtr);
			Module._free(descriptionPtr);
			
			if (result === 1) {
				showMessage('Expense updated successfully', 'success');
				// Clear edit mode
				delete expenseForm.dataset.editIndex;
				addExpenseBtn.textContent = 'Add Expense';
			} else {
				showMessage('Failed to update expense', 'error');
			}
			
			// Reset form
			expenseCategory.value = '';
			expenseAmount.value = '';
			expenseDescription.value = '';
			expenseCategory.focus();
			return; // Важно: выходим из функции после редактирования!
		}
		// === КОНЕЦ НОВОГО БЛОКА ===
		
		
        // Call the WebAssembly function to add the expense
        // We need to allocate memory for the strings in the WebAssembly module
        const datePtr = Module._malloc(date.length + 1);
        const categoryPtr = Module._malloc(category.length + 1);
        const descriptionPtr = Module._malloc(description.length + 1);
        
        // Write the strings to the allocated memory
        Module.stringToUTF8(date, datePtr, date.length + 1);
        Module.stringToUTF8(category, categoryPtr, category.length + 1);
        Module.stringToUTF8(description, descriptionPtr, description.length + 1);
        
        // Call the WebAssembly function
        const result = Module._jsAddExpense(datePtr, categoryPtr, amount, descriptionPtr);
        
        // Free the allocated memory
        Module._free(datePtr);
        Module._free(categoryPtr);
        Module._free(descriptionPtr);
        
        // Check the result
        if (result === 1) {
            // Success
            showMessage('Expense added successfully', 'success');
            
            // Reset the form (except the date)
            expenseCategory.value = '';
            expenseAmount.value = '';
            expenseDescription.value = '';
            
            // Focus on the category field for the next entry
            expenseCategory.focus();
        } else {
            // Failure
            showMessage('Failed to add expense. Maximum number of expenses reached.', 'error');
        }
    }
    
    /**
     * Function to handle deleting an expense
     * 
     * @param {number} index - The index of the expense to delete
     */
    function handleDeleteExpense(index) {
        // Call the WebAssembly function to delete the expense
        const result = Module._jsDeleteExpense(index);
        
        // Check the result
        if (result === 1) {
            // Success
            showMessage('Expense deleted successfully', 'success');
        } else {
            // Failure
            showMessage('Failed to delete expense. Invalid index.', 'error');
        }
    }
    
    /**
     * Function to handle clearing all expenses
     */
    function handleClearAllExpenses() {
        // Ask for confirmation
        if (confirm('Are you sure you want to clear all expenses? This action cannot be undone.')) {
            // Call the WebAssembly function to clear all expenses
            const result = Module._jsClearAllExpenses();
            
            // Check the result
            if (result === 1) {
                // Success
                showMessage('All expenses cleared successfully', 'success');
            } else {
                // Failure
                showMessage('Failed to clear expenses', 'error');
            }
        }
    }
    
	/**
	 * Function to draw the expenses chart using Chart.js
	 * @param {string} chartType - Type of chart: 'pie', 'doughnut', or 'bar'
	 */
	function drawExpensesChart(chartType = 'pie') {
		const canvas = document.getElementById('expensesChart');
		
		// Если canvas не найден (например, из-за прошлой ошибки), выходим
		if (!canvas) {
			console.error('Canvas element not found. Please reload the page (Ctrl+F5).');
			return;
		}

		const ctx = canvas.getContext('2d');
		const categoryCount = Module._jsGetCategoryCount();
		
		// Уничтожаем предыдущий экземпляр графика, если он был
		if (expensesChart) {
			expensesChart.destroy();
		}
		
		// === ИСПРАВЛЕНИЕ: НЕ УДАЛЯЕМ CANVAS, ЕСЛИ НЕТ ДАННЫХ ===
		if (categoryCount === 0) {
			// Просто очищаем canvas, чтобы на нем не оставалось старых рисунков
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			return; // Выходим из функции, не рисуя пустой график
		}
		// ======================================================
		
		// Prepare data arrays
		const labels = [];
		const data = [];
		const backgroundColors = [
			'#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
			'#FF9F40', '#C9CBCF', '#2ECC71', '#E74C3C', '#3498DB'
		];
		
		// Get category data from WebAssembly
		for (let i = 0; i < categoryCount; i++) {
			const categoryJsonPtr = Module._getCategoryTotalJSON(i);
			if (categoryJsonPtr === 0) continue;
			
			const categoryJson = Module.UTF8ToString(categoryJsonPtr);
			const category = JSON.parse(categoryJson);
			Module._freeMemory(categoryJsonPtr);
			
			labels.push(category.name);
			data.push(parseFloat(category.total.toFixed(2)));
		}
		
		// Create the chart
		expensesChart = new Chart(ctx, {
			type: chartType,
			data: {
				labels: labels,
				datasets: [{
					label: 'Expenses ($)',
					 data,
					backgroundColor: backgroundColors.slice(0, labels.length),
					borderColor: backgroundColors.slice(0, labels.length).map(color => color.replace('0.9', '1')),
					borderWidth: 1
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: {
						position: chartType === 'bar' ? 'top' : 'right',
					},
					title: {
						display: true,
						text: 'Expenses by Category'
					},
					tooltip: {
						callbacks: {
							label: function(context) {
								const label = context.label || '';
								const value = context.parsed || 0;
								const total = context.dataset.data.reduce((a, b) => a + b, 0);
								const percentage = ((value / total) * 100).toFixed(1);
								return `${label}: $${value.toFixed(2)} (${percentage}%)`;
							}
						}
					}
				}
			}
		});
	}
	
	/**
	 * Function to handle CSV export
	 * Downloads the expenses as a CSV file
	 */
	function handleExportToCSV() {
		console.log('Exporting expenses to CSV...');
		
		// Call the WebAssembly function to get CSV data
		const csvPtr = Module._exportToCSV();
		if (csvPtr === 0) {
			showMessage('Failed to export data', 'error');
			return;
		}
		
		// Convert C string to JavaScript string
		const csv = Module.UTF8ToString(csvPtr);
		
		// Free the memory allocated by C
		Module._freeMemory(csvPtr);
		
		// Check if we have data to export
		if (csv.trim().split('\n').length <= 1) {
			showMessage('No expenses to export', 'error');
			return;
		}
		
		// Create a Blob with the CSV data
		const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
		
		// Create a download link
		const link = document.createElement('a');
		const url = URL.createObjectURL(blob);
		
		// Generate filename with current date
		const now = new Date();
		const filename = `expenses_${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}.csv`;
		
		// Configure and trigger the download
		link.setAttribute('href', url);
		link.setAttribute('download', filename);
		link.style.visibility = 'hidden';
		
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		
		// Clean up
		URL.revokeObjectURL(url);
		
		showMessage('Expenses exported successfully!', 'success');
	}
	
    /**
     * Function to update the expense table with data from the WebAssembly module
     * This function is called from the C code when the expense data changes
     */
    window.updateExpenseTable = function() {
        // Get the number of expenses
        const expenseCount = Module._jsGetExpenseCount();
        
        // Clear the table body
        expenseTableBody.innerHTML = '';
        
        // Check if there are any expenses
        if (expenseCount === 0) {
            // No expenses, show the "No expenses" row
            expenseTableBody.appendChild(noExpensesRow);
            return;
        }
        
        // Loop through all expenses and add them to the table
        for (let i = 0; i < expenseCount; i++) {
            // Get the expense data as JSON
            const expenseJsonPtr = Module._getExpenseJSON(i);
            if (expenseJsonPtr === 0) {
                continue; // Skip invalid expenses
            }
            
            // Convert the JSON string to a JavaScript object
            const expenseJson = Module.UTF8ToString(expenseJsonPtr);
            const expense = JSON.parse(expenseJson);
            
            // Free the memory allocated for the JSON string
            Module._freeMemory(expenseJsonPtr);
            
            // Create a new row for the expense
            const row = document.createElement('tr');
            
            // Add cells for each expense property
            const dateCell = document.createElement('td');
            dateCell.textContent = expense.date;
            row.appendChild(dateCell);
            
            const categoryCell = document.createElement('td');
            categoryCell.textContent = expense.category;
            row.appendChild(categoryCell);
            
            const amountCell = document.createElement('td');
            amountCell.textContent = formatCurrency(expense.amount);
            row.appendChild(amountCell);
            
            const descriptionCell = document.createElement('td');
            descriptionCell.textContent = expense.description;
            row.appendChild(descriptionCell);
            
			// Add an edit button
			const actionCell = document.createElement('td');
			const editButton = document.createElement('button');
			editButton.textContent = 'Edit';
			editButton.className = 'edit';
			editButton.onclick = function() {
				handleEditExpense(i);
			};
			actionCell.appendChild(editButton);
			
            // Add a delete button
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.className = 'delete';
            deleteButton.onclick = function() {
                handleDeleteExpense(i);
            };
            actionCell.appendChild(deleteButton);
            row.appendChild(actionCell);
            
            // Add the row to the table
            expenseTableBody.appendChild(row);
        }
    };
    
    /**
     * Function to update the total expenses display
     * This function is called from the C code when the expense data changes
     * 
     * @param {number} total - The total amount of all expenses
     */
    window.updateTotalExpenses = function(total) {
        totalExpensesElement.textContent = formatCurrency(total);
    };
    
    /**
     * Function to update the category totals display
     * This function is called from the C code when the expense data changes
     */
    window.updateCategoryTotals = function() {
        // Get the number of categories
        const categoryCount = Module._jsGetCategoryCount();
        
        // Clear the category totals
        categoryTotalsElement.innerHTML = '';
        
        // Check if there are any categories
        if (categoryCount === 0) {
            // No categories, show the "No categories" message
            categoryTotalsElement.appendChild(noCategoriesMessage);
            return;
        }
        
        // Loop through all categories and add them to the display
        for (let i = 0; i < categoryCount; i++) {
            // Get the category total data as JSON
            const categoryJsonPtr = Module._getCategoryTotalJSON(i);
            if (categoryJsonPtr === 0) {
                continue; // Skip invalid categories
            }
            
            // Convert the JSON string to a JavaScript object
            const categoryJson = Module.UTF8ToString(categoryJsonPtr);
            const category = JSON.parse(categoryJson);
            
            // Free the memory allocated for the JSON string
            Module._freeMemory(categoryJsonPtr);
            
            // Create a new element for the category total
            const categoryElement = document.createElement('div');
            categoryElement.className = 'category-total-item';
            categoryElement.textContent = `${category.name}: ${formatCurrency(category.total)}`;
            
            // Add the element to the category totals
            categoryTotalsElement.appendChild(categoryElement);
        }
    };
    
    // Add event listeners
    expenseForm.addEventListener('submit', handleAddExpense);
    clearAllBtn.addEventListener('click', handleClearAllExpenses);
	
	// Validate date when user changes it
	expenseDate.addEventListener('change', function() {
		if (this.value && !validateDate(this.value)) {
			showMessage('Warning: Date cannot be in the future', 'error');
		}
	});
	
	// Export button event listener
	if (exportCsvBtn) {
		exportCsvBtn.addEventListener('click', handleExportToCSV);
	}
	
	// Chart event listeners
	const chartTypeSelect = document.getElementById('chartType');
	const refreshChartBtn = document.getElementById('refreshChartBtn');

	if (chartTypeSelect) {
		chartTypeSelect.addEventListener('change', function() {
			drawExpensesChart(this.value);
		});
	}

	if (refreshChartBtn) {
		refreshChartBtn.addEventListener('click', function() {
			drawExpensesChart(chartTypeSelect ? chartTypeSelect.value : 'pie');
			showMessage('Chart refreshed', 'success');
		});
	}

	// Auto-update chart when expense data changes
	// Store original functions to wrap them
	const originalUpdateExpenseTable = window.updateExpenseTable;
	const originalUpdateCategoryTotals = window.updateCategoryTotals;

	window.updateExpenseTable = function() {
		originalUpdateExpenseTable();
		// Redraw chart after table update
		if (document.getElementById('expensesChart')) {
			drawExpensesChart(chartTypeSelect ? chartTypeSelect.value : 'pie');
		}
	};

	window.updateCategoryTotals = function() {
		originalUpdateCategoryTotals();
		// Redraw chart after category totals update
		if (document.getElementById('expensesChart')) {
			drawExpensesChart(chartTypeSelect ? chartTypeSelect.value : 'pie');
		}
	};

	// Initialize chart on first load
	if (document.getElementById('expensesChart')) {
		// Small delay to ensure DOM is ready
		setTimeout(() => {
			drawExpensesChart('pie');
		}, 100);
	}
});
