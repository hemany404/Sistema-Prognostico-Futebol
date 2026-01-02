from fastapi import Depends,HTTPException
from sqlalchemy.orm import sessionmaker, session
from models.modelos import db,Usuario
from main import ALGORITHM,SECRETY_KEY,oauth2_schema
from jose import jwt,JWTError
from datetime import datetime,timezone
 

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session

    finally:
        session.close()

def verificar_usuario(token: str = Depends(oauth2_schema), session: session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token,SECRETY_KEY,ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:    
        raise HTTPException(status_code=401, detail="acesso negado,verifica a data do token")
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise  HTTPException(status_code=401,detail="usuario não encontrado")
    return usuario

def verificar_expiracao(usuario,session):
    if usuario.data_expiracao_plano and usuario.data_expiracao_plano.tzinfo is None:
        usuario.data_expiracao_plano = usuario.data_expiracao_plano.replace(tzinfo=timezone.utc)
    if usuario.data_expiracao_plano < datetime.now(timezone.utc):
        usuario.plano = "GRÁTIS"
        usuario.status_pagamento = "EXPIRADO"
        usuario.data_expiracao_plano = None
        session.commit()
    if usuario.data_expiracao_plano :
        mensagem ="o seu plano expira em:" + usuario.data_expiracao_plano.strftime("%d/%m/%Y")
    else:
        mensagem= "Ainda não ativou nenhum plano"
        return {
            "Seu plano expirou. Faça pagamento para continuar."
        }
    return mensagem