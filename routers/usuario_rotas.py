from fastapi import APIRouter,Depends,HTTPException
from dependecias import verificar_usuario,pegar_sessao
from models.modelos import Usuario
from sqlalchemy.orm import session
from schema.schemas import PagarPlanoSchema,RespostaUsuarioSchema
from datetime import datetime,timedelta,timezone
from typing import List


usuario_roteador = APIRouter(prefix="/usuario", tags=["usuario"])



@usuario_roteador.get("/usuario/me", response_model=RespostaUsuarioSchema)
async def usuario_dados(usuario: Usuario=Depends(verificar_usuario),session: session = Depends(pegar_sessao)):
        usuario = session.query(Usuario).filter(Usuario.id == usuario.id).first()
        if usuario.data_expiracao_plano:
            mensagem ="o seu plano expira em:" + usuario.data_expiracao_plano.strftime("%d/%m/%Y")
        else:
            mensagem= "Ainda não ativou nenhum plano"    
        return{
            "usuario": usuario,
            "mensagem":mensagem
        }

@usuario_roteador.post("/pagar")
async def pagar_plano(pagar_schema: PagarPlanoSchema,session: session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_usuario)):
    
    
    if usuario.data_expiracao_plano and usuario.data_expiracao_plano.tzinfo is None:
        usuario.data_expiracao_plano = usuario.data_expiracao_plano.replace(tzinfo=timezone.utc)
    
    if usuario.status_pagamento == "PAGO" and usuario.data_expiracao_plano  > datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail=f"Você já tem um plano ativo até {usuario.data_expiracao_plano.strftime('%d/%m/%Y')}")

    usuario.plano = pagar_schema.plano
    usuario.data_expiracao_plano = datetime.now(timezone.utc) + timedelta(days=30)
    usuario.status_pagamento = "PAGO"
    session.commit()

    return {
        "mensagem": f"Plano '{usuario.plano}' ativo com sucesso!",
        "expira_em": usuario.data_expiracao_plano.strftime("%d/%m/%Y")
    }

@usuario_roteador.get("/listar_usuarios")
async def listar_usuarios(usuario: Usuario = Depends(verificar_usuario),session: session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="voce não tem autorizacao para listar usuarios")
    else:
        lista = session.query(Usuario).all()
        return{
            "numero de usuarios": len(lista),
            "usuarios": lista
        }