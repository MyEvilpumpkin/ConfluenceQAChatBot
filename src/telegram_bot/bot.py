from typing import Callable

from telegram import *
from telegram.ext import *


START_MESSAGE = (
    'Здравствуйте, я - бот, который может помочь Вам с поиском документов с ответами на Ваши вопросы\n\n'
    'Задавайте вопрос\nИли воспользуйтесь /help для получения более детальной информации'
)

HELP_MESSAGE = (
    'Бот может работать в 2 режимах:\n\n'
    '1. Поиск наиболее подходящего документа и поиск ответа на вопрос в нем\n'
    'Для этого нужно просто написать свой вопрос в сообщении боту\n\n'
    '2. Поиск нескольких наиболее подходящих документов\n'
    'Для этого необходимо воспользоваться командой\n/top <количество документов> <вопрос>'
)


def start(token: str, text_message_handler: Callable[[str, int], str]) -> None:
    """
    Launch bot
    """

    # Configure application
    application = (
        ApplicationBuilder()
        .token(token)
        .post_init(_post_init)
        .build()
    )

    # Set up handlers
    application.add_handler(CommandHandler('start', _start_command_handler))
    application.add_handler(CommandHandler('help', _help_command_handler))
    application.add_handler(CommandHandler('top', _top_command_handler(text_message_handler)))
    application.add_handler(MessageHandler(filters.COMMAND, _unknown_command_handler))
    application.add_handler(MessageHandler(filters.TEXT, _text_message_handler(text_message_handler)))

    # Start application
    application.run_polling()


async def _post_init(application: Application) -> None:
    """
    Post initialization function
    """

    # Set up menu commands
    await application.bot.set_my_commands([
        BotCommand('start', 'Начало работы'),
        BotCommand('help', 'Помощь'),
        BotCommand('top', 'Ответ в виде списка похожих документов'),
    ])


async def _start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start command handler
    """

    await update.message.reply_text(START_MESSAGE)


async def _help_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /help command handler
    """

    await update.message.reply_text(HELP_MESSAGE)


def _top_command_handler(text_message_handler: Callable[[str, int], str]):
    async def handle_top_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        /top command handler
        """

        # Check arguments quantity
        if len(context.args) < 2:
            await update.message.reply_text('Недостаточное количество аргументов команды')
            return

        # Check first argument type
        n_results = context.args[0]
        if not n_results.isdigit() or not int(n_results) > 0:
            await update.message.reply_text('Первым аргументом команды должно быть целое число > 0')
            return

        # Generate message from arguments
        message = ' '.join(context.args[1:])

        # Handle message
        response = text_message_handler(message, int(n_results))

        await update.message.reply_html(response)

    return handle_top_command


async def _unknown_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Unknown command handler
    """

    await update.message.reply_text('Я не понимаю этой команды')


def _text_message_handler(text_message_handler: Callable[[str, int], str]):
    async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Text message handler
        """

        # Handle message
        response = text_message_handler(update.message.text, 1)

        await update.message.reply_html(response)

    return handle_text_message
