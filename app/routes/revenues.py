from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models import RevenueType, Revenue
from app.routes import router

class RevenueCreate(BaseModel):
    amount: float
    description: str
    type: RevenueType
    date: datetime

class RevenueUpdate(BaseModel):
    amount: float = None
    description: str = None
    type: RevenueType = None
    date: datetime = None

class RevenueResponse(BaseModel):
    id: int
    amount: float
    description: str
    type: RevenueType
    date: datetime

    class Config:
        orm_mode = True

@router.post("/revenues/", response_model=RevenueResponse)
def create_revenue(revenue: RevenueCreate, db: Session = Depends(get_db)):
    controller = RevenueController(db)
    return controller.create_revenue(revenue.dict())

@router.get("/revenues/", response_model=List[RevenueResponse])
def read_revenues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    controller = RevenueController(db)
    return controller.get_all_revenues(skip, limit)

@router.get("/revenues/{revenue_id}", response_model=RevenueResponse)
def read_revenue(revenue_id: int, db: Session = Depends(get_db)):
    controller = RevenueController(db)
    return controller.get_revenue(revenue_id)

@router.put("/revenues/{revenue_id}", response_model=RevenueResponse)
def update_revenue(revenue_id: int, revenue: RevenueUpdate, db: Session = Depends(get_db)):
    controller = RevenueController(db)
    return controller.update_revenue(revenue_id, revenue.dict(exclude_unset=True))

@router.delete("/revenues/{revenue_id}")
def delete_revenue(revenue_id: int, db: Session = Depends(get_db)):
    controller = RevenueController(db)
    return controller.delete_revenue(revenue_id)

class RevenueController:
    def __init__(self, db: Session):
        self.service = RevenueService(db)

    def create_revenue(self, revenue_data: dict):
        return self.service.create_revenue(revenue_data)

    def get_all_revenues(self, skip: int = 0, limit: int = 100):
        return self.service.get_all_revenues(skip, limit)

    def get_revenue(self, revenue_id: int):
        revenue = self.service.get_revenue(revenue_id)
        if not revenue:
            raise HTTPException(status_code=404, detail="Revenue not found")
        return revenue

    def update_revenue(self, revenue_id: int, revenue_data: dict):
        updated_revenue = self.service.update_revenue(revenue_id, revenue_data)
        if not updated_revenue:
            raise HTTPException(status_code=404, detail="Revenue not found")
        return updated_revenue

    def delete_revenue(self, revenue_id: int):
        deleted_revenue = self.service.delete_revenue(revenue_id)
        if not deleted_revenue:
            raise HTTPException(status_code=404, detail="Revenue not found")
        return {"message": "Revenue deleted successfully"}

class RevenueService:
    def __init__(self, db: Session):
        self.repository = RevenueRepository()
        self.db = db

    def create_revenue(self, revenue_data: dict):
        revenue = Revenue(**revenue_data)
        return self.repository.create(self.db, revenue)

    def get_all_revenues(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(self.db, skip, limit)

    def get_revenue(self, revenue_id: int):
        return self.repository.get_by_id(self.db, revenue_id)

    def update_revenue(self, revenue_id: int, revenue_data: dict):
        return self.repository.update(self.db, revenue_id, revenue_data)

    def delete_revenue(self, revenue_id: int):
        return self.repository.delete(self.db, revenue_id)
    
class RevenueRepository:
    @staticmethod
    def create(db: Session, revenue: Revenue):
        db.add(revenue)
        db.commit()
        db.refresh(revenue)
        return revenue

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Revenue).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, revenue_id: int):
        return db.query(Revenue).filter(Revenue.id == revenue_id).first()

    @staticmethod
    def update(db: Session, revenue_id: int, revenue_data: dict):
        db.query(Revenue).filter(Revenue.id == revenue_id).update(revenue_data)
        db.commit()
        return db.query(Revenue).filter(Revenue.id == revenue_id).first()

    @staticmethod
    def delete(db: Session, revenue_id: int):
        revenue = db.query(Revenue).filter(Revenue.id == revenue_id).first()
        if revenue:
            db.delete(revenue)
            db.commit()
        return revenue