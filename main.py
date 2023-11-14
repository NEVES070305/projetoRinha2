from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from datetime import date
import uuid


app = FastAPI()
DB_URL = 'postgresql://user_root:pass_root@db:5433/postgres'  

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Pessoa(BaseModel):
    apelido: str
    nome: str
    nascimento: date
    stack: List[str] = []

    @validator('stack', each_item=True)
    def validate_stack_item_length(cls, stack_item):
        if len(stack_item) > 32:
            raise ValueError('Stack item length should not exceed 32 characters')
        return stack_item
    
    @validator('nome')
    def validate_nome_length(cls, nome):
        if not nome:
            raise ValueError('O campo "nome" é obrigatório')
        if len(nome) > 100:
            raise ValueError('O campo "nome" deve ter no máximo 100 caracteres')
        return nome
    
    @validator('apelido')
    def validate_apelido(cls, apelido):
        if not apelido:
            raise ValueError('O campo "apelido" é obrigatório')
        if len(apelido) > 32:
            raise ValueError('O campo "apelido" deve ter no máximo 32 caracteres')
        return apelido
    
    @validator('nascimento')
    def validate_date_format(cls, nascimento):
        try:
            # Tenta converter a string em um objeto de data no formato "AAAA-MM-DD"
            date.fromisoformat(nascimento)
        except ValueError:
            raise ValueError('O campo "nascimento" deve estar no formato "AAAA-MM-DD"')

        return nascimento
    
Base = declarative_base()

class PessoaDB(Base):
    __tablename__ = "pessoas"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4))  # Use String para UUID
    apelido = Column(String, index=True)
    nome = Column(String)
    nascimento = Column(Date)
    stack = Column(String)

# Crie as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

class RespostaPessoa(BaseModel):
    message: str
    pessoa: Pessoa

# POST endpoint to create a Pessoa
@app.post("/pessoas", response_model=RespostaPessoa, status_code=201)
def criar_pessoa(pessoa:Pessoa):
    try:
        if any(len(item) > 32 for item in pessoa.stack):
            raise HTTPException(status_code=442, detail="Unprocessable Entity/Content")
        db_pessoa = PessoaDB(**pessoa.dict())
        with SessionLocal() as session:
            session.add(db_pessoa)
            session.commit()
            session.refresh(db_pessoa)
        location_url = f"/pessoas/{db_pessoa.id}"
        response_headers = {"Location": location_url}

        response_body = {"message":"Pessoa criada com sucesso", "pessoa": db_pessoa}
        return response_body, response_headers 
    except:
        raise HTTPException(status_code=442, detail="Unprocessable Entity/Content")

@app.get("/pessoas/{pessoa_id}", response_model=RespostaPessoa)
def pegar_pessoa(pessoa_id: uuid.UUID):
    try:
        with SessionLocal() as session:
            db_pessoa = session.query(PessoaDB).filter(PessoaDB.id==pessoa_id).first()
            if db_pessoa is None:
                raise HTTPException(status_code=404, detail="Pessoa not found")
            return db_pessoa
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")