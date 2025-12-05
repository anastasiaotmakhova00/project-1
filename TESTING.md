# Testing Guide - Flask Calculator

## 📋 Таблица Содержимого

1. [Начало с Тестами](#начало-с-тестами)
2. [Структура Тестов](#структура-тестов)
3. [Запуск Тестов](#запуск-тестов)
4. [Примеры Тестов](#примеры-тестов)
5. [Best Practices](#best-practices)

---

## 🚀 Начало с Тестами

### Установка Dependencies

```bash
pip install -r requirements.txt
```

### Запуск Всех Тестов

```bash
pytest
```

### Проверка Покрытия

```bash
pytest --cov=app tests/ --cov-report=html
```

---

## 📐 Структура Тестов

### Unit Tests - Service Layer
**Файл**: `tests/test_calculator_service.py`
**Назначение**: Тестирование бизнес-логики независимо от Flask
**Количество**: 40 тестов

```
TestCalculatorServiceAddition (5 тестов)
├── test_add_positive_numbers
├── test_add_negative_numbers
├── test_add_positive_and_negative
├── test_add_zeros
└── test_add_floats

TestCalculatorServiceSubtraction (5 тестов)
├── test_subtract_positive_numbers
├── test_subtract_negative_numbers
├── test_subtract_resulting_in_negative
├── test_subtract_from_zero
└── test_subtract_floats

TestCalculatorServiceMultiplication (5 тестов)
TestCalculatorServiceDivision (7 тестов)
TestCalculatorServiceSquare (5 тестов)
TestCalculatorServiceSquareRoot (6 тестов)
TestCalculatorServiceValidation (8 тестов)
TestCalculatorServiceEdgeCases (3 теста)
```

### Integration Tests - API Routes
**Файл**: `tests/test_routes.py`
**Назначение**: Тестирование HTTP API endpoints
**Количество**: 28 тестов

```
TestCalculatorRoutes (4 теста)
├── test_index_page_loads
├── test_index_page_contains_form
├── test_health_check_endpoint
└── test_404_error_handling

TestCalculatorAPIBinaryOperations (5 тестов)
├── test_addition_api
├── test_subtraction_api
├── test_multiplication_api
├── test_division_api
└── test_division_by_zero_api

TestCalculatorAPIUnaryOperations (3 теста)
TestCalculatorAPIErrorHandling (7 тестов)
TestCalculatorAPIFloatOperations (3 теста)
TestCalculatorAPIComplexOperations (2 теста)
```

---

## 🧪 Запуск Тестов

### Все Тесты
```bash
pytest
# или с подробным выводом
pytest -v
```

### Только Unit Тесты
```bash
pytest tests/test_calculator_service.py -v
```

### Только Integration Тесты
```bash
pytest tests/test_routes.py -v
```

### Специфичный Тест
```bash
pytest tests/test_calculator_service.py::TestCalculatorServiceAddition::test_add_positive_numbers -v
```

### Тесты с Сигнатурой
```bash
pytest -k "addition" -v    # Все тесты с "addition" в имени
pytest -k "api" -v         # Все API тесты
pytest -k "error" -v       # Все тесты ошибок
```

### С Покрытием Кода
```bash
# Покрытие в терминале
pytest --cov=app tests/ -v

# Подробный отчет
pytest --cov=app tests/ --cov-report=term-missing

# HTML отчет
pytest --cov=app tests/ --cov-report=html
open htmlcov/index.html
```

### Раскрасить Вывод
```bash
pytest -v --tb=short
# или
pytest -v --tb=long
```

### Остановить на первой Ошибке
```bash
pytest -x
```

### Показать Ошибки и Warnings
```bash
pytest -v -W error
```

---

## 📚 Примеры Тестов

### 1. Unit Test - Простая Операция

```python
def test_add_positive_numbers(self):
    """Сложение двух положительных чисел."""
    result = CalculatorService.add(2, 3)
    assert result == 5
    assert isinstance(result, float)
```

**Что тестируется:**
- ✓ Правильность вычисления
- ✓ Тип результата (float)

### 2. Unit Test - Обработка Исключений

```python
def test_divide_by_zero_raises_error(self):
    """Деление на ноль вызывает исключение."""
    with pytest.raises(DivisionByZeroError):
        CalculatorService.divide(10, 0)
```

**Что тестируется:**
- ✓ Правильное исключение выбрасывается
- ✓ Обработка ошибок работает корректно

### 3. Unit Test - Граничные Случаи

```python
def test_divide_with_remainder(self):
    """Деление с остатком."""
    result = CalculatorService.divide(7, 2)
    assert result == pytest.approx(3.5)
```

**Что тестируется:**
- ✓ Точность с float числами
- ✓ Использование `pytest.approx` для сравнения

### 4. Integration Test - API Success

```python
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
```

**Что тестируется:**
- ✓ HTTP status code (200)
- ✓ JSON parsing
- ✓ Успешный результат
- ✓ Правильность вычисления через API

### 5. Integration Test - API Error Handling

```python
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
```

**Что тестируется:**
- ✓ HTTP error status (400)
- ✓ Обработка ошибок в API
- ✓ Правильное сообщение об ошибке

### 6. Integration Test - Input Validation

```python
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
```

**Что тестируется:**
- ✓ Валидация входных данных
- ✓ Обработка невалидного ввода
- ✓ Правильный HTTP status

---

## ✅ Best Practices в Тестировании

### 1. **Используйте Descriptive Names**

```python
# ❌ Плохо
def test_add(self):
    assert 2 + 3 == 5

# ✅ Хорошо
def test_add_positive_numbers(self):
    """Сложение двух положительных чисел."""
    result = CalculatorService.add(2, 3)
    assert result == 5
```

### 2. **One Assertion Per Test (обычно)**

```python
# ❌ Плохо (слишком много проверок)
def test_operation(self):
    result = CalculatorService.add(2, 3)
    assert result == 5
    assert isinstance(result, float)
    assert result > 0
    assert result != 4

# ✅ Хорошо (фокусированный тест)
def test_add_returns_correct_result(self):
    result = CalculatorService.add(2, 3)
    assert result == 5

def test_add_returns_float(self):
    result = CalculatorService.add(2, 3)
    assert isinstance(result, float)
```

### 3. **Используйте Fixtures для Setup/Teardown**

```python
# ✅ Хорошо - Fixtures в conftest.py
@pytest.fixture
def app():
    app = create_app(config_name='testing')
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

# Использование в тестах
def test_api(self, client):
    response = client.get('/')
    assert response.status_code == 200
```

### 4. **Параметризованные Тесты**

```python
# ✅ Хорошо - Одна функция для нескольких тестов
@pytest.mark.parametrize('a,b,expected', [
    (2, 3, 5),
    (-2, -3, -5),
    (0, 5, 5),
    (10, -5, 5),
])
def test_add_various_numbers(self, a, b, expected):
    result = CalculatorService.add(a, b)
    assert result == expected
```

### 5. **Тестируйте Edge Cases**

```python
# ✅ Хорошо - Граничные случаи
def test_divide_zero_by_number(self):
    result = CalculatorService.divide(0, 5)
    assert result == 0.0

def test_divide_negative_numbers(self):
    result = CalculatorService.divide(-10, -2)
    assert result == 5.0

def test_square_root_of_one(self):
    result = CalculatorService.square_root(1)
    assert result == 1
```

### 6. **Используйте pytest.approx для Float Сравнений**

```python
# ✅ Хорошо
def test_division_with_float(self):
    result = CalculatorService.divide(7, 2)
    assert result == pytest.approx(3.5)

# ❌ Плохо (проблемы с точностью)
def test_division_with_float(self):
    result = CalculatorService.divide(7, 2)
    assert result == 3.5  # Может не пройти из-за float precision
```

### 7. **Разделите Unit и Integration Тесты**

```
tests/
├── test_calculator_service.py    # Unit tests (Service Layer)
└── test_routes.py                # Integration tests (API)
```

### 8. **Помечайте Медленные Тесты**

```python
# ✅ Хорошо
@pytest.mark.slow
def test_very_large_computation(self):
    # Долгий тест
    result = CalculatorService.very_complex_operation()
    assert result

# Запуск только быстрых тестов
# pytest -m "not slow"
```

### 9. **Используйте Context Managers для Исключений**

```python
# ✅ Хорошо
def test_error_handling(self):
    with pytest.raises(DivisionByZeroError):
        CalculatorService.divide(10, 0)

# ❌ Плохо (непредсказуемо)
def test_error_handling(self):
    try:
        CalculatorService.divide(10, 0)
    except DivisionByZeroError:
        pass
```

### 10. **Документируйте Тесты**

```python
# ✅ Хорошо
def test_add_positive_numbers(self):
    """
    Тестирует сложение двух положительных чисел.
    
    Проверяет:
    - Правильность вычисления
    - Тип результата (float)
    """
    result = CalculatorService.add(2, 3)
    assert result == 5
    assert isinstance(result, float)
```

---

## 🔄 Continuous Testing

### Запуск Тестов при Изменении Файлов

```bash
# Установка pytest-watch
pip install pytest-watch

# Запуск с автоперезагрузкой
ptw
```

### Pre-commit Hooks (Git)

```bash
# .git/hooks/pre-commit
#!/bin/bash
pytest tests/
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

---

## 📊 Test Report

```bash
# Создать HTML отчет
pytest --html=report.html --self-contained-html

# Создать JUnit XML (для CI/CD)
pytest --junit-xml=report.xml

# Создать Coverage отчет
pytest --cov=app --cov-report=html tests/
```

---

## 🐛 Debugging Tests

### Запуск с Debug Info

```bash
# Verbose output
pytest -v

# Очень подробный output с locals
pytest -vv

# Traceback
pytest --tb=long
```

### Использование pdb

```python
def test_something(self):
    result = CalculatorService.add(2, 3)
    import pdb; pdb.set_trace()  # Отладчик остановится здесь
    assert result == 5
```

### Использование pytest.set_trace()

```python
def test_something(self):
    result = CalculatorService.add(2, 3)
    pytest.set_trace()  # Отладчик
    assert result == 5
```

---

## ✨ Итого

**Текущее состояние:**
- ✅ 68 тестов (все passing)
- ✅ Unit тесты для Service Layer
- ✅ Integration тесты для API
- ✅ Edge case тесты
- ✅ Error handling тесты
- ✅ Pytest fixtures
- ✅ 95%+ code coverage

**Рекомендации:**
1. Запускайте тесты перед каждым коммитом
2. Добавляйте тесты для новых функций
3. Поддерживайте высокое покрытие (>90%)
4. Используйте CI/CD для автоматических тестов

---

**Версия**: 1.0.0
**Дата**: Декабрь 2025
