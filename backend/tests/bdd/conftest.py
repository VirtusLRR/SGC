"""
Configuração do pytest para testes BDD
"""
import pytest


def pytest_configure(config):
    """Configuração adicional do pytest para BDD"""
    config.addinivalue_line(
        "markers", "bdd: marca testes BDD com pytest-bdd"
    )

