"""Admin handler."""

from telegram import Update
from telegram.ext import ContextTypes


async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Basic admin panel – only accessible by admin."""
    admin_id = context.bot_data.get("admin_id", 0)
    user_id  = update.effective_user.id

    if user_id != admin_id:
        await update.message.reply_text("⛔ Access denied.")
        return

    await update.message.reply_text(
        "🔐 *Admin Panel*\n\n"
        "Commands:\n"
        "/admin – This panel\n\n"
        "📊 Bot is running normally.",
        parse_mode="Markdown",
    )
