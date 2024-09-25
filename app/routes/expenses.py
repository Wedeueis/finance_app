from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models import ExpenseType, Expense
from app.routes import router

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    type: ExpenseType
    date: datetime

class ExpenseUpdate(BaseModel):
    amount: float = None
    description: str = None
    type: ExpenseType = None
    date: datetime = None

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: str
    type: ExpenseType
    date: datetime

    class Config:
        orm_mode = True

@router.post("/expenses/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    controller = ExpenseController(db)
    return controller.create_expense(expense.dict())

@router.get("/expenses/", response_model=List[ExpenseResponse])
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    controller = ExpenseController(db)
    return controller.get_all_expenses(skip, limit)

@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    controller = ExpenseController(db)
    return controller.get_expense(expense_id)

@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    controller = ExpenseController(db)
    return controller.update_expense(expense_id, expense.dict(exclude_unset=True))

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    controller = ExpenseController(db)
    return controller.delete_expense(expense_id)

class ExpenseService:
    def __init__(self, db: Session):
        self.repository = ExpenseRepository()
        self.db = db

    def create_expense(self, expense_data: dict):
        expense = Expense(**expense_data)
        return self.repository.create(self.db, expense)

    def get_all_expenses(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(self.db, skip, limit)

    def get_expense(self, expense_id: int):
        return self.repository.get_by_id(self.db, expense_id)

    def update_expense(self, expense_id: int, expense_data: dict):
        return self.repository.update(self.db, expense_id, expense_data)

    def delete_expense(self, expense_id: int):
        return self.repository.delete(self.db, expense_id)

class ExpenseController:
    def __init__(self, db: Session):
        self.service = ExpenseService(db)

    def create_expense(self, expense_data: dict):
        return self.service.create_expense(expense_data)

    def get_all_expenses(self, skip: int = 0, limit: int = 100):
        return self.service.get_all_expenses(skip, limit)

    def get_expense(self, expense_id: int):
        expense = self.service.get_expense(expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense

    def update_expense(self, expense_id: int, expense_data: dict):
        updated_expense = self.service.update_expense(expense_id, expense_data)
        if not updated_expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return updated_expense

    def delete_expense(self, expense_id: int):
        deleted_expense = self.service.delete_expense(expense_id)
        if not deleted_expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return {"message": "Expense deleted successfully"}
    
class ExpenseRepository:
    @staticmethod
    def create(db: Session, expense: Expense):
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Expense).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, expense_id: int):
        return db.query(Expense).filter(Expense.id == expense_id).first()

    @staticmethod
    def update(db: Session, expense_id: int, expense_data: dict):
        db.query(Expense).filter(Expense.id == expense_id).update(expense_data)
        db.commit()
        return db.query(Expense).filter(Expense.id == expense_id).first()

    @staticmethod
    def delete(db: Session, expense_id: int):
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if expense:
            db.delete(expense)
            db.commit()
        return expense