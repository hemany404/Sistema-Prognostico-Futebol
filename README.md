Sobre o Projeto

Este é um sistema em desenvolvimento que permite gerenciar prognósticos esportivos (grátis,premium e vip), com autenticação, controle de assinaturas e expiração automática de planos.


Funcionalidades
 Usuários:

Criar conta e fazer login (JWT)

Acessar prognósticos conforme o plano (Grátis / Premium)

Ver plano ativo e data de expiração

Atualização automática do status quando o plano expira

 Planos:

Admin pode criar planos

Usuário pode pagar e ativar plano válido por 30 dias

Bloqueio automático após expiração

 Prognósticos:

Criar, editar e excluir prognósticos (somente admin)

Prognósticos gratuitos visíveis para todos

Prognósticos premium e vip visíveis apenas para assinantes ativos


Arquitetura do Sistema:

📁 Estrutura baseada em boas práticas com:

Routers

Schemas

Models

Interface da API (Swagger):

A documentação interativa está disponível em:

http://127.0.0.1:8000/docs

Tecnologias:

| Tecnologia | Finalidade        |
| ---------- | ----------------- |
| FastAPI    | Framework Backend |
| SQLAlchemy | ORM               |
| JWT        | Autenticação      |
| Sqlite     | Banco de dados    |
| Alembic    | Migrações         |
| Pydantic   | Validação         |

Estrutura do Projeto:

📁 projeto
 ┣ 📁 alembic
 ┣ 📁 models
 ┣ 📁 routers
 ┣ 📁 schema
 ┣ 📁 uploads
 ┣ 📄 main.py
 ┣ 📄 banco.db
 ┣ 📄 requirements.txt
 ┗ 📄 README.md

📄 Instalação e Setup:

1️⃣ Clonar o Repositório
git clone https://github.com/hemany404/Sistema-Prognostico-Futebol.git
cd seu-projeto

2️⃣ Criar Ambiente Virtual
python -m venv venv
venv\Scripts\activate    # Windows

3️⃣ Instalar Dependências
pip install -r requirements.txt

4️⃣ Configurar Variáveis .env
DATABASE_URL=sqlite:///nome_banco
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30 ou quanto tempo tu quiseres 


5️⃣ Rodar Migrações
alembic upgrade head

6️⃣ Iniciar o Servidor
uvicorn main:app --reload

Segurança Implementada

-Hash de senha
-Autenticação com JWT
-Verificação de expiração de sessão
-Niveis de acesso (Admin x Usuário)


