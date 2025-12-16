from sqlalchemy.orm import Session

from models import Bot

class BotRepository:
    @staticmethod
    def save(db: Session, bot: Bot) -> Bot:
        db.add(bot)
        db.commit()
        db.refresh(bot)
        return bot

    @staticmethod
    def get_messages(db: Session):
        messages = db.query(Bot).all()
        if not messages:
            return None
        return messages