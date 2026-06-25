from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False)

    session_date    = Column(DateTime(timezone=True), nullable=False)
    duration_mins   = Column(Integer, nullable=False)          # minutes
    focus_area      = Column(String, nullable=False)           # serve / return / groundstrokes / net / fitness / match_play
    intensity       = Column(String, default="medium")         # low / medium / high

    # Drills logged (JSON array: [{"name": "cross-court rally", "reps": 50, "notes": "..."}])
    drills          = Column(JSON, nullable=True)

    # Self-rated performance (1-10)
    performance_rating = Column(Integer, nullable=True)

    # Physical metrics
    balls_hit       = Column(Integer, nullable=True)
    distance_km     = Column(Float, nullable=True)

    # AI coaching tip for this session
    ai_tip          = Column(Text, nullable=True)

    notes           = Column(Text, nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    user            = relationship("User", back_populates="sessions")


class Video(Base):
    __tablename__ = "videos"

    id              = Column(Integer, primary_key=True, index=True)
    match_id        = Column(Integer, ForeignKey("matches.id"), nullable=False)

    s3_key          = Column(String, nullable=False)           # AWS S3 object key
    original_name   = Column(String, nullable=True)
    duration_secs   = Column(Integer, nullable=True)
    file_size_mb    = Column(Float, nullable=True)
    status          = Column(String, default="uploaded")       # uploaded / processing / analyzed / failed

    # OpenCV/MediaPipe analysis results
    analysis_results = Column(JSON, nullable=True)
    # e.g. {"shots_detected": 42, "avg_swing_speed": 85, "movement_heatmap": [...], "posture_score": 7.2}

    analyzed_at     = Column(DateTime(timezone=True), nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    match           = relationship("Match", back_populates="videos")
