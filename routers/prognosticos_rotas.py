from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import session
from models.modelos import Prognostico,Planos,Usuario
from schema.schemas import PrognosticoSchema,EditarSchema
from dependecias import pegar_sessao,verificar_usuario,verificar_expiracao
from typing import Callable

prognosticos_roteador = APIRouter(prefix="/prognostico", tags=["prognosticos"])



def verificar_plano_usuario(nivel_necessario: str) -> Callable:
    def dependencia(usuario: Usuario = Depends(verificar_usuario)):
        if  usuario.plano != nivel_necessario :
            raise HTTPException(status_code=403,detail=f"Acesso permitido apenas ao plano: {nivel_necessario}")
        return usuario
    return dependencia

@prognosticos_roteador.post("/criar_prognostico")
async def criar_prognostico( prognostico_schema:PrognosticoSchema, session: session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_usuario)):

    if not usuario.admin:
        raise HTTPException(status_code=403,detail="usuario não autorizado")
    plano = session.query(Planos).filter(Planos.nome == prognostico_schema.plano).first()
    if not plano:
        raise HTTPException(status_code=400,detail="este plano não existe")
    novo_prognostico = Prognostico(prognostico_schema.equipa_casa,prognostico_schema.equipa_fora,prognostico_schema.previsao,prognostico_schema.data_jogo,prognostico_schema.plano)
    session.add(novo_prognostico)
    session.commit()
    return{
        "mensagem":f"prognosticos cadastrado com sucesso:id do prognostico {novo_prognostico.id}",
        "prognostico": novo_prognostico
    }
@prognosticos_roteador.put("/prognostico/{id_prognostico}")
async  def editar_prognostico(id_prognostico: int,editar_schema:EditarSchema, session: session = Depends(pegar_sessao),usuario:Usuario = Depends(verificar_usuario)):
    prognostico = session.query(Prognostico).filter(Prognostico.id == id_prognostico).first()
    if not prognostico:
        raise HTTPException(status_code=403,detail="este prognostico não existe")
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="usuario não autorizado")
    editar_schema_dict = editar_schema.dict(exclude_unset=True)
    for chave,valor in editar_schema_dict.items():
        setattr(prognostico,chave,valor)
    session.commit()
    session.refresh(prognostico)

    return{
        "prognostico editado":prognostico
    }
@prognosticos_roteador.post("prognostico/{id_prognostico}")
async def eliminar_prognostico(id_prognostico: int,session: session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_usuario)):
    prognostico = session.query(Prognostico).filter(Prognostico.id == id_prognostico).first()
    if not prognostico:
        raise HTTPException(status_code=403,detail="este prognostico não existe")
    if not usuario.admin:
        raise HTTPException(status_code=401,detail="usuario não autorizado")
    
    session.delete(prognostico)
    session.commit()

    return{
        "mensagem":f"prognostico elimando com sucesso, id:{id_prognostico}"
    }

@prognosticos_roteador.post("/prognostico/{id_prognostico}")
async def detalhes_prognosticos(id_prognostico:int,session: session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_usuario)):
    prognostico = session.query(Prognostico).filter(Prognostico.id == id_prognostico).first()
    if not prognostico:
        raise HTTPException(status_code=400,detail="este prognostico não existe")
    if not usuario.admin and usuario.plano != prognostico.plano:
        raise HTTPException(status_code=403,detail="voce não tem autorizacao")
    return{
        "Detalhes":prognostico
    }


@prognosticos_roteador.get("/prognostico/gratis")
async def  prognosticos_gratis(session: session = Depends(pegar_sessao)):
    prognostico = session.query(Prognostico).filter(Prognostico.plano == "GRÁTIS").all()
    return{
        "Total":len(prognostico),
        "GRATIS":prognostico
    }

@prognosticos_roteador.get("/prognostico/premium")
async def  prognosticos_premium(session: session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_plano_usuario("PREMIUM"))):
    expiracao = verificar_expiracao(usuario,session)
    if usuario.data_expiracao_plano :
        mensagem ="o seu plano expira em:" + usuario.data_expiracao_plano.strftime("%d/%m/%Y")
    else:
        mensagem= "Ainda não ativou nenhum plano"
    prognostico = session.query(Prognostico).filter(Prognostico.plano == "PREMIUM").all()
    return{
        "Total":len(prognostico),
        "PREMIUM":prognostico,
        "mensagem":mensagem
    }

@prognosticos_roteador.get("/prognostico/vip")
async def  prognosticos_vip(session: session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_plano_usuario("VIP"))):
    expiracao = verificar_expiracao(usuario,session)
    if usuario.data_expiracao_plano:
        mensagem ="o seu plano expira em:" + usuario.data_expiracao_plano.strftime("%d/%m/%Y")
    else:
        mensagem= "Ainda não ativou nenhum plano"
    prognostico = session.query(Prognostico).filter(Prognostico.plano == "VIP").all()
    return{
        "Total":len(prognostico),
        "VIP":prognostico,
        "mensagem":mensagem
    }