from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Match(Base):
    __tablename__ = "matches"

    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Match info
    opponent_name       = Column(String, nullable=True)
    match_date          = Column(DateTime(timezone=True), nullable=False)
    surface             = Column(String, default="hard")       # hard / clay / grass / indoor
    match_format        = Column(String, default="best_of_3")  # best_of_3 / best_of_5 / pro_set
    tournament_name     = Column(String, nullable=True)
    location            = Column(String, nullable=True)

    # Result
    result              = Column(String, nullable=False)        # win / loss
    score               = Column(String, nullable=True)         # e.g. "6-3 4-6 6-2"

    # Serve stats
    first_serve_in      = Column(Integer, default=0)
    first_serve_total   = Column(Integer, default=0)
    second_serve_in     = Column(Integer, default=0)
    second_serve_total  = Column(Integer, default=0)
    aces                = Column(Integer, default=0)
    double_faults       = Column(Integer, default=0)
    avg_first_serve_speed  = Column(Float, nullable=True)       # mph
    avg_second_serve_speed = Column(Float, nullable=True)

    # Return stats
    first_return_winners  = Column(Integer, default=0)
    second_return_winners = Column(Integer, default=0)
    return_errors         = Column(Integer, default=0)

    # Rally stats
    winners             = Column(Integer, default=0)
    unforced_errors     = Column(Integer, default=0)
    forced_errors       = Column(Integer, default=0)
    avg_rally_length    = Column(Float, nullable=True)
    longest_rally       = Column(Integer, nullable=True)

    # Net stats
    net_approaches      = Column(Integer, default=0)
    net_points_won      = Column(Integer, default=0)

    # Breakpoints
    break_points_won    = Column(Integer, default=0)
    break_points_faced  = Column(Integer, default=0)
    break_points_saved  = Column(Integer, default=0)

    # Shot distribution (JSON: {"forehand": 45, "backhand": 30, "slice": 15, "volley": 10})
    shot_distribution   = Column(JSON, nullable=True)

    # AI analysis
    ai_analysis         = Column(Text, nullable=True)
    ai_analysis_at      = Column(DateTime(timezone=True), nullable=True)

    # Notes
    notes               = Column(Text, nullable=True)

    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    updated_at          = Column(DateTime(timezone=True), onupdate=func.now())

    user                = relationship("User", back_populates="matches")
    videos              = relationship("Video", back_populates="match", cascade="all, delete-orphan")
