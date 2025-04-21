from repository.faixas_de_consumo_tarifas import FaixasDeConsumoTarifasRepository
from repository.leituras_concessionaria import LeiturasConcessionariaRepository
from repository.leituras_condominios import LeiturasCondominiosRepository
from repository.consumos_condominios import ConsumosCondominiosRepository
from repository.leituras_unidades import LeiturasUnidadesRepository
from repository.consumos_unidades import ConsumosUnidadesRepository
from repository.tarifas import TarifasRepository
from decorators.service_error import error_handler


class DataFetcher:
    """Responsável por obter todos os dados necessários para os cálculos."""

    def __init__(self):
        self.consumos_condominios_repo = ConsumosCondominiosRepository()
        self.concessionaria_repo = LeiturasConcessionariaRepository()
        self.consumos_unidades_repo = ConsumosUnidadesRepository()
        self.condominios_repo = LeiturasCondominiosRepository()
        self.faixas_repo = FaixasDeConsumoTarifasRepository()
        self.unidades_repo = LeiturasUnidadesRepository()
        self.tarifas_repo = TarifasRepository()

    @error_handler
    def obter_todos_dados(
        self, condominio, data_da_leitura, data_da_leitura_anterior=None
    ):
        """
        Obtém todos os dados necessários para os cálculos.

        Args:
            condominio: Dados do condomínio
            data_da_leitura: Data da leitura atual
            data_da_leitura_anterior: Data da leitura anterior (opcional)

        Returns:
            dict: Todos os dados necessários para os cálculos
        """
        # Obtém leituras das unidades
        leituras_unidades = self.unidades_repo.obter_por_condominio_id(condominio["id"])

        # Obtém tarifa aplicada
        tarifa = self.tarifas_repo.obter_por_id(condominio["tarifa_id"][0])

        # Obtém leituras da concessionária
        leitura_concessionaria = self.concessionaria_repo.obter_por_condominio_id(
            condominio["id"]
        )

        # Obtém leituras do condomínio
        leitura_condominio = self.condominios_repo.obter_por_medidor_id(
            condominio["medidores_condominios_id"]
        )

        # Obtém faixas de consumo
        faixas_de_consumo = self.faixas_repo.obter_por_tarifa_id(
            tarifa["faixas_de_consumo_id"]
        )

        # Retorna todos os dados
        return {
            "leitura_concessionaria": leitura_concessionaria,
            "leitura_condominio": leitura_condominio,
            "leituras_unidades": leituras_unidades,
            "faixas_de_consumo": faixas_de_consumo,
            "tarifa": tarifa,
        }
