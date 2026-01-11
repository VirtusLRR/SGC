import pytest
from decimal import Decimal
from utils.unit_converter import calculate_unit_price, get_conversion_factor


def test_calculate_unit_price_kg_to_grams():
    """Testa conversão de preço de quilogramas para gramas."""
    price = Decimal('10.00')
    price_unit = 'quilograma'
    target_unit = 'grama'
    
    unit_price = calculate_unit_price(price, price_unit, target_unit)
    
    assert unit_price == Decimal('0.01')


def test_calculate_cost_for_recipe():
    """Testa o cálculo de custo para uma receita (500g de um item que custa 10 reais/kg)."""
    price = Decimal('10.00')
    price_unit = 'quilograma'
    measure_unity = 'grama'
    
    unit_price = calculate_unit_price(price, price_unit, measure_unity)
    cost_for_500g = Decimal('500.0') * unit_price
    
    assert cost_for_500g == Decimal('5.0')


def test_get_conversion_factor_grams_to_kg():
    """Testa fator de conversão de gramas para kg."""
    factor = get_conversion_factor('grama', 'kg')
    
    assert factor == Decimal('1000')


def test_get_conversion_factor_same_unit():
    """Testa fator de conversão para mesma unidade."""
    factor = get_conversion_factor('grama', 'grama')
    
    assert factor == Decimal('1')


def test_get_conversion_factor_unknown_returns_one():
    """Testa que unidades desconhecidas retornam fator 1."""
    factor = get_conversion_factor('unknown', 'other')
    
    assert factor == Decimal('1')


def test_calculate_unit_price_with_none_defaults_to_unidade():
    """Testa que valores None são tratados como 'unidade'."""
    price = Decimal('5.00')
    
    unit_price = calculate_unit_price(price, None, None)
    
    assert unit_price == Decimal('5.00')


@pytest.mark.parametrize(
    "price,price_unit,target_unit,expected",
    [
        (Decimal('10.00'), 'quilograma', 'grama', Decimal('0.01')),
        (Decimal('5.00'), 'litro', 'mililitro', Decimal('0.005')),
        (Decimal('12.00'), 'duzia', 'unidade', Decimal('1.00')),
        (Decimal('3.50'), 'unidade', 'unidade', Decimal('3.50')),
    ]
)
def test_calculate_unit_price_parametrized(price, price_unit, target_unit, expected):
    """Testa várias conversões de unidade de preço."""
    result = calculate_unit_price(price, price_unit, target_unit)
    
    assert result == expected

