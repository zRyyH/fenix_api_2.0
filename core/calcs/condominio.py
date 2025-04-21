from .base import CompositeCalculator
from .valor_concessionaria import ValorConcessionariaCalculator
from .residuo import ResiduoCalculator
from .unidade import UnidadeCalculator
from decorators.calc_error import error_handler


class CondominioCalculator(CompositeCalculator):
    """Coordena todos os cálculos relacionados ao condomínio."""

    def __init__(self):
        super().__init__(
            [
                ValorConcessionariaCalculator(),
                ResiduoCalculator(),
                UnidadeCalculator(),
            ]
        )

    @error_handler
    def calculate(self, data):
        """
        Realiza todos os cálculos para o condomínio e suas unidades.

        Args:
            data: Dicionário com todos os dados do condomínio

        Returns:
            dict: Resultados dos cálculos
        """
        valor_concessionaria_calculator = self.calculators[0]
        residuo_calculator = self.calculators[1]
        unidade_calculator = self.calculators[2]

        # Calcula valor da concessionária
        valor_concessionaria = valor_concessionaria_calculator.calculate(data)

        # Calcula total arrecadado (somando valores individuais)
        total_arrecadado = 0.0
        for leitura in data["leituras_unidades"]:
            # Verificar se a leitura tem o status "concluido"
            if not leitura.get("status") == "concluido":
                continue

            # Contexto para cálculo do valor individual
            context = {
                "leitura": leitura["leitura"],
                "faixas_de_consumo": data["faixas_de_consumo"],
                "tarifa": data["tarifa"],
            }

            # Usa o mesmo calculador de valor individual que está no UnidadeCalculator
            valor_individual = unidade_calculator.calculators[0].calculate(context)
            total_arrecadado += valor_individual

        # Contexto para cálculo do resíduo
        residuo_context = {
            "valor_concessionaria": valor_concessionaria,
            "total_arrecadado": total_arrecadado,
            "leituras_unidades": data["leituras_unidades"],
        }

        # Calcula resíduo
        residuo_result = residuo_calculator.calculate(residuo_context)

        # Calcula consumos das unidades
        consumos_unidades = []
        for leitura in data["leituras_unidades"]:
            # Processar apenas leituras com status concluído
            if not leitura.get("status") == "concluido":
                continue

            # Contexto para cálculo da unidade
            unidade_context = {
                "leitura": leitura,
                "faixas_de_consumo": data["faixas_de_consumo"],
                "tarifa": data["tarifa"],
                "leituras_unidades": data["leituras_unidades"],
                "residuo_individual": residuo_result["residuo_individual"],
                "condominio": data["condominio"],
            }

            # Calcula valores da unidade
            consumo_unidade = unidade_calculator.calculate(unidade_context)
            consumos_unidades.append(consumo_unidade)

        # Retorna todos os resultados
        return {
            "valor_concessionaria": valor_concessionaria,
            "total_arrecadado": total_arrecadado,
            "residuo": residuo_result["residuo"],
            "residuo_individual": residuo_result["residuo_individual"],
            "residuo_porcentual": residuo_result["residuo_porcentual"],
            "consumos_unidades": consumos_unidades,
        }
