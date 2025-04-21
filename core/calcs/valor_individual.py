from .base import Calculator
from decorators.calc_error import error_handler
from logger import info


class ValorIndividualCalculator(Calculator):
    """Calcula o valor individual baseado no consumo e faixas de tarifa."""

    @error_handler
    def calculate(self, data):
        """
        Calcula o valor individual baseado nas faixas de consumo.

        Args:
            data: Dicionário com:
                - leitura: consumo da unidade
                - faixas_de_consumo: lista de faixas de consumo
                - tarifa: informações da tarifa

        Returns:
            float: Valor individual calculado
        """
        consumo = float(data["leitura"])
        total = 0.0

        # Ordenar as faixas pelo consumo mínimo para garantir que a primeira faixa seja aplicada corretamente
        faixas_ordenadas = sorted(
            data["faixas_de_consumo"],
            key=lambda f: float(f["faixas_de_consumo_id"]["consumo_minimo"]),
        )

        # Aplicar a primeira faixa integralmente, independente do consumo
        primeira_faixa = faixas_ordenadas[0]["faixas_de_consumo_id"]
        consumo_primeira_faixa = float(primeira_faixa["consumo_maximo"]) - float(
            primeira_faixa["consumo_minimo"]
        )
        total += consumo_primeira_faixa * float(primeira_faixa["taxa"])

        # Se o consumo for maior que o máximo da primeira faixa, calcular as faixas adicionais
        if consumo > float(primeira_faixa["consumo_maximo"]):
            # Para as faixas restantes, calcular normalmente
            for faixa in faixas_ordenadas[1:]:
                faixa = faixa["faixas_de_consumo_id"]
                volume = max(
                    0,
                    min(consumo, float(faixa["consumo_maximo"]))
                    - float(faixa["consumo_minimo"]),
                )

                total += volume * float(faixa["taxa"])

        # Duplica o valor se tiver tarifa de esgoto
        if data["tarifa"]["tarifa_de_esgoto"]:
            total *= 2

        info(
            f"Valor Individual: {total:.2f}, Consumo: {consumo:.2f}, Consumo mínimo aplicado: {consumo_primeira_faixa:.2f}m³"
        )

        return total
