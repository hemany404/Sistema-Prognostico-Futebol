from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
SECRETY_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_MINUTO_EXPIRACAO = int(os.getenv("ACESS_TOKEN_MINUTO_EXPIRACAO"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated= "auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from routers.auth_rotas import auth_roteador
from routers.planos_rotas import planos_roteador
from routers.usuario_rotas import usuario_roteador
from routers.prognosticos_rotas import prognosticos_roteador


app.include_router(auth_roteador)
app.include_router(planos_roteador)
app.include_router(usuario_roteador)
app.include_router(prognosticos_roteador)


