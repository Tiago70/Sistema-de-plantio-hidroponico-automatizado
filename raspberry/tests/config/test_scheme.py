def test_max_values(fake_dataclass):
    """ Testa todas as possibilidades para a verificação de valor máximo """
    assert fake_dataclass.is_high('T', 31) == True
    assert fake_dataclass.is_high('C', 3) == True
    assert fake_dataclass.is_high('Invalid module', 22) == False

    assert fake_dataclass.is_high('T', 20) == False
    assert fake_dataclass.is_high('C', 1) == False

def test_min_values(fake_dataclass):
    """ Testa todas as possibilidades para a verificação de valor mínimo """
    assert fake_dataclass.is_low('T', 9) == True
    assert fake_dataclass.is_low('C', 0.09) == True
    assert fake_dataclass.is_low('Invalid module', 22) == False

    assert fake_dataclass.is_low('T', 20) == False
    assert fake_dataclass.is_low('C', 1) == False