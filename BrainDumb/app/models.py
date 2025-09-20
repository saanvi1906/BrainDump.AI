from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from .database import Base

class Dump(Base):
    __tablename__ = "dumps"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    tags = Column(String(255))  
    stress_score = Column(Float)
    action_plan = Column(Text)
    wellness_tip = Column(Text)
    motivation = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
