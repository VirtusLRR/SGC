from sqlalchemy.orm import Session

from models import Bot

class BotRepository:
    @staticmethod
    def save(db: Session, bot: Bot) -> Bot:
        """Salva ou atualiza uma mensagem do bot no banco de dados."""
        db.add(bot)
        db.commit()
        db.refresh(bot)
        return bot

    @staticmethod
    def get_messages(db: Session):
        """Recupera todas as mensagens do bot do banco de dados."""
        messages = db.query(Bot).all()
        if not messages:
            return None
        return messages