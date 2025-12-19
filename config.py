"""Application configuration"""

from typing import Final

# Telegram Bot Token
BOT_TOKEN: Final = ""

# TheCatAPI
CAT_API_URL: Final = "https://api.thecatapi.com/v1/breeds"
CAT_FACT_URL: Final = "https://catfact.ninja/fact"
API_KEY: Final = ""

# Database
DATABASE_URL: Final = "sqlite:///cat_bot.db"

# Conversation states
SIZE, ACTIVITY, GROOMING, FRIENDLINESS, SHEDDING, VOCALIZATION = range(6)

# Scoring weights
SCORE_WEIGHTS = {
    "size": 2.0,
    "activity": 1.5,
    "grooming": 1.5,
    "friendliness": 1.5,
    "shedding": 1.0,
    "vocalization": 1.0,
    "has_image": 0.5
}
