"""Start and main menu handler."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.translations import t
from utils.states import LANGUAGE, MAIN_MENU


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send welcome message with language selection."""
    keyboard = [
        [
            InlineKeyboardButton("🇦🇫 دری / فارسی", callback_data="lang_fa"),
            InlineKeyboardButton("🇬🇧 English",      callback_data="lang_en"),
        ]
    ]
    text = (
        "🇦🇫 *Afghan TopUp Bot*\n\n"
        "به بوت افغان تاپ‌آپ خوش آمدید!\n"
        "Welcome to Afghan TopUp Bot!\n\n"
        "لطفاً زبان خود را انتخاب کنید:\n"
        "Please select your language:"
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
        )
    return LANGUAGE


async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save language and show main menu."""
    query = update.callback_query
    await query.answer()

    lang = query.data.replace("lang_", "")
    context.user_data["lang"] = lang

    return await show_main_menu(update, context)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the main menu."""
    lang = context.user_data.get("lang", "fa")

    keyboard = [
        [InlineKeyboardButton(t("btn_mobile", lang), callback_data="mobile")],
        [InlineKeyboardButton(t("btn_games",  lang), callback_data="games")],
        [InlineKeyboardButton(t("btn_apps",   lang), callback_data="apps")],
    ]

    text = t("main_menu", lang)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
    return MAIN_MENU
