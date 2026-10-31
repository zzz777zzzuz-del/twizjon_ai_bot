import os
import asyncio
import logging
import sqlite3

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

MODEL = "gemini-2.5-flash"

ai = genai.Client(api_key=GEMINI_API_KEY)

db = sqlite3.connect("bot.db", check_same_thread=False)

db.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    messages INTEGER DEFAULT 0
)
""")
db.commit()

chats = {}

SYSTEM = """
Sen TWIZJON AI nomli aqlli sun'iy intellektsan.

Vazifalaring:
- Dasturlashni o'rgatish.
- HTML, CSS, JavaScript va Python kodlari yozish.
- Xatolarni topish va tuzatish.
- IT savollariga javob berish.
- Ingliz, rus va koreys tillarini o'rgatish.
- Foydalanuvchiga o'zbek tilida tushuntirish.

Javoblaring aniq, tezkor va foydali bo'lsin.
"""

keyboard = Reply