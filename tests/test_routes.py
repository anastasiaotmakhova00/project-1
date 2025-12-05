"""
Integration Tests for Flask Routes
===================================
Интеграционные тесты для API маршрутов приложения.
Тестируют взаимодействие контроллеров и Service Layer.
"""
import pytest
import json


class TestCalculatorRoutes:
    """Тесты для маршрутов калькулятора."""

    def test_index_page_loads(self, client):
        """Главная страница загружается успешно."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Calculator' in response.data

    def test_index_page_contains_form(self, client):
        """Главная страница содержит форму калькулятора."""
        response = client.get('/')
        assert b'operand1' in response.data
        assert b'result' in response.data

    def test_health_check_endpoint(self, client):
        """Endpoint здоровья приложения возвращает корректный статус."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

    def test_404_error_handling(self, client):
        """Несуществующий маршрут возвращает 404."""
        response = client.get('/nonexistent')
        assert response.status_code == 404


class TestCalculatorAPIBinaryOperations:
    """Тесты для API операций калькулятора."""

    def test_addition_api(self, client):
        """API сложения работает корректно."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'add',
                'operand1': 2,
                'operand2': 3
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == 5

    def test_subtraction_api(self, client):
        """API вычитания работает корректно."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'subtract',
                'operand1': 10,
                'operand2': 3
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == 7

    def test_multiplication_api(self, client):
        """API умножения работает корректно."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'multiply',
                'operand1': 4,
                'operand2': 5
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == 20

    def test_division_api(self, client):
        """API деления работает корректно."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'divide',
                'operand1': 10,
                'operand2': 2
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == 5

    def test_division_by_zero_api(self, client):
        """API деления на ноль возвращает ошибку."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'divide',
                'operand1': 10,
                'operand2': 0
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Division by zero' in data['error']


class TestCalculatorAPIUnaryOperations:
    """Тесты для унарных операций API."""

    def test_square_api(self, client):
        """API возведения в квадрат работает корректно."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'square',
                'operand1': 5
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == 25

    def test_square_root_api(self, client):
        """API извлечения корня работает корректно."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'square_root',
                'operand1': 16
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == 4

    def test_square_root_negative_api(self, client):
        """API корня из отрицательного числа возвращает ошибку."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'square_root',
                'operand1': -4
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'negative' in data['error'].lower()


class TestCalculatorAPIErrorHandling:
    """Тесты обработки ошибок в API."""

    def test_invalid_operation(self, client):
        """API с невалидной операцией возвращает ошибку."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'invalid_op',
                'operand1': 5,
                'operand2': 3
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_missing_operand1(self, client):
        """API без первого операнда возвращает ошибку."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'add',
                'operand2': 3
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_missing_operand2_for_binary_op(self, client):
        """API без второго операнда для бинарной операции возвращает ошибку."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'add',
                'operand1': 5
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_invalid_operand1(self, client):
        """API с невалидным первым операндом возвращает ошибку."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'add',
                'operand1': 'not_a_number',
                'operand2': 3
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_invalid_operand2(self, client):
        """API с невалидным вторым операндом возвращает ошибку."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'add',
                'operand1': 5,
                'operand2': 'not_a_number'
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_invalid_json_format(self, client):
        """API с невалидным JSON возвращает ошибку."""
        response = client.post(
            '/api/calculate',
            data='invalid json',
            content_type='application/json'
        )
        assert response.status_code == 400 or response.status_code == 500

    def test_empty_json_body(self, client):
        """API с пустым JSON телом возвращает ошибку."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False


class TestCalculatorAPIFloatOperations:
    """Тесты для операций с числами с плавающей точкой."""

    def test_float_addition(self, client):
        """API сложения чисел с плавающей точкой."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'add',
                'operand1': 1.5,
                'operand2': 2.5
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == pytest.approx(4.0)

    def test_float_division(self, client):
        """API деления чисел с плавающей точкой."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'divide',
                'operand1': 7.5,
                'operand2': 2.5
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == pytest.approx(3.0)

    def test_negative_operands(self, client):
        """API с отрицательными операндами."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'multiply',
                'operand1': -3,
                'operand2': -4
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == 12


class TestCalculatorAPIComplexOperations:
    """Тесты для сложных операций и последовательностей."""

    def test_string_operands_valid_format(self, client):
        """API принимает строковые операнды в валидном формате."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'add',
                'operand1': '5',
                'operand2': '3'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['result'] == 8

    def test_response_structure(self, client):
        """API возвращает правильную структуру ответа."""
        response = client.post(
            '/api/calculate',
            data=json.dumps({
                'operation': 'add',
                'operand1': 5,
                'operand2': 3
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert 'success' in data
        assert 'result' in data
        assert 'error' in data
