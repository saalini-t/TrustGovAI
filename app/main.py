from fastapi import FastAPI
from app.routes.chat_routes import router as chat_router
from app.routes.voice_routes import router as voice_router

app = FastAPI(title="TrustGov AI")

app.include_router(chat_router, prefix="/chat")
app.include_router(voice_router, prefix="/voice")