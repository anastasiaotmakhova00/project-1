# Flask Calculator - Best Practices Project

## 📋 Описание

Полнофункциональное веб-приложение-калькулятор, разработанное на Flask согласно best practices и архитектурным паттернам для обеспечения чистоты кода, тестируемости и долгосрочной поддержки.

### Ключевые особенности

- ✅ **Архитектура Service Layer** - Строгое разделение бизнес-логики и логики представления
- ✅ **Application Factory Pattern** - Гибкое создание экземпляров приложения для различных окружений
- ✅ **TDD/BDD подход** - Полное покрытие unit и интеграционными тестами
- ✅ **Интернационализация (i18n)** - Встроенная поддержка английского и русского языков
- ✅ **Clean Code** - Следование лучшим практикам Python/Flask
- ✅ **Responsive Design** - Адаптивный интерфейс с поддержкой темного режима

---

## 🏗️ Архитектура Проекта

```
project-1/
├── app/                          # Основной пакет приложения
│   ├── __init__.py              # Application Factory (create_app)
│   ├── routes.py                # Controller/View слой (Flask маршруты)
│   ├── service/                 # Service Layer (бизнес-логика)
│   │   ├── __init__.py
│   │   └── calculator_service.py # Вся математическая логика
│   ├── templates/               # Jinja2 шаблоны
│   │   └── index.html          # Главная страница с интерфейсом
│   └── static/                  # Статические файлы
│       ├── css/
│       │   └── style.css        # Стили калькулятора
│       └── js/
│           └── calculator.js    # Клиентская логика
├── tests/                        # Модульные и интеграционные тесты
│   ├── conftest.py              # Pytest конфигурация и fixtures
│   ├── test_calculator_service.py # Unit тесты Service Layer
│   └── test_routes.py           # Интеграционные тесты маршрутов
├── translations/                 # Файлы локализации
│   ├── messages.pot             # Шаблон переводов
│   ├── en/LC_MESSAGES/
│   │   └── messages.po          # Английские переводы
│   └── ru/LC_MESSAGES/
│       └── messages.po          # Русские переводы
├── babel.cfg                    # Конфигурация Flask-Babel
├── requirements.txt             # Зависимости Python
├── pytest.ini                   # Конфигурация pytest
├── .env                         # Переменные окружения
├── run.py                       # Entry point приложения
└── README.md                    # Этот файл
```

---

## 🚀 Быстрый Старт

### Предварительные Требования

- Python 3.8+
- pip или conda

### Установка

1. **Клонируйте репозиторий**
   ```bash
   cd /workspaces/project-1
   ```

2. **Создайте виртуальное окружение** (опционально, но рекомендуется)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate      # Windows
   ```

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

### Запуск Приложения

```bash
python run.py
```

Приложение будет доступно по адресу: **http://localhost:5000**

### Запуск Тестов

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# С покрытием кода
pytest --cov=app tests/

# Только unit тесты
pytest tests/test_calculator_service.py

# Только интеграционные тесты
pytest tests/test_routes.py
```

---

## 📱 Использование Приложения

### Доступные Операции

| Операция | Описание | Пример |
|----------|---------|--------|
| **Сложение** | Добавляет два числа | 5 + 3 = 8 |
| **Вычитание** | Вычитает второе число из первого | 10 − 3 = 7 |
| **Умножение** | Перемножает два числа | 4 × 5 = 20 |
| **Деление** | Делит первое число на второе | 10 ÷ 2 = 5 |
| **Квадрат** | Возводит число в квадрат | x² (5) = 25 |
| **Квадратный корень** | Извлекает корень квадратный | √(16) = 4 |

### Обработка Ошибок

- ✅ **Деление на ноль** - Приложение перехватывает и выдает понятное сообщение об ошибке
- ✅ **Некорректный ввод** - Валидация на стороне клиента и сервера
- ✅ **Отрицательный корень** - Система предупреждает о невозможности операции

---

## 🏛️ Архитектурные Паттерны

### 1. **Application Factory Pattern**

```python
# app/__init__.py
def create_app(config_name='development') -> Flask:
    """Создает и конфигурирует Flask приложение."""
    app = Flask(__name__)
    babel.init_app(app)
    register_routes(app)
    return app
```

**Преимущества:**
- Легко создавать несколько экземпляров приложения (production, testing, development)
- Упрощает тестирование
- Позволяет отложенную инициализацию расширений

### 2. **Service Layer Pattern**

```python
# app/service/calculator_service.py
class CalculatorService:
    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Division by zero is not allowed")
        return float(a / b)
```

**Преимущества:**
- Бизнес-логика полностью независима от Flask
- Легко тестировать без HTTP запросов
- Можно переиспользовать в других контекстах (CLI, задачах и т.д.)

### 3. **MVC/Controller-View Pattern**

```python
# app/routes.py
@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Controller - принимает запрос, вызывает Service, возвращает результат."""
    data = request.get_json()
    result = CalculatorService.divide(data['operand1'], data['operand2'])
    return jsonify({'success': True, 'result': result})
```

**Преимущества:**
- Четкое разделение ответственности
- Маршруты только для HTTP-логики
- Легко модифицировать API без изменения бизнес-логики

### 4. **Exception Handling Pattern**

```python
# Собственные исключения для конкретных ошибок
class DivisionByZeroError(CalculatorError):
    pass

# Специфичная обработка ошибок в контроллере
try:
    result = CalculatorService.divide(a, b)
except DivisionByZeroError:
    return jsonify({'error': 'Division by zero'}), 400
```

---

## 🧪 Тестирование

### Unit Тесты (Service Layer)

```bash
pytest tests/test_calculator_service.py -v
```

**Покрытие:**
- ✅ Все арифметические операции
- ✅ Обработка ошибок (деление на ноль, корень из отрицательного)
- ✅ Граничные случаи (очень большие/маленькие числа)
- ✅ Валидация входных данных
- ✅ Операции с float числами

### Интеграционные Тесты (API Routes)

```bash
pytest tests/test_routes.py -v
```

**Покрытие:**
- ✅ HTTP endpoints работают корректно
- ✅ JSON parsing и response formatting
- ✅ Error handling и HTTP status codes
- ✅ Все операции через API
- ✅ Обработка невалидных requests

### Пример Теста

```python
def test_division_by_zero_api(client):
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

---

## 🌐 Интернационализация (i18n)

### Поддерживаемые Языки

- 🇬🇧 **English** (en)
- 🇷🇺 **Русский** (ru)

### Использование в Шаблонах

```html
<!-- app/templates/index.html -->
<h1>{{ gettext('Scientific Calculator') }}</h1>
<button>{{ gettext('Add') }}</button>
```

### Использование в Python Коде

```python
# app/routes.py
from flask_babel import gettext

error_msg = gettext('Division by zero is not allowed')
```

### Добавление новых Переводов

1. Отметьте строки для перевода используя `gettext()`
2. Обновите файлы переводов:
   ```bash
   pybabel extract -F babel.cfg -o translations/messages.pot .
   pybabel update -i translations/messages.pot -d translations
   pybabel compile -d translations
   ```

---

## 📊 API Документация

### POST `/api/calculate`

Выполняет математическую операцию.

**Request:**
```json
{
  "operation": "add|subtract|multiply|divide|square|square_root",
  "operand1": 10,
  "operand2": 5
}
```

**Response (Success):**
```json
{
  "success": true,
  "result": 15,
  "error": null
}
```

**Response (Error):**
```json
{
  "success": false,
  "result": null,
  "error": "Division by zero is not allowed"
}
```

**Status Codes:**
- `200 OK` - Успешное выполнение операции
- `400 Bad Request` - Невалидный запрос или ошибка вычисления
- `500 Internal Server Error` - Неожиданная ошибка сервера

### GET `/api/health`

Проверка здоровья приложения.

**Response:**
```json
{
  "status": "healthy",
  "service": "Calculator API"
}
```

---

## 💾 Хранение История Вычислений

Приложение сохраняет последние 10 вычислений в `localStorage` браузера:

```javascript
// JavaScript (app/static/js/calculator.js)
calculator.addToHistory(operand1, operation, operand2, result);
```

История автоматически загружается при открытии страницы и отображается в интерфейсе.

---

## 📝 Примеры Кода

### Добавление Новой Операции

1. **Добавьте метод в Service Layer:**

```python
# app/service/calculator_service.py
@staticmethod
def logarithm(a: float, base: float = 10) -> float:
    """Логарифм числа."""
    if a <= 0:
        raise InvalidInputError("Logarithm of non-positive number is undefined")
    return float(math.log(a, base))
```

2. **Добавьте маршрут в Controller:**

```python
# app/routes.py (в функции register_routes)
elif operation == 'logarithm':
    try:
        result = CalculatorService.logarithm(operand1)
    except InvalidInputError as e:
        return jsonify({
            'success': False,
            'result': None,
            'error': gettext(str(e))
        }), 400
```

3. **Напишите тесты:**

```python
# tests/test_calculator_service.py
def test_logarithm():
    result = CalculatorService.logarithm(100, 10)
    assert result == pytest.approx(2.0)

def test_logarithm_invalid():
    with pytest.raises(InvalidInputError):
        CalculatorService.logarithm(-5)
```

---

## 🔒 Безопасность

- ✅ **Input Validation** - Все входные данные валидируются на сервере
- ✅ **Error Handling** - Правильная обработка исключений без утечки информации
- ✅ **JSON Security** - CSRF защита встроена в Flask
- ✅ **Type Checking** - Использование type hints для проверки типов

---

## 📚 Best Practices в Проекте

### 1. **Документирование**
- Docstrings для всех модулей, классов и функций
- Комментарии для сложной логики
- README с примерами использования

### 2. **Code Style**
- PEP 8 compliance
- Meaningful variable names
- DRY (Don't Repeat Yourself)
- SOLID принципы

### 3. **Testing**
- Покрытие критической функциональности
- Test fixtures для переиспользования
- Отделение unit от интеграционных тестов

### 4. **Error Handling**
- Собственные исключения для разных ошибок
- Информативные сообщения об ошибках
- Правильные HTTP status codes

---

## 🐛 Известные Ограничения и Возможные Улучшения

### Текущие Ограничения

- История сохраняется только в браузере (localStorage)
- Нет аутентификации/авторизации
- Нет логирования операций

### Возможные Улучшения

- [ ] Добавить логирование в файл
- [ ] Сохранять историю в базу данных (SQLite, PostgreSQL)
- [ ] Добавить больше научных функций (синус, косинус, логарифм и т.д.)
- [ ] Реализовать кэширование результатов
- [ ] Добавить WebSocket для real-time обновлений
- [ ] Увеличить покрытие тестами до 95%+

---

## 📞 Поддержка и Контакты

Для вопросов, проблем или предложений:

1. Проверьте существующие issues в репозитории
2. Создайте новый issue с подробным описанием
3. Свяжитесь с разработчиком

---

## 📄 Лицензия

Этот проект является учебным примером архитектуры Flask приложений.

---

## 🎯 Заключение

Этот проект демонстрирует:

✅ Как правильно структурировать Flask приложение
✅ Как разделить бизнес-логику и логику представления
✅ Как писать тестируемый код
✅ Как использовать паттерны проектирования
✅ Как обеспечить долгосрочную поддержку и масштабируемость

Приложение готово к использованию как шаблон для более крупных проектов!

---

**Создано:** Декабрь 2025
**Версия:** 1.0.0
**Статус:** Production Ready
