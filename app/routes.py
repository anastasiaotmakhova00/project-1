"""
Routes/Controller Module
=======================
Маршруты приложения, обработка HTTP запросов и представления (Views).
Отделены от бизнес-логики, которая находится в Service Layer.
"""
from flask import render_template, request, jsonify
from flask_babel import gettext

from .service import (
    CalculatorService,
    CalculatorError,
    DivisionByZeroError,
    InvalidInputError,
)


def register_routes(app):
    """
    Регистрирует все маршруты приложения.
    
    Args:
        app: Flask приложение
    """

    @app.route('/')
    def index():
        """Главная страница с интерфейсом калькулятора."""
        return render_template('index.html')

    @app.route('/api/calculate', methods=['POST'])
    def calculate():
        """
        API endpoint для выполнения операции калькулятора.
        
        Принимает JSON:
        {
            "operation": "add|subtract|multiply|divide|square|square_root",
            "operand1": number,
            "operand2": number (опционально для unary операций)
        }
        
        Возвращает JSON:
        {
            "success": bool,
            "result": number или null,
            "error": string или null
        }
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'result': None,
                    'error': gettext('Invalid request format')
                }), 400
            
            operation = data.get('operation')
            
            # Validate operation
            valid_operations = [
                'add', 'subtract', 'multiply', 'divide', 'square', 'square_root'
            ]
            if operation not in valid_operations:
                return jsonify({
                    'success': False,
                    'result': None,
                    'error': gettext('Invalid operation')
                }), 400
            
            # Validate operands
            try:
                operand1 = CalculatorService.validate_number(data.get('operand1'))
            except InvalidInputError:
                return jsonify({
                    'success': False,
                    'result': None,
                    'error': gettext('Invalid first operand')
                }), 400
            
            # For binary operations
            if operation in ['add', 'subtract', 'multiply', 'divide']:
                try:
                    operand2 = CalculatorService.validate_number(data.get('operand2'))
                except InvalidInputError:
                    return jsonify({
                        'success': False,
                        'result': None,
                        'error': gettext('Invalid second operand')
                    }), 400
                
                # Perform operation
                try:
                    if operation == 'add':
                        result = CalculatorService.add(operand1, operand2)
                    elif operation == 'subtract':
                        result = CalculatorService.subtract(operand1, operand2)
                    elif operation == 'multiply':
                        result = CalculatorService.multiply(operand1, operand2)
                    elif operation == 'divide':
                        result = CalculatorService.divide(operand1, operand2)
                except DivisionByZeroError:
                    return jsonify({
                        'success': False,
                        'result': None,
                        'error': gettext('Division by zero is not allowed')
                    }), 400
            
            # For unary operations
            elif operation in ['square', 'square_root']:
                try:
                    if operation == 'square':
                        result = CalculatorService.square(operand1)
                    elif operation == 'square_root':
                        result = CalculatorService.square_root(operand1)
                except (DivisionByZeroError, InvalidInputError) as e:
                    error_msg = str(e)
                    if 'negative' in error_msg.lower():
                        error_msg = gettext('Cannot calculate square root of negative number')
                    return jsonify({
                        'success': False,
                        'result': None,
                        'error': error_msg
                    }), 400
            
            # Return successful result
            return jsonify({
                'success': True,
                'result': round(result, 10),  # Округление для избежания ошибок float
                'error': None
            }), 200
        
        except Exception as e:
            # Unexpected error
            return jsonify({
                'success': False,
                'result': None,
                'error': gettext('An unexpected error occurred')
            }), 500

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint для мониторинга приложения."""
        return jsonify({
            'status': 'healthy',
            'service': 'Calculator API'
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        """Обработчик ошибки 404."""
        return jsonify({
            'success': False,
            'error': gettext('Resource not found')
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        """Обработчик ошибки 500."""
        return jsonify({
            'success': False,
            'error': gettext('Internal server error')
        }), 500
