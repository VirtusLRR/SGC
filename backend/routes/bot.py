from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from controllers import BotController
from schemas import BotResponse, BotRequest
from database.database import get_db

bot_routes = APIRouter()

@bot_routes.post("/bot/message", response_model=BotResponse, status_code=status.HTTP_200_OK)
async def process_bot_message(request: BotRequest, db: Session = Depends(get_db)):
    return await BotController.process_message(request, db)

@bot_routes.get("/bot/history", response_model=list[BotResponse], status_code=status.HTTP_200_OK)
def get_bot_messages(db: Session = Depends(get_db)):
    return BotController.get_all_messages(db)

@bot_routes.post("/bot/image_message", response_model=BotResponse, status_code=status.HTTP_200_OK)
async def process_image_message(request: BotRequest, db: Session = Depends(get_db)):
    return await BotController.process_image_message(request, db)

@bot_routes.post("/bot/audio_message", response_model=BotResponse, status_code=status.HTTP_200_OK)
async def process_audio_message(request: BotRequest, db: Session = Depends(get_db)):
    return await BotController.process_audio_message(request, db)