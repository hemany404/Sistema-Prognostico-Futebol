from fastapi import APIRouter, Depends, HTTPException,BackgroundTasks
from sqlalchemy.orm import session
from models.modelos import Usuario
from dependecias import pegar_sessao,verificar_usuario
from jose import jwt,JWTError
from schema.schemas import UsuarioSchema,LoginSchema
from main import bcrypt_context,SECRETY_KEY,ALGORITHM,ACESS_TOKEN_MINUTO_EXPIRACAO
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordRequestForm
from utils.email import enviar_mensagem

auth_roteador = APIRouter(prefix="/auth", tags=["autenticação"])

def criar_token(id_usuario: int, duracao_token = timedelta(minutes=ACESS_TOKEN_MINUTO_EXPIRACAO)):
    data_expircao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub":str(id_usuario), "expiracao": str(data_expircao)}
    jwt_codificado = jwt.encode(dic_info,SECRETY_KEY,ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email,senha,session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha,usuario.senha):
        return False
    return usuario

@auth_roteador.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema,background_tasks:BackgroundTasks, session: session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario:
        raise HTTPException(status_code=400,detail="este email já está cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome,usuario_schema.email,senha_criptografada, usuario_schema.admin, usuario_schema.plano)
        session.add(novo_usuario)
        session.commit()
        background_tasks.add_task(enviar_mensagem,email=novo_usuario.email,nome=novo_usuario.nome)
        return{
            "mensagem":"usuario cadastrado com sucesso"
        }
    
@auth_roteador.post("/login")   
async def login(login_schema: LoginSchema, session: session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email,login_schema.senha,session)
    if not usuario:
        raise HTTPException(status_code=400,detail="usuario não encontrado ou cadastrado")
    
    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=30))                              
        return{
            "access_token":acess_token,
            "refresh_token":refresh_token,
            "token_type":"Bearer"
        }
    
@auth_roteador.post("/login-form")   
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username,dados_formulario.password,session)
    if not usuario:
        raise HTTPException(status_code=400,detail="usuario não encontrado ou cadastrado")
    
    else:
        acess_token = criar_token(usuario.id)
        return{
            "access_token":acess_token,
            "token_type":"Bearer"
        }    
    
@auth_roteador.post("/refresh_token")
async def utilizar_refresh_token(usuario: Usuario = Depends(verificar_usuario)):
    access_token = criar_token(usuario.id)
    return{
        "access": access_token,
        "token_type":"Bearer"
    }   





