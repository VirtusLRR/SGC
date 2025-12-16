from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database.database import get_db
from models import Bot
from services.graph.graph import graph
from repositories import BotRepository
from schemas import BotRequest, BotResponse
from datetime import datetime
import uuid

class BotController:
    @staticmethod
    async def process_message(request: BotRequest, db: Session = Depends(get_db)):
        user_msg = request.user_message.strip()
        if request.thread_id is not None:
            thread_id = request.thread_id
        else:
            thread_id = str(uuid.uuid4())

        response = graph.invoke({'user_input': user_msg}, {"configurable": {"thread_id": str(thread_id)}})
        final_answer = response.get("final_answer")

        if isinstance(final_answer, list) and len(final_answer) > 0:
            ai_message = final_answer[0].get("text", str(final_answer))
        elif isinstance(final_answer, str):
            ai_message = final_answer
        else:
            ai_message = str(final_answer)

        create_at = response.get("create_at", datetime.now())

        message = BotRepository.save(db, Bot(
            thread_id=thread_id,
            user_message=user_msg,
            ai_message=ai_message,
            create_at=create_at
        ))
        return BotResponse.model_validate(message)

    @staticmethod
    def get_all_messages(db: Session = Depends(get_db)):
        messages = BotRepository.get_messages(db)
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sem mensagens encontradas."
            )
        return [BotResponse.model_validate(message) for message in messages]