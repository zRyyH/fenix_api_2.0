from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class LeiturasUnidadesRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_todos(self):
        return self.directus_api.get_directus(endpoint="/items/leituras_unidades")[
            "data"
        ]

    @error_handler
    def obter_por_condominio_id(self, condominio_id):
        return self.directus_api.get_directus(
            endpoint="/items/leituras_unidades",
            params={
                "filter[medidor_unidade_id][unidade_id][condominio_id][_eq]": condominio_id,
                "fields": "*,medidor_unidade_id.unidade_id.*",
            },
        )["data"]

    @error_handler
    def criar_leituras(self, payload):
        return self.directus_api.post_directus(
            endpoint="/items/leituras_unidades", json_data=payload
        )["data"]

    @error_handler
    def atualizar_leitura(self, leitura_id, payload):
        """
        Atualiza uma leitura existente.

        Args:
            leitura_id: ID da leitura a ser atualizada
            payload: Dados a serem atualizados

        Returns:
            dict: Leitura atualizada
        """
        return self.directus_api.patch_directus(
            endpoint=f"/items/leituras_unidades/{leitura_id}", json_data=payload
        )["data"]
