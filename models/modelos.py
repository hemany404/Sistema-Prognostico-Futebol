from sqlalchemy import create_engine,Column,DateTime, Integer, String,Float, Boolean, ForeignKey   
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
from sqlalchemy.sql import func

db = create_engine("sqlite:///banco.db")

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    nome = Column("nome",String,nullable=False)
    email = Column("email",String, nullable= False,unique=True)
    senha = Column("senha",String,nullable=False)
    admin = Column("admin",Boolean,default=False)   
    plano = Column("plano",String)
    data_expiracao_plano = Column("data_expiracao_plano", DateTime(timezone=True), nullable=True)
    status_pagamento = Column("status_pagamento",String, default="PENDENTE")
    criado_em = Column("criado_em", DateTime, default=datetime.now())


    def __init__(self, nome, email, senha, admin = False, plano="GRÁTIS", status_pagamento="PENDENTE", criado_em =None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin
        self.plano = plano
        self.status_pagamento = status_pagamento
        self.criado_em = criado_em or datetime.now()
        

class Prognostico(Base):
    __tablename__ = "prognosticos"

    id = Column("id",Integer, primary_key=True, autoincrement=True) 
    equipa_casa = Column("equipa_casa",String,nullable=False)
    equipa_fora = Column("equipa_fora",String,nullable=False)
    previsao = Column("previsao",String, nullable=False)
    data_jogo = Column("data_jogo",DateTime,nullable=False)
    plano = Column("plano",String)
    criado_em = Column("criado_em",DateTime, default = datetime.now(timezone.utc))
    prognosticos_status = Column("prognosticos_status", String, default="ATIVO")

    def __init__(self,equipa_casa, equipa_fora, previsao,data_jogo, plano = "GRÁTIS",  criado_em = datetime.now(timezone.utc), prognosticos_status = "ATIVO",):
        self.equipa_casa = equipa_casa
        self.equipa_fora = equipa_fora
        self.previsao = previsao
        self.data_jogo = data_jogo
        self.plano = plano
        self.criado_em = criado_em
        self.prognosticos_status = prognosticos_status
        

class Planos(Base):
    __tablename__ = "planos"

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    nome = Column(String, unique=True)
    preco = Column("preco",Float)    
    duracao = Column("duracao",Integer)

    def __init__ (self,nome, preco,duracao):
        self.nome = nome
        self.preco = preco
        self.duracao = duracao     