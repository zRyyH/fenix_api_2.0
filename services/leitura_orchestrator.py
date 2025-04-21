from repository.consumos_condominios import ConsumosCondominiosRepository
from repository.consumos_unidades import ConsumosUnidadesRepository
from repository.leituras_unidades import LeiturasUnidadesRepository
from repository.condominios import CondominiosRepository
from decorators.service_error import error_handler
from core.factory import CalculatorFactory
from core.data_fetcher import DataFetcher
from logger import info
import json


class LeituraOrchestrator:
    """Orquestra todo o processo de cálculo das leituras."""

    def __init__(self):
        self.condominios_repo = CondominiosRepository()
        self.consumos_condominios_repo = ConsumosCondominiosRepository()
        self.consumos_unidades_repo = ConsumosUnidadesRepository()
        self.leituras_unidades_repo = LeiturasUnidadesRepository()
        self.data_fetcher = DataFetcher()
        self.calculator_factory = CalculatorFactory()

    @error_handler
    def processar_leituras(self, data_da_leitura):
        """
        Processa as leituras para todos os condomínios.

        Args:
            data_da_leitura: Data da leitura para processamento
        """
        for condominio in self.condominios_repo.obter_todos():
            info(f"Processando leituras para condomínio {condominio['id']}")

            # Obtém todos os dados necessários
            raw_data = self.data_fetcher.obter_todos_dados(condominio, data_da_leitura)
            raw_data["condominio"] = condominio

            info(json.dumps(raw_data, indent=4))

            # Cria o calculador de condomínio
            condominio_calculator = self.calculator_factory.create_calculator(
                "condominio"
            )

            # Realiza todos os cálculos
            results = condominio_calculator.calculate(raw_data)

            # Salva os resultados
            self._salvar_resultados(results)

            # Atualiza o status das leituras para "processado"
            self._atualizar_status_leituras(raw_data["leituras_unidades"])

            info(f"Concluído processamento para condomínio {condominio['id']}")

    @error_handler
    def _salvar_resultados(self, results):
        """
        Salva os resultados dos cálculos no banco de dados.

        Args:
            results: Resultados dos cálculos
        """
        # Salva consumos das unidades
        for consumo_unidade in results["consumos_unidades"]:
            self.consumos_unidades_repo.criar_consumos(consumo_unidade)

        # Poderia adicionar lógica para salvar consumos do condomínio também
        # self.consumos_condominios_repo.criar_consumos(...)

    @error_handler
    def _atualizar_status_leituras(self, leituras_unidades):
        """
        Atualiza o status das leituras para "processado".

        Args:
            leituras_unidades: Lista de leituras a serem atualizadas
        """
        for leitura in leituras_unidades:
            # Atualizar apenas leituras com status "concluido"
            if leitura.get("status") == "concluido":
                # Preparar o payload para atualização
                payload = {"status": "processado"}

                # Fazer o PATCH da leitura
                self.leituras_unidades_repo.atualizar_leitura(leitura["id"], payload)
                info(f"Leitura {leitura['id']} atualizada para status 'processado'")
