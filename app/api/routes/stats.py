from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from app.db.database import get_db
from app.models.match import Match
from app.models.session_video import TrainingSession
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/api/stats", tags=["stats"])

@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """High-level stats for the dashboard — win rate, averages, trends."""
    matches = db.query(Match).filter(Match.user_id == current_user.id).all()
    sessions = db.query(TrainingSession).filter(TrainingSession.user_id == current_user.id).all()

    if not matches:
        return {"message": "No matches recorded yet", "matches": 0}

    wins = sum(1 for m in matches if m.result == "win")
    total = len(matches)

    total_aces = sum(m.aces for m in matches)
    total_dfs = sum(m.double_faults for m in matches)
    total_winners = sum(m.winners for m in matches)
    total_ue = sum(m.unforced_errors for m in matches)

    first_serve_in = sum(m.first_serve_in for m in matches)
    first_serve_total = sum(m.first_serve_total for m in matches)

    surface_wins = {}
    for m in matches:
        if m.surface not in surface_wins:
            surface_wins[m.surface] = {"wins": 0, "total": 0}
        surface_wins[m.surface]["total"] += 1
        if m.result == "win":
            surface_wins[m.surface]["wins"] += 1

    recent_5 = sorted(matches, key=lambda m: m.match_date, reverse=True)[:5]

    return {
        "total_matches": total,
        "wins": wins,
        "losses": total - wins,
        "win_rate": round((wins / total) * 100, 1) if total else 0,
        "total_training_sessions": len(sessions),
        "total_training_hours": round(sum(s.duration_mins for s in sessions) / 60, 1),
        "avg_aces_per_match": round(total_aces / total, 1),
        "avg_double_faults_per_match": round(total_dfs / total, 1),
        "avg_winners_per_match": round(total_winners / total, 1),
        "avg_unforced_errors_per_match": round(total_ue / total, 1),
        "overall_winner_error_ratio": round(total_winners / total_ue, 2) if total_ue else 0,
        "overall_first_serve_pct": round((first_serve_in / first_serve_total) * 100, 1) if first_serve_total else 0,
        "win_rate_by_surface": {
            s: round((v["wins"] / v["total"]) * 100, 1)
            for s, v in surface_wins.items()
        },
        "recent_results": [
            {"id": m.id, "date": m.match_date, "opponent": m.opponent_name, "result": m.result, "score": m.score}
            for m in recent_5
        ]
    }


@router.get("/trends")
def get_trends(
    last_n: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Match-by-match trend data for charts — unforced errors, winners, serve % over time."""
    matches = (
        db.query(Match)
        .filter(Match.user_id == current_user.id)
        .order_by(Match.match_date)
        .limit(last_n)
        .all()
    )

    return {
        "matches": [
            {
                "id": m.id,
                "date": m.match_date,
                "result": m.result,
                "aces": m.aces,
                "double_faults": m.double_faults,
                "winners": m.winners,
                "unforced_errors": m.unforced_errors,
                "first_serve_pct": round((m.first_serve_in / m.first_serve_total) * 100, 1) if m.first_serve_total else None,
                "winner_error_ratio": round(m.winners / m.unforced_errors, 2) if m.unforced_errors else None,
            }
            for m in matches
        ]
    }
