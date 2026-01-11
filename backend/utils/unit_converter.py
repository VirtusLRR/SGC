from decimal import Decimal
from typing import Tuple

CONVERSION_MAP = {
    # De unidade menor para maior: quantas unidades menores cabem na maior
    ("grama", "kg"): Decimal('1000'),              # 1000 gramas = 1 kg
    ("grama", "quilograma"): Decimal('1000'),      # 1000 gramas = 1 quilograma
    ("grama", "grama"): Decimal('1'),              # 1 grama = 1 grama
    ("mililitro", "litro"): Decimal('1000'),       # 1000 ml = 1 litro
    ("mililitro", "mililitro"): Decimal('1'),      # 1 ml = 1 ml
    ("unidade", "unidade"): Decimal('1'),          # 1 unidade = 1 unidade
    ("unidade", "pacote"): Decimal('1'),           # 1 unidade = 1 pacote
    ("unidade", "duzia"): Decimal('12'),           # 12 unidades = 1 dúzia
    ("kg", "kg"): Decimal('1'),                    # 1 kg = 1 kg
    ("quilograma", "quilograma"): Decimal('1'),    # 1 kg = 1 kg
    ("litro", "litro"): Decimal('1'),              # 1 litro = 1 litro
}


def get_conversion_factor(measure_unity: str, price_unit: str) -> Decimal:
    """
    Retorna o fator de conversão entre a unidade de medida do estoque
    e a unidade de preço

    Args:
        measure_unity: Unidade de medida do estoque (ex: 'grama', 'mililitro')
        price_unit: Unidade do preço (ex: 'kg', 'litro')

    Returns:
        Fator de conversão como Decimal
    """
    key = (measure_unity.lower(), price_unit.lower())
    factor = CONVERSION_MAP.get(key)
    if factor is None:
        return Decimal('1')

    return factor


def calculate_item_total_value(amount: Decimal, price: Decimal, measure_unity: str, price_unit: str) -> Decimal:
    """
    Calcula o valor total de um item considerando conversão de unidades

    Args:
        amount: Quantidade em estoque
        price: Preço por unidade de price_unit
        measure_unity: Unidade de medida do estoque
        price_unit: Unidade do preço

    Returns:
        Valor total como Decimal
    """
    factor = get_conversion_factor(measure_unity, price_unit)
    return (amount / factor) * price


def calculate_unit_price(price: Decimal, price_unit: str, target_unit: str) -> Decimal:
    """
    Converte o preço de uma unidade para outra
    
    Exemplo: price=10.00, price_unit='quilograma', target_unit='grama'
    Resultado: 10.00 / 1000 = 0.01 (preço por grama)

    Args:
        price: Preço na unidade original (ex: 10.00 por kg)
        price_unit: Unidade original do preço (ex: 'quilograma')
        target_unit: Unidade desejada (ex: 'grama')

    Returns:
        Preço convertido como Decimal (ex: 0.01 por grama)
    """
    # Converter price para Decimal se não for
    if not isinstance(price, Decimal):
        price = Decimal(str(price))
    
    # Tratar valores None
    if price_unit is None:
        price_unit = 'unidade'
    if target_unit is None:
        target_unit = 'unidade'
    
    # Normalizar unidades
    price_unit_normalized = 'kg' if price_unit.lower() in ['quilograma', 'kg'] else price_unit.lower()
    target_unit_normalized = target_unit.lower()
    
    factor = get_conversion_factor(target_unit_normalized, price_unit_normalized)
    return price / factor