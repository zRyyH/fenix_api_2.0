from .calcs.condominio import CondominioCalculator
from .calcs.unidade import UnidadeCalculator
from .calcs.valor_individual import ValorIndividualCalculator
from .calcs.valor_medicao import ValorMedicaoCalculator
from .calcs.valor_concessionaria import ValorConcessionariaCalculator
from .calcs.residuo import ResiduoCalculator


class CalculatorFactory:
    """Fábrica para criar calculadores conforme necessário."""

    @staticmethod
    def create_calculator(calculator_type):
        """
        Cria um calculador do tipo especificado.

        Args:
            calculator_type: Tipo de calculador a ser criado

        Returns:
            Calculator: Instância do calculador
        """
        calcs = {
            "condominio": CondominioCalculator,
            "unidade": UnidadeCalculator,
            "valor_individual": ValorIndividualCalculator,
            "valor_medicao": ValorMedicaoCalculator,
            "valor_concessionaria": ValorConcessionariaCalculator,
            "residuo": ResiduoCalculator,
        }

        if calculator_type not in calcs:
            raise ValueError(f"Tipo de calculador não suportado: {calculator_type}")

        return calcs[calculator_type]()
