from abc import ABC, abstractmethod


class Calculator(ABC):
    """Interface base para todos os calculadores."""

    @abstractmethod
    def calculate(self, data):
        """Realiza o cálculo e retorna o resultado."""
        pass


class CompositeCalculator(Calculator):
    """Calculador que combina outros calculadores."""

    def __init__(self, calculators=None):
        self.calculators = calculators or []

    def add_calculator(self, calculator):
        """Adiciona um calculador à composição."""
        self.calculators.append(calculator)
