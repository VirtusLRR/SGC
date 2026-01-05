from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database.database import get_db
from models import Bot
from services.graph.graph import graph
from services.graph.agents.extractor import optical_extractor, audio_extractor
from repositories import BotRepository
from schemas import BotRequest, BotResponse
from datetime import datetime
import uuid
import base64
import binascii

class BotController:
    @staticmethod
    async def process_message(request: BotRequest, db: Session = Depends(get_db)):
        """Processa a mensagem do usuário, interage com o grafo e salva a resposta."""
        user_msg = request.user_message.strip()
        if request.thread_id is not None:
            thread_id = request.thread_id
        else:
            thread_id = str(uuid.uuid4())

        response = graph.invoke({'user_input': user_msg}, {"configurable": {"thread_id": str(thread_id)}})
        final_answer = response.get("final_answer")
        ai_message = parse_final_answer(final_answer)

        create_at = response.get("create_at", datetime.now())

        message = BotRepository.save(db, Bot(
            thread_id=thread_id,
            user_message=user_msg,
            ai_message=ai_message,
            create_at=create_at
        ))
        return BotResponse.model_validate(message)
        
    @staticmethod
    async def process_image_message(request: BotRequest, db: Session = Depends(get_db)):
        """
            Processa imagens enviadas pelo usuário, interage com o grafo e salva a resposta.
            Args:
                request: Corpo enviado pela requisição, precisa ter o atributo image_b64
        """
        if not request.image_b64 or is_valid_base64(request.image_b64):
            raise HTTPException(400, "Imagem inválida")

        image_b64 = request.image_b64
        if request.thread_id is not None:
            thread_id = request.thread_id
        else:
            thread_id = str(uuid.uuid4())

        extractor_response = optical_extractor(image_b64)
        extractor_answer = response.get("final_answer")
        extractor_message = parse_final_answer(extractor_answer)

        if ai_message != "": 
            response = graph.invoke({'user_input': extractor_message}, {"configurable": {"thread_id": str(thread_id)}})
            final_answer = response.get("final_answer")
            ai_message = parse_final_answer(final_answer)

            create_at = response.get("create_at", datetime.now())

            message = BotRepository.save(db, Bot(
                thread_id=thread_id,
                user_message=user_msg,
                ai_message=ai_message,
                create_at=create_at
            ))
            return BotResponse.model_validate(message)

        raise HTTPException(400, "Imagem inválida")
        
    @staticmethod
    async def process_audio_message(request: BotRequest, db: Session = Depends(get_db)):
        """
            Processa áudios enviados pelo usuário, interage com o grafo e salva a resposta.
            Args:
                request: Corpo enviado pela requisição, precisa ter o atributo audio_b64
        """
        if not request.audio_b64 or is_valid_base64(request.audio_b64):
            raise HTTPException(400, "Áudio inválido")

        audio_b64 = request.audio_b64
        if request.thread_id is not None:
            thread_id = request.thread_id
        else:
            thread_id = str(uuid.uuid4())

        extractor_response = audio_extractor(audio_b64)
        extractor_answer = response.get("final_answer")
        extractor_message = parse_final_answer(extractor_answer)

        if ai_message != "": 
            response = graph.invoke({'user_input': extractor_message}, {"configurable": {"thread_id": str(thread_id)}})
            final_answer = response.get("final_answer")
            ai_message = parse_final_answer(final_answer)

            create_at = response.get("create_at", datetime.now())

            message = BotRepository.save(db, Bot(
                thread_id=thread_id,
                user_message=user_msg,
                ai_message=ai_message,
                create_at=create_at
            ))
            return BotResponse.model_validate(message)

        raise HTTPException(400, "Áudio inválido")

    @staticmethod
    def get_all_messages(db: Session = Depends(get_db)):
        """Retorna todas as mensagens trocadas com o bot."""
        messages = BotRepository.get_messages(db)
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sem mensagens encontradas."
            )
        return [BotResponse.model_validate(message) for message in messages]


def is_valid_base64(data: str) -> bool:
    """
        Valida se uma str está em formato base64
        Args:
            data: informação no formato base64
    """
    try:
        base64.b64decode(data, validate=True)
        return True
    except (binascii.Error, ValueError):
        return False

def parse_final_answer(final_answer: str) -> str:
    """
        Recebe a mensagem gerada pelo agente e retorna em string.
    """
    if isinstance(final_answer, list) and len(final_answer) > 0:
        return final_answer[0].get("text", str(final_answer))
    elif isinstance(final_answer, str):
        return final_answer
    else:
        return str(final_answer)

