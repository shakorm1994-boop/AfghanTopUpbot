#!/usr/bin/env python3
"""
AfghanTopUpBot - Telegram Bot for Afghan Digital Top-Up Services
بوت تلگرام برای خدمات دیجیتال افغانستان
"""

import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

from handlers.start import start_handler, language_handler
from handlers.mobile import mobile_handler
from handlers.games import games_handler
from handlers.apps import apps_handler
from handlers.payment import payment_handler, receipt_handler
from handlers.admin import admin_handler
from utils.states import (
    LANGUAGE, MAIN_MENU,
    MOBILE_NETWORK, MOBILE_TYPE, MOBILE_PACKAGE, MOBILE_NUMBER,
    GAME_SELECT, GAME_PACKAGE, GAME_ID,
    APP_SELECT, APP_PACKAGE,
    PAYMENT_METHOD, AWAITING_RECEIPT,
)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

    app = Application.builder().token(BOT_TOKEN).build()
    app.bot_data["admin_id"] = ADMIN_ID

    # ── Conversation handler ──────────────────────────────────────────────────
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_handler)],
        states={
            LANGUAGE: [
                CallbackQueryHandler(language_handler, pattern="^lang_")
            ],
            MAIN_MENU: [
                CallbackQueryHandler(mobile_handler, pattern="^mobile$"),
                CallbackQueryHandler(games_handler, pattern="^games$"),
                CallbackQueryHandler(apps_handler,  pattern="^apps$"),
                CallbackQueryHandler(start_handler, pattern="^main_menu$"),
            ],
            MOBILE_NETWORK: [
                CallbackQueryHandler(mobile_handler, pattern="^net_"),
                CallbackQueryHandler(start_handler, pattern="^main_menu$"),
            ],
            MOBILE_TYPE: [
                CallbackQueryHandler(mobile_handler, pattern="^mtype_"),
                CallbackQueryHandler(mobile_handler, pattern="^net_back$"),
            ],
            MOBILE_PACKAGE: [
                CallbackQueryHandler(mobile_handler, pattern="^mpkg_"),
                CallbackQueryHandler(mobile_handler, pattern="^mtype_back$"),
            ],
            MOBILE_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, mobile_handler),
                CallbackQueryHandler(mobile_handler, pattern="^mpkg_back$"),
            ],
            GAME_SELECT: [
                CallbackQueryHandler(games_handler, pattern="^game_"),
                CallbackQueryHandler(start_handler, pattern="^main_menu$"),
            ],
            GAME_PACKAGE: [
                CallbackQueryHandler(games_handler, pattern="^gpkg_"),
                CallbackQueryHandler(games_handler, pattern="^game_back$"),
            ],
            GAME_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, games_handler),
                CallbackQueryHandler(games_handler, pattern="^gpkg_back$"),
            ],
            APP_SELECT: [
                CallbackQueryHandler(apps_handler, pattern="^app_"),
                CallbackQueryHandler(start_handler, pattern="^main_menu$"),
            ],
            APP_PACKAGE: [
                CallbackQueryHandler(apps_handler, pattern="^apkg_"),
                CallbackQueryHandler(apps_handler, pattern="^app_back$"),
            ],
            PAYMENT_METHOD: [
                CallbackQueryHandler(payment_handler, pattern="^pay_"),
                CallbackQueryHandler(mobile_handler, pattern="^mpkg_back$"),
                CallbackQueryHandler(games_handler,  pattern="^gpkg_back$"),
                CallbackQueryHandler(apps_handler,   pattern="^apkg_back$"),
            ],
            AWAITING_RECEIPT: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, receipt_handler),
                CallbackQueryHandler(payment_handler, pattern="^pay_back$"),
            ],
        },
        fallbacks=[
            CommandHandler("start", start_handler),
            CommandHandler("menu",  start_handler),
        ],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)

    # Admin commands
    app.add_handler(CommandHandler("admin", admin_handler))

    logger.info("✅ AfghanTopUpBot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
