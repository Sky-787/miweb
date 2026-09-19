from main import calculator

def test_sum():
    calc = calculator()
    assert calc.sum(2, 2) == 4

def test_resta():
    calc = calculator()
    assert calc.resta(5, 3) == 2