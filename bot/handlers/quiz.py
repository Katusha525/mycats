"""Quiz handlers"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

import config
from bot.handlers.conversation import (
    SIZE, ACTIVITY, GROOMING, FRIENDLINESS, SHEDDING, VOCALIZATION
)
from services.user_service import user_service
from services.matcher import breed_matcher

logger = logging.getLogger(__name__)


async def start_quiz(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> int:
    """The beginning of the quiz"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Let's find your perfect cat breed!")

    keyboard = [
        [
            InlineKeyboardButton("Small", callback_data="size_small"),
            InlineKeyboardButton("Medium", callback_data="size_medium"),
            InlineKeyboardButton("Large", callback_data="size_large"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "What size cat do you prefer?",
        reply_markup=reply_markup
    )
    return SIZE


async def size_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Size selection handler"""
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    context.user_data["size"] = choice
    await query.edit_message_text(f"Size: {choice.capitalize()}")

    keyboard = [
        [
            InlineKeyboardButton("Low", callback_data="activity_low"),
            InlineKeyboardButton("Medium", callback_data="activity_medium"),
            InlineKeyboardButton("High", callback_data="activity_high"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "What activity level do you prefer?",
        reply_markup=reply_markup
    )
    return ACTIVITY


async def activity_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Activity selection handler"""
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    context.user_data["activity"] = choice
    await query.edit_message_text(f"Activity: {choice.capitalize()}")

    keyboard = [
        [
            InlineKeyboardButton("Low", callback_data="grooming_low"),
            InlineKeyboardButton("Medium", callback_data="grooming_medium"),
            InlineKeyboardButton("High", callback_data="grooming_high"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "How much grooming are you willing to do?",
        reply_markup=reply_markup
    )
    return GROOMING


async def grooming_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Care selection handler"""
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    context.user_data["grooming"] = choice
    await query.edit_message_text(f"Grooming: {choice.capitalize()}")

    keyboard = [
        [
            InlineKeyboardButton("Low", callback_data="friend_low"),
            InlineKeyboardButton("Medium", callback_data="friend_medium"),
            InlineKeyboardButton("High", callback_data="friend_high"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "How friendly should the cat be?",
        reply_markup=reply_markup
    )
    return FRIENDLINESS


async def friend_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler for selecting friendliness"""
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    context.user_data["friendliness"] = choice
    await query.edit_message_text(f"Friendliness: {choice.capitalize()}")

    keyboard = [
        [
            InlineKeyboardButton("Low", callback_data="shed_low"),
            InlineKeyboardButton("Medium", callback_data="shed_medium"),
            InlineKeyboardButton("High", callback_data="shed_high"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "How much shedding is acceptable?",
        reply_markup=reply_markup
    )
    return SHEDDING


async def shed_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Molt selection handler"""
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    context.user_data["shedding"] = choice
    await query.edit_message_text(f"Shedding: {choice.capitalize()}")

    keyboard = [
        [
            InlineKeyboardButton("Low", callback_data="vocal_low"),
            InlineKeyboardButton("Medium", callback_data="vocal_medium"),
            InlineKeyboardButton("High", callback_data="vocal_high"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "How vocal should the cat be?",
        reply_markup=reply_markup
    )
    return VOCALIZATION


async def vocal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """The final step is saving and recommending"""
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    context.user_data["vocalization"] = choice
    await query.edit_message_text(f"Vocalization: {choice.capitalize()}")

    chat_id = query.message.chat_id

    # Saving preferences
    user_service.save_preferences(chat_id, context.user_data)

    # Getting a recommendation
    name, text, image_url = breed_matcher.match_breed(context.user_data)

    # Sending the result
    await query.message.reply_text(f"Recommended breed: {name}\n\n{text}")
    if image_url:
        await query.message.reply_photo(photo=image_url, caption=name)

    context.user_data.clear()
    return ConversationHandler.END