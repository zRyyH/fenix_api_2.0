from .base import Calculator
from decorators.calc_error import error_handler
from logger import info, error


class ResiduoCalculator(Calculator):
    """Calcula o resíduo, resíduo individual e percentual."""

    @error_handler
    def calculate(self, data):
        """
        Calcula valores relacionados ao resíduo.

        Args:
            data: Dicionário com:
                - valor_concessionaria: valor calculado da concessionária
                - total_arrecadado: valor total arrecadado
                - leituras_unidades: lista de leituras

        Returns:
            dict: Contendo:
                - residuo: valor total do resíduo
                - residuo_individual: resíduo por unidade
                - residuo_porcentual: percentual do resíduo
        """
        total_arrecadado = data["total_arrecadado"]
        valor_concessionaria = data["valor_concessionaria"]

        if total_arrecadado == 0:
            error("Total arrecadado é zero, não é possível calcular o resíduo.")
            return {
                "residuo": 0.0,
                "residuo_individual": 0.0,
                "residuo_porcentual": 0.0,
            }

        # Calcula o resíduo (diferença entre valor concessionária e total arrecadado)
        residuo_calculado = valor_concessionaria - total_arrecadado

        # Garante que o resíduo nunca seja negativo
        residuo = max(0.0, residuo_calculado)

        # Se o resíduo calculado for negativo, registra uma mensagem informativa
        if residuo_calculado < 0:
            info(
                f"Resíduo calculado como negativo ({residuo_calculado:.2f}), definido como 0.0"
            )

        # Calcula o resíduo individual e porcentual apenas se o resíduo for maior que zero
        if residuo > 0 and len(data["leituras_unidades"]) > 0:
            residuo_individual = residuo / len(data["leituras_unidades"])
            residuo_porcentual = (
                (residuo / total_arrecadado) * 100 if total_arrecadado > 0 else 0.0
            )
        else:
            residuo_individual = 0.0
            residuo_porcentual = 0.0

        info(
            f"Residuo: R$ {residuo:.2f} - Residuo Individual: R$ {residuo_individual:.2f} - "
            f"Residuo Percentual: {residuo_porcentual:.2f}%"
        )

        return {
            "residuo": residuo,
            "residuo_individual": residuo_individual,
            "residuo_porcentual": residuo_porcentual,
        }
