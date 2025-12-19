"""Basic command handlers"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.cat_api import cat_api_client
from services.user_service import user_service
from services.matcher import breed_matcher

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """The /start command handler is the main menu"""
    chat_id = update.message.chat_id
    user = update.message.from_user

    # Creating or getting a user
    user_service.get_or_create_user(
        chat_id=chat_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    keyboard = [
        [InlineKeyboardButton("Start Quiz", callback_data="start_quiz")],
        [InlineKeyboardButton("View Previous Match", callback_data="view_previous")],
        [InlineKeyboardButton("Random Cat Fact", callback_data="cat_fact")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to the Cat Breed Matcher Bot!\nChoose an option below:",
        reply_markup=reply_markup,
    )


async def view_previous(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Viewing the previous selection"""
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    prefs = user_service.get_user_preferences(chat_id)
    if not prefs:
        await query.message.reply_text(
            "No previous preferences found. Start the quiz!"
        )
        return

    name, text, image_url = breed_matcher.match_breed(prefs)
    await query.message.reply_text(f"Previous match: {name}\n\n{text}")
    if image_url:
        await query.message.reply_photo(photo=image_url, caption=name)


async def cat_fact_handler(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """A random fact about cats"""
    query = update.callback_query
    await query.answer()
    fact = cat_api_client.fetch_cat_fact()
    await query.message.reply_text(f"Cat Fact: {fact}")


async def help_handler(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help on the bot"""
    query = update.callback_query if update.callback_query else None
    if query:
        await query.answer()

    text = (
        "Cat Breed Matcher Bot\n\n"
        "/start — main menu\n"
        "Start Quiz — answer questions to get a breed recommendation\n"
        "View Previous Match — see your last result\n"
        "Random Cat Fact — fun fact about cats\n"
        "Help — this message"
    )
    if query:
        await query.message.reply_text(text)
    else:
        await update.message.reply_text(text)