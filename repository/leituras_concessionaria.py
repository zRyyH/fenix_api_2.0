from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class LeiturasConcessionariaRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_todos(self, periodo_da_leitura):
        return self.directus_api.get_directus(
            endpoint="/items/leituras_concessionaria",
            params={
                "filter[data_da_leitura][_between]": periodo_da_leitura,
            },
        )["data"]

    @error_handler
    def obter_por_condominio_id(self, condominio_id, periodo_da_leitura):
        return self.directus_api.get_directus(
            endpoint="/items/leituras_concessionaria",
            params={
                "filter[condominio_id][_eq]": condominio_id,
                "filter[data_da_leitura][_between]": periodo_da_leitura,
            },
        )["data"]

    @error_handler
    def criar_leituras(self, payload):
        return self.directus_api.post_directus(
            endpoint="/items/leituras_concessionaria", json_data=payload
        )["data"]
