from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


## Data Model

class Categoria(Enum):
    MORADIA = 'moradia'
    SAUDE = 'saude'
    BANCO = 'banco'
    ADA = 'ada'
    PESSOAL = 'pessoal'
    TRANSPORTE = 'transporte'
    DIVERSOS = 'diversos'
    EDUCACAO = 'educacao'
    LAZER = 'lazer'

class DespesaDataModel(BaseModel):
    dia: int
    mes: int
    ano: int
    categoria: str
    nome: str
    valor: float

app = FastAPI()

despesas ={
    0: DespesaDataModel(ano=2024, mes=9, dia=24, categoria=Categoria.PESSOAL, nome="IFOOD", valor=155),
    1: DespesaDataModel(ano=2024, mes=9, dia=24, categoria=Categoria.TRANSPORTE, nome="UBER", valor=44),
    2: DespesaDataModel(ano=2024, mes=9, dia=24, categoria=Categoria.MORADIA, nome="aluguel", valor=3500)
}

@app.get("/")
def index() -> dict[str, dict[int, DespesaDataModel]]:
    return {"despesas": despesas}

@app.get("/despesa/{despesa_id}")
def query_despesa_by_id(despesa_id: int) -> DespesaDataModel:
    if despesa_id not in despesas:
        raise HTTPException(
            status_code=404, detail=f"Despesa com {despesa_id=} não existe."
        )
    return despesas[despesa_id]