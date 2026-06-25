from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class DrillLog(BaseModel):
    name: str
    reps: Optional[int] = None
    duration_mins: Optional[int] = None
    notes: Optional[str] = None

class SessionCreate(BaseModel):
    session_date: datetime
    duration_mins: int
    focus_area: str          # serve / return / groundstrokes / net / fitness / match_play
    intensity: str = "medium"
    drills: Optional[List[DrillLog]] = None
    performance_rating: Optional[int] = None   # 1-10
    balls_hit: Optional[int] = None
    distance_km: Optional[float] = None
    notes: Optional[str] = None

class SessionResponse(BaseModel):
    id: int
    user_id: int
    session_date: datetime
    duration_mins: int
    focus_area: str
    intensity: str
    drills: Optional[List[Dict[str, Any]]]
    performance_rating: Optional[int]
    balls_hit: Optional[int]
    distance_km: Optional[float]
    ai_tip: Optional[str]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
