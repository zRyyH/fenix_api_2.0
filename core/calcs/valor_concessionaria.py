from .base import Calculator
from decorators.calc_error import error_handler
from logger import info


class ValorConcessionariaCalculator(Calculator):
    """Calcula o valor da concessionária com garantidora percentual."""

    @error_handler
    def calculate(self, data):
        """
        Calcula o valor da concessionária incluindo percentual garantidor.

        Args:
            data: Dicionário com:
                - tarifa: contém garantidora_percentual
                - leitura_concessionaria: lista com valor_da_conta

        Returns:
            float: Valor da concessionária calculado
        """
        porcentual = float(data["tarifa"]["garantidora_percentual"])

        if (
            not data["leitura_concessionaria"]
            or len(data["leitura_concessionaria"]) == 0
        ):
            return 0.0

        valor_da_conta = float(data["leitura_concessionaria"][0]["valor_da_conta"])
        valor_concessionaria = valor_da_conta * (1 + porcentual / 100)

        info(f"Valor da conta: R$ {valor_concessionaria:.2f}")
        return valor_concessionaria
