"""
Calculator Service Layer
========================
Бизнес-логика калькулятора, полностью независимая от Flask.
Обеспечивает все арифметические операции и обработку ошибок.
"""
import math
from decimal import Decimal, InvalidOperation


class CalculatorError(Exception):
    """Базовый класс для исключений калькулятора."""
    pass


class DivisionByZeroError(CalculatorError):
    """Ошибка деления на ноль."""
    pass


class InvalidInputError(CalculatorError):
    """Ошибка некорректного входного значения."""
    pass


class CalculatorService:
    """
    Сервис калькулятора с методами для основных арифметических операций.
    
    Все методы принимают числовые значения и возвращают результат или исключение.
    """

    @staticmethod
    def add(a: float, b: float) -> float:
        """Сложение двух чисел."""
        return float(a + b)

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Вычитание b из a."""
        return float(a - b)

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Умножение двух чисел."""
        return float(a * b)

    @staticmethod
    def divide(a: float, b: float) -> float:
        """
        Деление a на b.
        
        Args:
            a: Делимое
            b: Делитель
            
        Returns:
            Результат деления
            
        Raises:
            DivisionByZeroError: Если b равно нулю
        """
        if b == 0:
            raise DivisionByZeroError("Division by zero is not allowed")
        return float(a / b)

    @staticmethod
    def square(a: float) -> float:
        """Возведение числа в квадрат."""
        return float(a * a)

    @staticmethod
    def square_root(a: float) -> float:
        """
        Извлечение квадратного корня из числа.
        
        Args:
            a: Число, из которого извлекается корень
            
        Returns:
            Квадратный корень числа
            
        Raises:
            InvalidInputError: Если число отрицательное
        """
        if a < 0:
            raise InvalidInputError("Cannot calculate square root of negative number")
        return float(math.sqrt(a))

    @staticmethod
    def validate_number(value) -> float:
        """
        Валидация и конвертация входного значения в число.
        
        Args:
            value: Входное значение (строка, int или float)
            
        Returns:
            Валидное число как float
            
        Raises:
            InvalidInputError: Если значение невозможно конвертировать
        """
        try:
            return float(value)
        except (ValueError, TypeError) as e:
            raise InvalidInputError(f"Invalid input: {value}") from e
