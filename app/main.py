from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, matches, sessions, stats
from app.db.database import Base, engine
import app.models.user
import app.models.match
import app.models.session_video

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tennis Analyzer API",
    description="AI-powered tennis performance analysis backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8081", "https://courtiq-frontend-bd1uzyzc9-shivaaniganesh2307-8957s-projects.vercel.app/"] # React web + Expo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(matches.router)
app.include_router(sessions.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {"message": "Tennis Analyzer API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
