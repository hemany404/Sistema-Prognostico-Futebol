
from fastapi import APIRouter,Depends
from typing import  Annotated
from sqlalchemy.orm import session


notificao_roteador = APIRouter(prefix="/not",tags=["notificao"])

class servico_notificacao:
    def enviar(self,mensagem):
        print(f"{mensagem}")

def usar_servico_notificacao():
    return servico_notificacao()

notificacao_dependencia = Annotated[servico_notificacao, Depends(usar_servico_notificacao)]        
@notificao_roteador.post("/not")
async def notificar(mensagem: str, servico: notificacao_dependencia):
    servico.enviar(mensagem)