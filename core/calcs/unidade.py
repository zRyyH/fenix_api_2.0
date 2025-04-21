from .base import Calculator, CompositeCalculator
from .valor_individual import ValorIndividualCalculator
from .valor_medicao import ValorMedicaoCalculator
from decorators.calc_error import error_handler
from logger import info
import json


class UnidadeCalculator(CompositeCalculator):
    """Calcula todos os valores relacionados a uma unidade."""

    def __init__(self):
        super().__init__(
            [
                ValorIndividualCalculator(),
                ValorMedicaoCalculator(),
            ]
        )

    @error_handler
    def calculate(self, data):
        """
        Calcula todos os valores para uma unidade específica.

        Args:
            data: Dicionário com todos os dados necessários:
                - leitura: dados da leitura da unidade
                - tarifa: dados da tarifa aplicada
                - faixas_de_consumo: faixas de consumo
                - residuo_individual: valor do resíduo individual (opcional)

        Returns:
            dict: Dicionário com os valores calculados para a unidade no formato simplificado
        """
        # Contexto para os calculadores internos
        context = {
            "leitura": data["leitura"]["leitura"],
            "faixas_de_consumo": data["faixas_de_consumo"],
            "tarifa": data["tarifa"],
            "leituras_unidades": data["leituras_unidades"],
        }

        # Calcula valor individual
        valor_individual = self.calculators[0].calculate(context)

        # Calcula valor de medição individual
        valor_medicao_individual = self.calculators[1].calculate(context)

        # Valores do resíduo (se fornecidos)
        valor_residuo_individual = data.get("residuo_individual", 0.0)

        # Calcula valor total
        valor_total_individual = valor_individual

        # Adiciona valor do resíduo se configurado
        if data["tarifa"]["conta_zero"]:
            valor_total_individual += valor_residuo_individual

        # Adiciona valor de medição se configurado
        if data["tarifa"]["incluir_valor_medicao"]:
            valor_total_individual += valor_medicao_individual

        # Monta o resultado no formato simplificado
        result = {
            "leitura_unidade_id": data["leitura"]["id"],
            "valor_individual": valor_individual,
            "valor_residual": valor_residuo_individual,
            "valor_medicao": valor_medicao_individual,
            "valor_total": valor_total_individual,
        }

        info(f"Consumo Unidade: {json.dumps(result, indent=4)}")
        return result
