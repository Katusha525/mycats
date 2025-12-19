"""Creating and configuring a bot application"""

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

import config
from bot.handlers import base, quiz
from bot.handlers.conversation import (
    SIZE, ACTIVITY, GROOMING, FRIENDLINESS, SHEDDING, VOCALIZATION
)

logger = logging.getLogger(__name__)


def create_application() -> Application:
    """Create and configure a bot application"""
    logger.info("Creating application...")
    application = Application.builder().token(config.BOT_TOKEN).build()

    # ConversationHandler for the quiz
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(quiz.start_quiz, pattern="^start_quiz$")],
        states={
            SIZE: [CallbackQueryHandler(quiz.size_handler, pattern="^size_")],
            ACTIVITY: [CallbackQueryHandler(quiz.activity_handler, pattern="^activity_")],
            GROOMING: [CallbackQueryHandler(quiz.grooming_handler, pattern="^grooming_")],
            FRIENDLINESS: [CallbackQueryHandler(quiz.friend_handler, pattern="^friend_")],
            SHEDDING: [CallbackQueryHandler(quiz.shed_handler, pattern="^shed_")],
            VOCALIZATION: [CallbackQueryHandler(quiz.vocal_handler, pattern="^vocal_")],
        },
        fallbacks=[],
    )

    # Adding handlers
    application.add_handler(CommandHandler("start", base.start))
    application.add_handler(conv_handler)
    application.add_handler(
        CallbackQueryHandler(base.view_previous, pattern="^view_previous$")
    )
    application.add_handler(
        CallbackQueryHandler(base.cat_fact_handler, pattern="^cat_fact$")
    )
    application.add_handler(
        CallbackQueryHandler(base.help_handler, pattern="^help$")
    )

    logger.info("Application created successfully")
    return application