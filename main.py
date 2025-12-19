"""The main entry point of the application"""

from bot.application import create_application
from utils.logging_setup import get_logger

logger = get_logger(__name__)


def main() -> None:
    """Launch the bot"""
    logger.info("Initializing bot...")

    application = create_application()

    logger.info("Bot is starting...")
    application.run_polling()


if __name__ == "__main__":
    main()