from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class ConsumosUnidadesRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_todos_por_unidade_id(self, unidade_id):
        return self.directus_api.get_directus(
            endpoint="/items/consumos_unidades",
            params={
                "filter[unidade_id][_eq]": unidade_id,
            },
        )["data"]

    @error_handler
    def obter_todos_por_condominio_id(self, unidades_ids):
        # Se unidades_ids for uma lista
        if isinstance(unidades_ids, list):
            return self.directus_api.get_directus(
                endpoint="/items/consumos_unidades",
                params={
                    "filter[unidade_id][_in]": ",".join(str(id) for id in unidades_ids),
                },
            )["data"]
        # Se for um único ID
        else:
            return self.directus_api.get_directus(
                endpoint="/items/consumos_unidades",
                params={
                    "filter[unidade_id][condominio_id][_eq]": unidades_ids,
                },
            )["data"]

    @error_handler
    def criar_consumos(self, payload):
        return self.directus_api.post_directus(
            endpoint="/items/consumos_unidades", json_data=payload
        )["data"]
