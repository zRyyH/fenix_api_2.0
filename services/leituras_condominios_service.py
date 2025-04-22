from repository.condominios import CondominiosRepository
from utils.data_utils import extrair_data
from logger import info, error, warning


# Classe de serviço para manipular condominios
condominios_repository = CondominiosRepository()


def validar_leitura(medidor, leituras, payload):
    if not leituras:
        return True

    # Verifica se a leitura já existe para o medidor e o mês de referência
    for leitura in leituras:
        if leitura["medidor_condominio_id"] != medidor:
            continue

        mes_proxima_leitura = (
            extrair_data(payload.data_da_proxima_leitura)["ano_mes"]
            == extrair_data(leitura["data_da_proxima_leitura"])["ano_mes"]
        )

        mes_leitura_atual = (
            extrair_data(payload.data_da_leitura)["ano_mes"]
            == extrair_data(leitura["data_da_leitura"])["ano_mes"]
        )

        mes_referencia = (
            extrair_data(payload.mes_de_referencia)["ano_mes"]
            == extrair_data(leitura["mes_de_referencia"])["ano_mes"]
        )

        if mes_proxima_leitura or mes_leitura_atual or mes_referencia:
            warning(
                f"Leitura já existe para o medidor {medidor} no mês de referência {leitura['mes_de_referencia']}."
            )

            return False

    return True
