/**
 * Flask Calculator - Client-side JavaScript
 * Handles calculator interactions and API calls
 */

class Calculator {
    constructor() {
        this.operand1 = null;
        this.operand2 = null;
        this.currentOperation = null;
        this.history = [];
        this.isOperand2Active = false;

        this.initializeElements();
        this.attachEventListeners();
        this.loadHistory();
    }

    /**
     * Initialize DOM elements
     */
    initializeElements() {
        this.operand1Input = document.getElementById('operand1');
        this.operand2Input = document.getElementById('operand2');
        this.resultDisplay = document.getElementById('result');
        this.operand2Section = document.querySelector('.operand2-section');
        this.errorMessage = document.getElementById('errorMessage');
        this.errorText = document.getElementById('errorText');
        this.clearBtn = document.getElementById('clearBtn');
        this.historyList = document.getElementById('historyList');
    }

    /**
     * Attach event listeners to buttons
     */
    attachEventListeners() {
        // Operation buttons
        const operationBtns = document.querySelectorAll('.btn-operation');
        operationBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const operation = e.target.closest('.btn-operation').dataset.operation;
                this.handleOperation(operation);
            });
        });

        // Clear button
        this.clearBtn.addEventListener('click', () => this.clear());

        // Enter key support
        this.operand1Input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && this.currentOperation) {
                this.operand2Input.focus();
            }
        });

        this.operand2Input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && this.currentOperation) {
                this.calculate();
            }
        });
    }

    /**
     * Handle operation button click
     * @param {string} operation - The operation to perform
     */
    async handleOperation(operation) {
        this.hideError();

        // Validate operand1
        if (!this.operand1Input.value.trim()) {
            this.showError('First operand required');
            return;
        }

        try {
            this.operand1 = parseFloat(this.operand1Input.value);
        } catch (e) {
            this.showError('Invalid first operand');
            return;
        }

        // For unary operations, calculate immediately
        if (['square', 'square_root'].includes(operation)) {
            this.currentOperation = operation;
            await this.calculate();
        } else {
            // For binary operations, show second operand input
            this.currentOperation = operation;
            this.isOperand2Active = true;
            this.operand2Section.classList.add('active');
            this.operand2Input.focus();
            this.operand2Input.value = '';
        }
    }

    /**
     * Calculate the result
     */
    async calculate() {
        if (!this.currentOperation) return;

        // Validate operand1
        if (!this.operand1Input.value.trim()) {
            this.showError('First operand required');
            return;
        }

        try {
            this.operand1 = parseFloat(this.operand1Input.value);
        } catch (e) {
            this.showError('Invalid first operand');
            return;
        }

        // For binary operations, validate operand2
        if (!['square', 'square_root'].includes(this.currentOperation)) {
            if (!this.operand2Input.value.trim()) {
                this.showError('Second operand required');
                return;
            }

            try {
                this.operand2 = parseFloat(this.operand2Input.value);
            } catch (e) {
                this.showError('Invalid second operand');
                return;
            }
        }

        // Prepare request payload
        const payload = {
            operation: this.currentOperation,
            operand1: this.operand1,
            operand2: this.operand2
        };

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (data.success) {
                this.resultDisplay.value = data.result;
                this.addToHistory(this.operand1, this.currentOperation, this.operand2, data.result);
                this.operand1Input.value = data.result;
                this.operand2Input.value = '';
                this.isOperand2Active = false;
                this.operand2Section.classList.remove('active');
                this.currentOperation = null;
            } else {
                this.showError(data.error || 'Calculation error');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        }
    }

    /**
     * Add calculation to history
     * @param {number} op1 - First operand
     * @param {string} operation - Operation name
     * @param {number} op2 - Second operand (optional)
     * @param {number} result - Result
     */
    addToHistory(op1, operation, op2, result) {
        const operationSymbol = this.getOperationSymbol(operation);
        let historyEntry;

        if (op2 !== undefined && op2 !== null) {
            historyEntry = `${op1} ${operationSymbol} ${op2} = ${result}`;
        } else {
            historyEntry = `${operationSymbol}(${op1}) = ${result}`;
        }

        this.history.unshift(historyEntry);
        if (this.history.length > 10) {
            this.history.pop();
        }

        this.saveHistory();
        this.renderHistory();
    }

    /**
     * Get operation symbol
     * @param {string} operation - Operation name
     * @returns {string} - Symbol
     */
    getOperationSymbol(operation) {
        const symbols = {
            'add': '+',
            'subtract': '−',
            'multiply': '×',
            'divide': '÷',
            'square': 'x²',
            'square_root': '√'
        };
        return symbols[operation] || operation;
    }

    /**
     * Render history list
     */
    renderHistory() {
        this.historyList.innerHTML = '';
        this.history.forEach(entry => {
            const li = document.createElement('li');
            li.textContent = entry;
            this.historyList.appendChild(li);
        });
    }

    /**
     * Save history to localStorage
     */
    saveHistory() {
        try {
            localStorage.setItem('calculatorHistory', JSON.stringify(this.history));
        } catch (e) {
            console.warn('Could not save history to localStorage:', e);
        }
    }

    /**
     * Load history from localStorage
     */
    loadHistory() {
        try {
            const saved = localStorage.getItem('calculatorHistory');
            if (saved) {
                this.history = JSON.parse(saved);
                this.renderHistory();
            }
        } catch (e) {
            console.warn('Could not load history from localStorage:', e);
        }
    }

    /**
     * Show error message
     * @param {string} message - Error message
     */
    showError(message) {
        this.errorText.textContent = message;
        this.errorMessage.classList.add('active');
        this.errorMessage.style.display = 'block';
    }

    /**
     * Hide error message
     */
    hideError() {
        this.errorMessage.classList.remove('active');
        this.errorMessage.style.display = 'none';
    }

    /**
     * Clear all inputs and state
     */
    clear() {
        this.operand1Input.value = '';
        this.operand2Input.value = '';
        this.resultDisplay.value = '';
        this.operand1 = null;
        this.operand2 = null;
        this.currentOperation = null;
        this.isOperand2Active = false;
        this.operand2Section.classList.remove('active');
        this.hideError();
        this.operand1Input.focus();
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.calculator = new Calculator();
});
