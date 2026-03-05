from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat_routes import router as chat_router
from app.routes.voice_routes import router as voice_router
from app.routes.tts_routes import router as tts_router

app = FastAPI(title="TrustGov AI")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat")
app.include_router(voice_router, prefix="/voice")
app.include_router(tts_router, prefix="/tts")

@app.get("/")
def root():
    return {"status": "online", "message": "TrustGov AI API is running"}