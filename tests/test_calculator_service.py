"""
Unit Tests for Calculator Service Layer
========================================
Тесты для Service Layer - ядра бизнес-логики приложения.
Полностью независимы от Flask и фронтенда.
"""
import pytest
import math
from app.service import (
    CalculatorService,
    CalculatorError,
    DivisionByZeroError,
    InvalidInputError,
)


class TestCalculatorServiceAddition:
    """Тесты для операции сложения."""

    def test_add_positive_numbers(self):
        """Сложение двух положительных чисел."""
        result = CalculatorService.add(2, 3)
        assert result == 5
        assert isinstance(result, float)

    def test_add_negative_numbers(self):
        """Сложение двух отрицательных чисел."""
        result = CalculatorService.add(-2, -3)
        assert result == -5

    def test_add_positive_and_negative(self):
        """Сложение положительного и отрицательного числа."""
        result = CalculatorService.add(10, -5)
        assert result == 5

    def test_add_zeros(self):
        """Сложение нулей."""
        result = CalculatorService.add(0, 0)
        assert result == 0

    def test_add_floats(self):
        """Сложение чисел с плавающей точкой."""
        result = CalculatorService.add(1.5, 2.5)
        assert result == pytest.approx(4.0)


class TestCalculatorServiceSubtraction:
    """Тесты для операции вычитания."""

    def test_subtract_positive_numbers(self):
        """Вычитание положительных чисел."""
        result = CalculatorService.subtract(5, 3)
        assert result == 2

    def test_subtract_negative_numbers(self):
        """Вычитание отрицательных чисел."""
        result = CalculatorService.subtract(-5, -3)
        assert result == -2

    def test_subtract_resulting_in_negative(self):
        """Вычитание, результат - отрицательное число."""
        result = CalculatorService.subtract(3, 5)
        assert result == -2

    def test_subtract_from_zero(self):
        """Вычитание из нуля."""
        result = CalculatorService.subtract(0, 5)
        assert result == -5

    def test_subtract_floats(self):
        """Вычитание чисел с плавающей точкой."""
        result = CalculatorService.subtract(5.5, 2.5)
        assert result == pytest.approx(3.0)


class TestCalculatorServiceMultiplication:
    """Тесты для операции умножения."""

    def test_multiply_positive_numbers(self):
        """Умножение положительных чисел."""
        result = CalculatorService.multiply(3, 4)
        assert result == 12

    def test_multiply_by_zero(self):
        """Умножение на ноль."""
        result = CalculatorService.multiply(5, 0)
        assert result == 0

    def test_multiply_negative_numbers(self):
        """Умножение отрицательных чисел."""
        result = CalculatorService.multiply(-3, -4)
        assert result == 12

    def test_multiply_positive_and_negative(self):
        """Умножение положительного на отрицательное."""
        result = CalculatorService.multiply(3, -4)
        assert result == -12

    def test_multiply_floats(self):
        """Умножение чисел с плавающей точкой."""
        result = CalculatorService.multiply(2.5, 4.0)
        assert result == pytest.approx(10.0)


class TestCalculatorServiceDivision:
    """Тесты для операции деления."""

    def test_divide_positive_numbers(self):
        """Деление положительных чисел."""
        result = CalculatorService.divide(10, 2)
        assert result == 5.0

    def test_divide_by_zero_raises_error(self):
        """Деление на ноль вызывает исключение."""
        with pytest.raises(DivisionByZeroError):
            CalculatorService.divide(10, 0)

    def test_divide_negative_numbers(self):
        """Деление отрицательных чисел."""
        result = CalculatorService.divide(-10, -2)
        assert result == pytest.approx(5.0)

    def test_divide_positive_by_negative(self):
        """Деление положительного на отрицательное."""
        result = CalculatorService.divide(10, -2)
        assert result == pytest.approx(-5.0)

    def test_divide_with_remainder(self):
        """Деление с остатком."""
        result = CalculatorService.divide(7, 2)
        assert result == pytest.approx(3.5)

    def test_divide_floats(self):
        """Деление чисел с плавающей точкой."""
        result = CalculatorService.divide(7.5, 2.5)
        assert result == pytest.approx(3.0)

    def test_divide_zero_by_number(self):
        """Деление нуля на число."""
        result = CalculatorService.divide(0, 5)
        assert result == 0.0


class TestCalculatorServiceSquare:
    """Тесты для операции возведения в квадрат."""

    def test_square_positive_number(self):
        """Возведение положительного числа в квадрат."""
        result = CalculatorService.square(5)
        assert result == 25

    def test_square_negative_number(self):
        """Возведение отрицательного числа в квадрат."""
        result = CalculatorService.square(-5)
        assert result == 25

    def test_square_zero(self):
        """Возведение нуля в квадрат."""
        result = CalculatorService.square(0)
        assert result == 0

    def test_square_float(self):
        """Возведение числа с плавающей точкой в квадрат."""
        result = CalculatorService.square(2.5)
        assert result == pytest.approx(6.25)

    def test_square_one(self):
        """Возведение одного в квадрат."""
        result = CalculatorService.square(1)
        assert result == 1


class TestCalculatorServiceSquareRoot:
    """Тесты для операции извлечения квадратного корня."""

    def test_square_root_positive_number(self):
        """Извлечение корня из положительного числа."""
        result = CalculatorService.square_root(16)
        assert result == pytest.approx(4.0)

    def test_square_root_zero(self):
        """Извлечение корня из нуля."""
        result = CalculatorService.square_root(0)
        assert result == 0

    def test_square_root_one(self):
        """Извлечение корня из одного."""
        result = CalculatorService.square_root(1)
        assert result == 1

    def test_square_root_negative_raises_error(self):
        """Извлечение корня из отрицательного числа вызывает исключение."""
        with pytest.raises(InvalidInputError):
            CalculatorService.square_root(-4)

    def test_square_root_float(self):
        """Извлечение корня из числа с плавающей точкой."""
        result = CalculatorService.square_root(6.25)
        assert result == pytest.approx(2.5)

    def test_square_root_two(self):
        """Извлечение корня из двух."""
        result = CalculatorService.square_root(2)
        assert result == pytest.approx(math.sqrt(2))


class TestCalculatorServiceValidation:
    """Тесты для валидации входных данных."""

    def test_validate_integer_string(self):
        """Валидация строки с целым числом."""
        result = CalculatorService.validate_number("42")
        assert result == 42.0
        assert isinstance(result, float)

    def test_validate_float_string(self):
        """Валидация строки с числом с плавающей точкой."""
        result = CalculatorService.validate_number("3.14")
        assert result == pytest.approx(3.14)

    def test_validate_integer(self):
        """Валидация целого числа."""
        result = CalculatorService.validate_number(42)
        assert result == 42.0

    def test_validate_float(self):
        """Валидация числа с плавающей точкой."""
        result = CalculatorService.validate_number(3.14)
        assert result == pytest.approx(3.14)

    def test_validate_negative_number(self):
        """Валидация отрицательного числа."""
        result = CalculatorService.validate_number("-42")
        assert result == -42.0

    def test_validate_invalid_string_raises_error(self):
        """Валидация невалидной строки вызывает исключение."""
        with pytest.raises(InvalidInputError):
            CalculatorService.validate_number("not_a_number")

    def test_validate_none_raises_error(self):
        """Валидация None вызывает исключение."""
        with pytest.raises(InvalidInputError):
            CalculatorService.validate_number(None)

    def test_validate_empty_string_raises_error(self):
        """Валидация пустой строки вызывает исключение."""
        with pytest.raises(InvalidInputError):
            CalculatorService.validate_number("")


class TestCalculatorServiceEdgeCases:
    """Тесты для граничных случаев."""

    def test_very_large_numbers(self):
        """Операции с очень большими числами."""
        large = 1e300
        result = CalculatorService.add(large, 1e299)
        assert result > large

    def test_very_small_numbers(self):
        """Операции с очень маленькими числами."""
        small = 1e-308
        result = CalculatorService.multiply(small, 2)
        assert result > 0

    def test_multiple_operations_sequence(self):
        """Последовательность операций."""
        result1 = CalculatorService.add(2, 3)  # 5
        result2 = CalculatorService.multiply(result1, 2)  # 10
        result3 = CalculatorService.divide(result2, 5)  # 2
        assert result3 == pytest.approx(2.0)
