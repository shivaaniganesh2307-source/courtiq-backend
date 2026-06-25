from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.models.match import Match
from app.models.user import User
from app.schemas.match import MatchCreate, MatchUpdate, MatchResponse
from app.core.security import get_current_user
from app.services.ai_service import analyze_match

router = APIRouter(prefix="/api/matches", tags=["matches"])

def build_response(match: Match) -> MatchResponse:
    resp = MatchResponse.model_validate(match)
    if match.first_serve_total > 0:
        resp.first_serve_pct = round((match.first_serve_in / match.first_serve_total) * 100, 1)
    if match.unforced_errors > 0:
        resp.winner_error_ratio = round(match.winners / match.unforced_errors, 2)
    return resp

async def run_ai_analysis(match_id: int, user_id: int):
    """Background task — runs after match is saved so the user isn't waiting."""
    from app.db.database import SessionLocal
    db = SessionLocal()
    try:
        match = db.query(Match).filter(Match.id == match_id).first()
        user = db.query(User).filter(User.id == user_id).first()
        if match and user:
            analysis = await analyze_match(match, user)
            match.ai_analysis = analysis
            match.ai_analysis_at = datetime.utcnow()
            db.commit()
    except Exception as e:
        print(f"AI analysis failed for match {match_id}: {e}")
    finally:
        db.close()


@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def create_match(
    payload: MatchCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    match = Match(**payload.model_dump(), user_id=current_user.id)
    db.add(match)
    db.commit()
    db.refresh(match)

    # Kick off AI analysis in background — user gets match saved immediately
    if current_user.id:
        background_tasks.add_task(run_ai_analysis, match.id, current_user.id)

    return build_response(match)


@router.get("/", response_model=List[MatchResponse])
def get_matches(
    skip: int = 0,
    limit: int = 20,
    result: str = None,
    surface: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Match).filter(Match.user_id == current_user.id)
    if result:
        query = query.filter(Match.result == result)
    if surface:
        query = query.filter(Match.surface == surface)
    matches = query.order_by(desc(Match.match_date)).offset(skip).limit(limit).all()
    return [build_response(m) for m in matches]


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    match = db.query(Match).filter(Match.id == match_id, Match.user_id == current_user.id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return build_response(match)


@router.patch("/{match_id}", response_model=MatchResponse)
def update_match(
    match_id: int,
    payload: MatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    match = db.query(Match).filter(Match.id == match_id, Match.user_id == current_user.id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(match, field, value)
    db.commit()
    db.refresh(match)
    return build_response(match)


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    match = db.query(Match).filter(Match.id == match_id, Match.user_id == current_user.id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    db.delete(match)
    db.commit()


@router.post("/{match_id}/analyze", response_model=MatchResponse)
async def trigger_analysis(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Manually trigger AI analysis on a match — useful if background task failed."""
    match = db.query(Match).filter(Match.id == match_id, Match.user_id == current_user.id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    analysis = await analyze_match(match, current_user)
    match.ai_analysis = analysis
    match.ai_analysis_at = datetime.utcnow()
    db.commit()
    db.refresh(match)
    return build_response(match)
