from .base import Calculator
from decorators.calc_error import error_handler


class ValorMedicaoCalculator(Calculator):
    """Calcula o valor de medição individual."""

    @error_handler
    def calculate(self, data):
        """
        Calcula o valor de medição individual.

        Args:
            data: Dicionário com:
                - tarifa: contém o valor_de_medicao
                - leituras_unidades: lista de leituras

        Returns:
            float: Valor de medição individual
        """
        valor_medicao = float(data["tarifa"]["valor_de_medicao"])
        leituras = float(len(data["leituras_unidades"]))

        # Evitar divisão por zero
        if leituras == 0:
            return 0.0

        return valor_medicao / leituras
