from src.document_searching import TfidfModel
from src.telegram_bot import bot
from src.utils.config import bot_token
from src.utils.loader import get_model
from src.utils.question_handler import question_handler


if __name__ == '__main__':
    model = get_model(TfidfModel)
    bot.start(bot_token, question_handler(model))
