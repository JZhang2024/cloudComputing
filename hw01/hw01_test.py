'''unit tests for calculator.py'''
import pytest
import calculator

def test_add():
    '''test add function'''
    assert calculator.add(1, 2) == 3
    assert calculator.add(0, 0) == 0
    assert calculator.add(-1, -3) == -4
    assert calculator.add(1, -3) == -2
def test_subtract():
    '''test subtract function'''
    assert calculator.subtract(1, 2) == -1
    assert calculator.subtract(0, 0) == 0
    assert calculator.subtract(-1, -3) == 2
    assert calculator.subtract(1, -3) == 4
def test_multiply():
    '''test multiply function'''
    assert calculator.multiply(1, 2) == 2
    assert calculator.multiply(0, 0) == 0
    assert calculator.multiply(-1, -3) == 3
    assert calculator.multiply(1, -3) == -3
def test_divide():
    '''test divide function'''
    assert calculator.divide(1, 2) == 0.5
    with pytest.raises(ZeroDivisionError):
        calculator.divide(1, 0)
    assert calculator.divide(-18, -6) == 3
    assert calculator.divide(18, -6) == -3
def test_invalid_operation():
    '''test for invalid operations'''
    with pytest.raises(ValueError):
        calculator.operation(1, 2, "!")
    with pytest.raises(ValueError):
        calculator.operation(1, 2, "a")
    with pytest.raises(ValueError):
        calculator.operation(1, 2, " ")
    with pytest.raises(TypeError):
        calculator.operation("", 2, "+")
