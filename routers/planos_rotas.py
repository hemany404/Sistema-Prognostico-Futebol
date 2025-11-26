from fastapi import APIRouter,Depends, HTTPException
from dependecias import pegar_sessao,verificar_usuario
from models.modelos import Planos,Usuario
from sqlalchemy.orm import session
from schema.schemas import PlanoSchema


planos_roteador = APIRouter(prefix="/plano", tags=["planos"])

@planos_roteador.post("/criar_planos")
async def criar_planos(plano_schema: PlanoSchema, session: session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_usuario)):
    plano = session.query(Planos).filter(Planos.nome == plano_schema.nome).first()

    if plano:
        raise HTTPException(status_code=400, detail=" este plano já foi cadastrado")
    
    elif not usuario.admin:
        raise HTTPException(status_code=401,detail="voce não tem autorizacao")
    else:
        novo_plano = Planos(plano_schema.nome,plano_schema.preco,plano_schema.duracao)
        session.add(novo_plano)
        session.commit()
        return{
            "mensagem":"plano criado com sucesso"
        }
@planos_roteador.get("/listar_planos")
async def listar_planos(session:session = Depends(pegar_sessao)):
    planos = session.query(Planos).all() 
    return{
        "numero de plano":len(planos),
        "planos":planos
    }   

