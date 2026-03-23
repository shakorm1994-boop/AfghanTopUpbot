"""Mobile top-up handler."""

import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.translations import t
from utils.states import (
    MAIN_MENU, MOBILE_NETWORK, MOBILE_TYPE, MOBILE_PACKAGE,
    MOBILE_NUMBER, PAYMENT_METHOD,
)
from data.products import NETWORKS, MOBILE_PACKAGES


def _lang(context):
    return context.user_data.get("lang", "fa")


async def mobile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Route mobile top-up flow based on callback data."""
    lang = _lang(context)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        data = query.data
    else:
        # Text input – phone number step
        return await _handle_phone_number(update, context)

    # ── Step 1: show network selection ───────────────────────────────────────
    if data == "mobile":
        keyboard = [
            [InlineKeyboardButton(info[lang], callback_data=f"net_{key}")]
            for key, info in NETWORKS.items()
        ]
        keyboard.append([InlineKeyboardButton(t("btn_main", lang), callback_data="main_menu")])
        await query.edit_message_text(
            t("select_network", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return MOBILE_NETWORK

    # ── Step 2: show service type ─────────────────────────────────────────────
    if data.startswith("net_"):
        net = data.replace("net_", "")
        context.user_data["mobile_network"] = net
        keyboard = [
            [InlineKeyboardButton(t("btn_internet", lang), callback_data="mtype_internet")],
            [InlineKeyboardButton(t("btn_calls",    lang), callback_data="mtype_calls")],
            [InlineKeyboardButton(t("btn_credit",   lang), callback_data="mtype_credit")],
            [InlineKeyboardButton(t("btn_back",     lang), callback_data="mobile")],
        ]
        net_name = NETWORKS[net][lang]
        await query.edit_message_text(
            f"📶 {net_name}\n\n{t('select_type', lang)}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return MOBILE_TYPE

    if data == "net_back":
        return await mobile_handler.__wrapped__(update, context) if hasattr(mobile_handler, "__wrapped__") else await _go_networks(query, context, lang)

    # ── Step 3: show packages ─────────────────────────────────────────────────
    if data.startswith("mtype_"):
        svc = data.replace("mtype_", "")
        context.user_data["mobile_service"] = svc
        net = context.user_data.get("mobile_network", "roshan")
        packages = MOBILE_PACKAGES.get(net, {}).get(svc, [])

        keyboard = [
            [InlineKeyboardButton(
                f"{p[lang]}  —  {p['price']} USDT",
                callback_data=f"mpkg_{p['id']}"
            )]
            for p in packages
        ]
        keyboard.append([InlineKeyboardButton(t("btn_back", lang), callback_data=f"net_{net}")])

        await query.edit_message_text(
            t("select_package", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return MOBILE_PACKAGE

    # ── Step 4: selected package – ask phone number ───────────────────────────
    if data.startswith("mpkg_"):
        pkg_id = data.replace("mpkg_", "")
        net = context.user_data.get("mobile_network", "roshan")
        svc = context.user_data.get("mobile_service", "internet")
        packages = MOBILE_PACKAGES.get(net, {}).get(svc, [])
        pkg = next((p for p in packages if p["id"] == pkg_id), None)

        if pkg:
            context.user_data["selected_package"] = pkg
            context.user_data["order_type"] = "mobile"

        await query.edit_message_text(
            t("enter_number", lang),
        )
        return MOBILE_NUMBER

    return MOBILE_NETWORK


async def _go_networks(query, context, lang):
    keyboard = [
        [InlineKeyboardButton(info[lang], callback_data=f"net_{key}")]
        for key, info in NETWORKS.items()
    ]
    keyboard.append([InlineKeyboardButton(t("btn_main", lang), callback_data="main_menu")])
    await query.edit_message_text(
        t("select_network", lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return MOBILE_NETWORK


async def _handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate phone number and proceed to payment."""
    lang = _lang(context)
    number = update.message.text.strip()

    if not re.fullmatch(r"0\d{9}", number):
        await update.message.reply_text(t("invalid_number", lang))
        return MOBILE_NUMBER

    context.user_data["mobile_number"] = number

    # Build order summary
    pkg   = context.user_data.get("selected_package", {})
    net   = context.user_data.get("mobile_network", "")
    svc   = context.user_data.get("mobile_service", "")
    net_name = NETWORKS.get(net, {}).get(lang, net)

    summary_lines = [
        f"{'شبکه' if lang == 'fa' else 'Network'}: {net_name}",
        f"{'بسته' if lang == 'fa' else 'Package'}: {pkg.get(lang, '')}",
        f"{'شماره' if lang == 'fa' else 'Number'}: {number}",
        f"{'مبلغ' if lang == 'fa' else 'Amount'}: {pkg.get('price', 0)} USDT",
    ]
    context.user_data["order_summary"] = "\n".join(summary_lines)
    context.user_data["order_amount"]  = f"{pkg.get('price', 0)} USDT"

    from handlers.payment import show_payment_methods
    return await show_payment_methods(update, context)
