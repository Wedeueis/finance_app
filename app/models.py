from sqlalchemy import Column, Integer, Float, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class RevenueType(enum.Enum):
    SALARY = "salary"
    INVESTMENT = "investment"
    FREELANCE = "freelance"
    GIFT = "gift"
    OTHER = "other"

class Revenue(Base):
    __tablename__ = "revenues"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    type = Column(Enum(RevenueType))
    date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ExpenseType(enum.Enum):
    FOOD = "food"
    TRANSPORTATION = "transportation"
    HOUSING = "housing"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    OTHER = "other"

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    type = Column(Enum(ExpenseType))
    date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())