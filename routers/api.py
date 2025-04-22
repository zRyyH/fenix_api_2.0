from services.leituras_unidades_service import criar_leituras_unidades
from services.leitura_orchestrator import LeituraOrchestrator
from middleware.wrapper_routers import handle_exceptions
from models.ProcessarLeituras import ProcessarLeituras
from models.LeituraCondominio import LeituraCondominio
from models.LeituraUnidade import LeituraUnidade
from middleware.auth import verify_token
from constants.globals import API_CONFIG
from fastapi import APIRouter, Depends


# Criar router com autenticação
router = APIRouter(prefix=API_CONFIG["path_api"], dependencies=[Depends(verify_token)])


# Rota para gerar leituras
orchestrator = LeituraOrchestrator()


# Rota para gerar leituras
@router.post("/gerar-leituras-unidades")
@handle_exceptions
async def gerar_leituras_unidades(payload: LeituraUnidade):
    criar_leituras_unidades(payload)
    return {"message": payload}


# Rota para gerar leituras
@router.post("/processar-leituras")
@handle_exceptions
async def gerar_leituras_condominios(payload: ProcessarLeituras):
    orchestrator.processar_leituras(payload.data_da_leitura)
    return {"message": "Leituras processadas com sucesso."}
