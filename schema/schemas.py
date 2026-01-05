from pydantic import BaseModel
from typing import Optional
from enum import Enum
from fastapi import Path
from datetime import datetime

class UsuarioSchema(BaseModel):
    nome: str = Path(...,min_length=3,max_length=10)
    email: str
    senha: str
    admin: Optional[bool]
    plano: str = "GRÁTIS"
    

    class config:
        from_attributes = True

class PlanoSchema(BaseModel):
    nome: str =Path(...,min_length=3,max_length=10)
    preco: float
    duracao: int    

    class config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class config:
        from_attributes = True

class PlanoPrognosticoEnum(str, Enum):
    GRÁTIS = "GRÁTIS"
    PREMIUM = "PREMIUM"
    VIP = "VIP"

class PlanoPagarEnum(str, Enum):
    PREMIUM = "PREMIUM"
    VIP = "VIP"

class PrognosticoSchema(BaseModel):
    equipa_casa: str
    equipa_fora:str
    previsao: str
    data_jogo: datetime
    plano: PlanoPrognosticoEnum
    mensagem:str
    
    class config:
        from_attributes = True
class PagarPlanoSchema(BaseModel):
    plano: PlanoPagarEnum

    class config:
        from_attributes = True 
class  EditarSchema(BaseModel):
    equipa_casa: Optional[str] = None
    equipa_fora:Optional[str] = None
    previsao: Optional[str]=None
    data_jogo: Optional[datetime]=None
    plano: Optional[PlanoPrognosticoEnum]=None
    prognosticos_status: Optional[str] =None

    class config:
        from_attributes = True

class RespostaInfoSchema(BaseModel):
    nome: str
    email: str
    plano: str
    status_pagamento:str
  
    class config:
        from_attributes = True

class RespostaUsuarioSchema(BaseModel):
    usuario: RespostaInfoSchema
    mensagem: str
  
    class config:
        from_attributes = True        
    

