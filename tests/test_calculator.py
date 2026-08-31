import pytest

from agentic_ai.tools.calculator import calculate


def test_addition():
    assert calculate("2 + 2") == "4"


def test_multiplication():
    assert calculate("12 * 5") == "60"


def test_power():
    assert calculate("2 ** 10") == "1024"


def test_sqrt():
    assert calculate("sqrt(25)") == "5"


def test_pi():
    result = float(calculate("pi * 2"))

    assert round(result, 5) == round(
        3.141592653589793 * 2,
        5,
    )


def test_division_by_zero():
    with pytest.raises(ValueError):
        calculate("10 / 0")


def test_unsafe_expression():
    with pytest.raises(ValueError):
        calculate("__import__('os').system('ls')")
