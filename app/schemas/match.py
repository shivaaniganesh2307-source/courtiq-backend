from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class MatchCreate(BaseModel):
    opponent_name: Optional[str] = None
    match_date: datetime
    surface: str = "hard"
    match_format: str = "best_of_3"
    tournament_name: Optional[str] = None
    location: Optional[str] = None
    result: str                         # "win" or "loss"
    score: Optional[str] = None

    # Serve
    first_serve_in: int = 0
    first_serve_total: int = 0
    second_serve_in: int = 0
    second_serve_total: int = 0
    aces: int = 0
    double_faults: int = 0
    avg_first_serve_speed: Optional[float] = None
    avg_second_serve_speed: Optional[float] = None

    # Return
    first_return_winners: int = 0
    second_return_winners: int = 0
    return_errors: int = 0

    # Rally
    winners: int = 0
    unforced_errors: int = 0
    forced_errors: int = 0
    avg_rally_length: Optional[float] = None
    longest_rally: Optional[int] = None

    # Net
    net_approaches: int = 0
    net_points_won: int = 0

    # Breakpoints
    break_points_won: int = 0
    break_points_faced: int = 0
    break_points_saved: int = 0

    shot_distribution: Optional[Dict[str, int]] = None
    notes: Optional[str] = None

class MatchUpdate(BaseModel):
    notes: Optional[str] = None
    score: Optional[str] = None

class MatchResponse(BaseModel):
    id: int
    user_id: int
    opponent_name: Optional[str]
    match_date: datetime
    surface: str
    result: str
    score: Optional[str]
    aces: int
    double_faults: int
    winners: int
    unforced_errors: int
    first_serve_in: int
    first_serve_total: int
    ai_analysis: Optional[str]
    ai_analysis_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime

    # Computed fields returned by API
    first_serve_pct: Optional[float] = None
    winner_error_ratio: Optional[float] = None

    class Config:
        from_attributes = True
