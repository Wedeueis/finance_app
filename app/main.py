from enum import Enum

from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router

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


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance API", 
              description="API for managing personal expenses", 
              version="1.0.0")

app.include_router(router, prefix="/api/v1", tags=["expenses"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)