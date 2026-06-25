from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name       = Column(String, nullable=False)
    skill_level     = Column(String, default="intermediate")  # beginner / intermediate / advanced / pro
    dominant_hand   = Column(String, default="right")         # right / left
    play_style      = Column(String, default="baseline")      # baseline / serve-volley / all-court
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    updated_at      = Column(DateTime(timezone=True), onupdate=func.now())

    matches         = relationship("Match", back_populates="user", cascade="all, delete-orphan")
    sessions        = relationship("TrainingSession", back_populates="user", cascade="all, delete-orphan")
