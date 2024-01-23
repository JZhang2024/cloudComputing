'''unit tests for calculator.py'''
import pytest
import calculator

class TestCalculator():
    def test_add(self):
        assert calculator.add(1, 2) == 3
        assert calculator.add(0, 0) == 0
        assert calculator.add(-1, -3) == -4
        assert calculator.add(1, -3) == -2
    
    def test_subtract(self):
        assert calculator.subtract(1, 2) == -1
        assert calculator.subtract(0, 0) == 0
        assert calculator.subtract(-1, -3) == 2
        assert calculator.subtract(1, -3) == 4
    
    def test_multiply(self):
        assert calculator.multiply(1, 2) == 2
        assert calculator.multiply(0, 0) == 0
        assert calculator.multiply(-1, -3) == 3
        assert calculator.multiply(1, -3) == -3
    
    def test_divide(self):
        assert calculator.divide(1, 2) == 0.5
        with pytest.raises(ZeroDivisionError):
            calculator.divide(1, 0)
        assert calculator.divide(-18, -6) == 3
        assert calculator.divide(18, -6) == -3
    
    def test_invalid_operation(self):
        with pytest.raises(ValueError):
            calculator.operation(1, 2, "!")
        with pytest.raises(ValueError):
            calculator.operation(1, 2, "a")
        with pytest.raises(ValueError):
            calculator.operation(1, 2, " ")
        