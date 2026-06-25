from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from app.db.database import get_db
from app.models.session_video import TrainingSession
from app.models.user import User
from app.schemas.session import SessionCreate, SessionResponse
from app.core.security import get_current_user
from app.services.ai_service import generate_session_tip

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

async def run_session_tip(session_id: int, user_id: int, session_data: dict):
    from app.db.database import SessionLocal
    db = SessionLocal()
    try:
        session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
        user = db.query(User).filter(User.id == user_id).first()
        if session and user:
            tip = await generate_session_tip(session_data, user)
            session.ai_tip = tip
            db.commit()
    except Exception as e:
        print(f"AI tip failed for session {session_id}: {e}")
    finally:
        db.close()


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: SessionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    drills_data = [d.model_dump() for d in payload.drills] if payload.drills else None
    session = TrainingSession(
        **payload.model_dump(exclude={"drills"}),
        drills=drills_data,
        user_id=current_user.id
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    background_tasks.add_task(run_session_tip, session.id, current_user.id, payload.model_dump())
    return session


@router.get("/", response_model=List[SessionResponse])
def get_sessions(
    skip: int = 0,
    limit: int = 20,
    focus_area: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(TrainingSession).filter(TrainingSession.user_id == current_user.id)
    if focus_area:
        query = query.filter(TrainingSession.focus_area == focus_area)
    return query.order_by(desc(TrainingSession.session_date)).offset(skip).limit(limit).all()


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(TrainingSession).filter(
        TrainingSession.id == session_id,
        TrainingSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(TrainingSession).filter(
        TrainingSession.id == session_id,
        TrainingSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
