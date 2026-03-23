"""Payment handler."""

import random
import string
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.translations import t
from utils.states import PAYMENT_METHOD, AWAITING_RECEIPT, MAIN_MENU
from data.products import PAYMENT_ACCOUNTS


def _lang(c): return c.user_data.get("lang", "fa")

PAYMENT_METHODS = list(PAYMENT_ACCOUNTS.keys())


async def show_payment_methods(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show payment method selection."""
    lang    = _lang(context)
    summary = context.user_data.get("order_summary", "")
    amount  = context.user_data.get("order_amount", "")

    keyboard = [
        [InlineKeyboardButton(f"💳 {method}", callback_data=f"pay_{i}")]
        for i, method in enumerate(PAYMENT_METHODS)
    ]
    keyboard.append([InlineKeyboardButton(t("btn_main", lang), callback_data="main_menu")])

    text = t("select_payment", lang, summary=summary)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
        )
    return PAYMENT_METHOD


async def payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle payment method selection."""
    lang  = _lang(context)
    query = update.callback_query
    await query.answer()
    data  = query.data

    if data == "pay_back":
        return await show_payment_methods(update, context)

    idx    = int(data.replace("pay_", ""))
    method = PAYMENT_METHODS[idx]
    amount = context.user_data.get("order_amount", "")
    acct   = PAYMENT_ACCOUNTS[method][lang]

    context.user_data["payment_method"] = method

    text = t(
        "payment_instructions", lang,
        method=method,
        amount=amount,
        account_info=acct,
    )

    keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="pay_back")]]
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )

    # Follow-up prompt
    if update.callback_query.message.chat:
        await context.bot.send_message(
            chat_id=update.callback_query.message.chat.id,
            text=t("send_receipt_prompt", lang),
        )

    return AWAITING_RECEIPT


async def receipt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle receipt photo or transaction ID."""
    lang     = _lang(context)
    order_id = "".join(random.choices(string.digits, k=8))
    context.user_data["order_id"] = order_id

    # Notify user
    await update.message.reply_text(
        t("receipt_received", lang, order_id=order_id),
        parse_mode="Markdown",
    )

    # Forward to admin
    admin_id = context.bot_data.get("admin_id", 0)
    if admin_id:
        summary = context.user_data.get("order_summary", "")
        method  = context.user_data.get("payment_method", "")
        user    = update.effective_user
        admin_text = (
            f"🔔 *New Order #{order_id}*\n\n"
            f"👤 User: @{user.username or user.first_name} (ID: {user.id})\n"
            f"📋 Order:\n{summary}\n\n"
            f"💳 Payment: {method}\n"
            f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        try:
            if update.message.photo:
                await context.bot.send_photo(
                    chat_id=admin_id,
                    photo=update.message.photo[-1].file_id,
                    caption=admin_text,
                    parse_mode="Markdown",
                )
            else:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=admin_text + f"\n\n📝 Receipt/TX: {update.message.text}",
                    parse_mode="Markdown",
                )
        except Exception:
            pass

    # Show main menu button
    keyboard = [[InlineKeyboardButton(t("btn_main", lang), callback_data="main_menu")]]
    await update.message.reply_text(
        "🏠" if lang == "fa" else "🏠",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return MAIN_MENU
