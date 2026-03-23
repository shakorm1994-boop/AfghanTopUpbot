#!/usr/bin/env python3
"""
AfghanTopUpBot - Single file version
بوت تلگرام افغان تاپ‌آپ - نسخه تک‌فایلی
"""

import logging
import os
import re
import random
import string
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ConversationHandler, ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── States ────────────────────────────────────────────────────────────────────
(
    LANGUAGE, MAIN_MENU,
    MOBILE_NETWORK, MOBILE_TYPE, MOBILE_PACKAGE, MOBILE_NUMBER,
    GAME_SELECT, GAME_PACKAGE, GAME_ID,
    APP_SELECT, APP_PACKAGE,
    PAYMENT_METHOD, AWAITING_RECEIPT,
) = range(13)

# ── Translations ──────────────────────────────────────────────────────────────
TEXTS = {
    "main_menu":        {"fa": "🏠 *منوی اصلی*\n\nلطفاً یک گزینه را انتخاب کنید:", "en": "🏠 *Main Menu*\n\nPlease select an option:"},
    "btn_mobile":       {"fa": "📱 شارژ موبایل افغانستان", "en": "📱 Afghan Mobile Top-Up"},
    "btn_games":        {"fa": "🎮 گیم‌ها", "en": "🎮 Games"},
    "btn_apps":         {"fa": "📲 برنامه‌ها", "en": "📲 Apps & Subscriptions"},
    "btn_back":         {"fa": "🔙 بازگشت", "en": "🔙 Back"},
    "btn_main":         {"fa": "🏠 منوی اصلی", "en": "🏠 Main Menu"},
    "select_network":   {"fa": "📶 لطفاً شبکه موبایل را انتخاب کنید:", "en": "📶 Please select a mobile network:"},
    "select_type":      {"fa": "لطفاً نوع سرویس را انتخاب کنید:", "en": "Please select the service type:"},
    "btn_internet":     {"fa": "🌐 بسته انترنت", "en": "🌐 Internet Package"},
    "btn_calls":        {"fa": "📞 دقیقه تماس", "en": "📞 Call Minutes"},
    "btn_credit":       {"fa": "💳 شارژ مستقیم", "en": "💳 Direct Credit"},
    "select_package":   {"fa": "📦 لطفاً بسته مورد نظر را انتخاب کنید:", "en": "📦 Please select a package:"},
    "enter_number":     {"fa": "📱 لطفاً شماره موبایل مقصد را وارد کنید:\n\nمثال: 0700123456", "en": "📱 Please enter the destination mobile number:\n\nExample: 0700123456"},
    "invalid_number":   {"fa": "❌ شماره نامعتبر است. ۱۰ رقم وارد کنید.", "en": "❌ Invalid number. Please enter 10 digits."},
    "select_game":      {"fa": "🎮 لطفاً بازی مورد نظر را انتخاب کنید:", "en": "🎮 Please select a game:"},
    "select_gpkg":      {"fa": "💎 لطفاً بسته مورد نظر را انتخاب کنید:", "en": "💎 Please select a package:"},
    "enter_game_id":    {"fa": "🆔 لطفاً ID بازی خود را وارد کنید:\n\n📌 PUBG: Player ID\n📌 Free Fire: UID\n📌 Mobile Legends: ID + Server", "en": "🆔 Please enter your Game ID:\n\n📌 PUBG: Player ID\n📌 Free Fire: UID\n📌 Mobile Legends: ID + Server"},
    "select_app":       {"fa": "📲 لطفاً برنامه مورد نظر را انتخاب کنید:", "en": "📲 Please select an app/subscription:"},
    "send_receipt":     {"fa": "📸 لطفاً اسکرین‌شات رسید پرداخت یا شماره تراکنش را ارسال کنید:", "en": "📸 Please send a screenshot of the receipt or the transaction ID:"},
    "receipt_ok":       {"fa": "✅ *رسید دریافت شد!*\n\nسفارش شما در حال بررسی است.\nپس از تأیید، سرویس فعال می‌شود.\n\n🕐 زمان بررسی: ۵ تا ۳۰ دقیقه\n🆔 شماره سفارش: #{oid}", "en": "✅ *Receipt received!*\n\nYour order is being reviewed.\nService will be activated after confirmation.\n\n🕐 Review time: 5–30 minutes\n🆔 Order ID: #{oid}"},
}

def t(key, lang, **kw):
    text = TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get("en", key))
    return text.format(**kw) if kw else text

# ── Products ──────────────────────────────────────────────────────────────────
PAYMENT_ACCOUNTS = {
    "USDT (TRC20)":   {"fa": "آدرس USDT (TRC20):\n`TYourUSDTAddressHere`",        "en": "USDT (TRC20) Address:\n`TYourUSDTAddressHere`"},
    "Binance Pay":    {"fa": "Binance Pay ID:\n`123456789`",                        "en": "Binance Pay ID:\n`123456789`"},
    "Papara":         {"fa": "شماره Papara:\n`0500-000-0000`",                      "en": "Papara Number:\n`0500-000-0000`"},
    "M-Paisa":        {"fa": "شماره M-Paisa:\n`03XX-XXXXXXX`",                     "en": "M-Paisa Number:\n`03XX-XXXXXXX`"},
}
PAYMENT_METHODS = list(PAYMENT_ACCOUNTS.keys())

NETWORKS = {
    "roshan":   {"fa": "🟢 روشن (Roshan)", "en": "🟢 Roshan"},
    "mtn":      {"fa": "🟡 MTN افغانستان",  "en": "🟡 MTN Afghanistan"},
    "etisalat": {"fa": "🔵 اتصالات",        "en": "🔵 Etisalat"},
    "salaam":   {"fa": "🟠 سلام",           "en": "🟠 Salaam"},
}

MOBILE_PACKAGES = {
    "roshan": {
        "internet": [
            {"id":"r_n1","fa":"۱ GB - ۱ روز","en":"1 GB – 1 Day","price":0.50},
            {"id":"r_n2","fa":"۵ GB - ۷ روز","en":"5 GB – 7 Days","price":2.00},
            {"id":"r_n3","fa":"۱۰ GB - ۳۰ روز","en":"10 GB – 30 Days","price":3.50},
            {"id":"r_n4","fa":"۲۰ GB - ۳۰ روز","en":"20 GB – 30 Days","price":6.00},
        ],
        "calls": [
            {"id":"r_c1","fa":"۳۰ دقیقه","en":"30 Minutes","price":0.60},
            {"id":"r_c2","fa":"۶۰ دقیقه","en":"60 Minutes","price":1.00},
            {"id":"r_c3","fa":"۱۲۰ دقیقه","en":"120 Minutes","price":1.80},
            {"id":"r_c4","fa":"۳۰۰ دقیقه","en":"300 Minutes","price":4.00},
        ],
        "credit": [
            {"id":"r_cr1","fa":"۵۰ افغانی","en":"50 AFN","price":0.60},
            {"id":"r_cr2","fa":"۱۰۰ افغانی","en":"100 AFN","price":1.20},
            {"id":"r_cr3","fa":"۲۰۰ افغانی","en":"200 AFN","price":2.30},
            {"id":"r_cr4","fa":"۵۰۰ افغانی","en":"500 AFN","price":5.50},
        ],
    },
    "mtn": {
        "internet": [
            {"id":"m_n1","fa":"۱ GB - ۱ روز","en":"1 GB – 1 Day","price":0.50},
            {"id":"m_n2","fa":"۵ GB - ۷ روز","en":"5 GB – 7 Days","price":1.90},
            {"id":"m_n3","fa":"۱۰ GB - ۳۰ روز","en":"10 GB – 30 Days","price":3.40},
            {"id":"m_n4","fa":"۲۵ GB - ۳۰ روز","en":"25 GB – 30 Days","price":7.00},
        ],
        "calls": [
            {"id":"m_c1","fa":"۳۰ دقیقه","en":"30 Minutes","price":0.55},
            {"id":"m_c2","fa":"۶۰ دقیقه","en":"60 Minutes","price":1.00},
            {"id":"m_c3","fa":"۲۰۰ دقیقه","en":"200 Minutes","price":3.00},
        ],
        "credit": [
            {"id":"m_cr1","fa":"۵۰ افغانی","en":"50 AFN","price":0.60},
            {"id":"m_cr2","fa":"۱۰۰ افغانی","en":"100 AFN","price":1.20},
            {"id":"m_cr3","fa":"۲۵۰ افغانی","en":"250 AFN","price":2.80},
            {"id":"m_cr4","fa":"۵۰۰ افغانی","en":"500 AFN","price":5.50},
        ],
    },
    "etisalat": {
        "internet": [
            {"id":"e_n1","fa":"۲ GB - ۳ روز","en":"2 GB – 3 Days","price":0.80},
            {"id":"e_n2","fa":"۸ GB - ۱۵ روز","en":"8 GB – 15 Days","price":2.50},
            {"id":"e_n3","fa":"۱۵ GB - ۳۰ روز","en":"15 GB – 30 Days","price":4.50},
        ],
        "calls": [
            {"id":"e_c1","fa":"۵۰ دقیقه","en":"50 Minutes","price":0.80},
            {"id":"e_c2","fa":"۱۰۰ دقیقه","en":"100 Minutes","price":1.50},
        ],
        "credit": [
            {"id":"e_cr1","fa":"۱۰۰ افغانی","en":"100 AFN","price":1.20},
            {"id":"e_cr2","fa":"۲۰۰ افغانی","en":"200 AFN","price":2.30},
            {"id":"e_cr3","fa":"۵۰۰ افغانی","en":"500 AFN","price":5.50},
        ],
    },
    "salaam": {
        "internet": [
            {"id":"s_n1","fa":"۱ GB - ۱ روز","en":"1 GB – 1 Day","price":0.50},
            {"id":"s_n2","fa":"۵ GB - ۷ روز","en":"5 GB – 7 Days","price":2.00},
            {"id":"s_n3","fa":"۱۰ GB - ۳۰ روز","en":"10 GB – 30 Days","price":3.50},
        ],
        "calls": [
            {"id":"s_c1","fa":"۳۰ دقیقه","en":"30 Minutes","price":0.60},
            {"id":"s_c2","fa":"۱۲۰ دقیقه","en":"120 Minutes","price":1.80},
        ],
        "credit": [
            {"id":"s_cr1","fa":"۵۰ افغانی","en":"50 AFN","price":0.60},
            {"id":"s_cr2","fa":"۲۰۰ افغانی","en":"200 AFN","price":2.30},
        ],
    },
}

GAMES = {
    "pubg":     {"fa":"🎯 PUBG Mobile (UC)",        "en":"🎯 PUBG Mobile (UC)"},
    "freefire": {"fa":"🔥 Free Fire (الماس)",        "en":"🔥 Free Fire (Diamonds)"},
    "mlbb":     {"fa":"⚔️ Mobile Legends (الماس)",  "en":"⚔️ Mobile Legends (Diamonds)"},
    "cod":      {"fa":"🔫 Call of Duty Mobile (CP)", "en":"🔫 Call of Duty Mobile (CP)"},
}

GAME_PACKAGES = {
    "pubg": [
        {"id":"pu60",  "fa":"۶۰ UC",   "en":"60 UC",   "price":0.90},
        {"id":"pu180", "fa":"۱۸۰ UC",  "en":"180 UC",  "price":2.50},
        {"id":"pu325", "fa":"۳۲۵ UC",  "en":"325 UC",  "price":4.50},
        {"id":"pu660", "fa":"۶۶۰ UC",  "en":"660 UC",  "price":8.50},
        {"id":"pu1800","fa":"۱۸۰۰ UC", "en":"1800 UC", "price":22.00},
        {"id":"pu3850","fa":"۳۸۵۰ UC", "en":"3850 UC", "price":44.00},
        {"id":"pu8100","fa":"۸۱۰۰ UC", "en":"8100 UC", "price":88.00},
    ],
    "freefire": [
        {"id":"ff100", "fa":"۱۰۰ الماس", "en":"100 Diamonds", "price":1.00},
        {"id":"ff310", "fa":"۳۱۰ الماس", "en":"310 Diamonds", "price":3.00},
        {"id":"ff520", "fa":"۵۲۰ الماس", "en":"520 Diamonds", "price":5.00},
        {"id":"ff1060","fa":"۱۰۶۰ الماس","en":"1060 Diamonds","price":9.50},
        {"id":"ff2180","fa":"۲۱۸۰ الماس","en":"2180 Diamonds","price":19.00},
        {"id":"ff5600","fa":"۵۶۰۰ الماس","en":"5600 Diamonds","price":47.00},
    ],
    "mlbb": [
        {"id":"ml86",  "fa":"۸۶ الماس",  "en":"86 Diamonds",  "price":1.20},
        {"id":"ml172", "fa":"۱۷۲ الماس", "en":"172 Diamonds", "price":2.30},
        {"id":"ml257", "fa":"۲۵۷ الماس", "en":"257 Diamonds", "price":3.40},
        {"id":"ml514", "fa":"۵۱۴ الماس", "en":"514 Diamonds", "price":6.50},
        {"id":"ml1029","fa":"۱۰۲۹ الماس","en":"1029 Diamonds","price":12.50},
        {"id":"ml2195","fa":"۲۱۹۵ الماس","en":"2195 Diamonds","price":25.00},
    ],
    "cod": [
        {"id":"cod80",  "fa":"۸۰ CP",   "en":"80 CP",   "price":1.00},
        {"id":"cod400", "fa":"۴۰۰ CP",  "en":"400 CP",  "price":4.80},
        {"id":"cod800", "fa":"۸۰۰ CP",  "en":"800 CP",  "price":9.30},
        {"id":"cod2000","fa":"۲۰۰۰ CP", "en":"2000 CP", "price":22.00},
        {"id":"cod5000","fa":"۵۰۰۰ CP", "en":"5000 CP", "price":52.00},
    ],
}

APPS = {
    "netflix": {"fa":"🎬 Netflix اشتراک",      "en":"🎬 Netflix Subscription"},
    "google":  {"fa":"🎁 Google Play Gift Card","en":"🎁 Google Play Gift Card"},
    "apple":   {"fa":"🍎 Apple Gift Card",      "en":"🍎 Apple Gift Card"},
}

APP_PACKAGES = {
    "netflix": [
        {"id":"nf1ms", "fa":"۱ ماه - استاندارد", "en":"1 Month – Standard", "price":8.00},
        {"id":"nf1mp", "fa":"۱ ماه - پریمیوم",   "en":"1 Month – Premium",  "price":13.00},
        {"id":"nf3ms", "fa":"۳ ماه - استاندارد", "en":"3 Months – Standard","price":22.00},
        {"id":"nf3mp", "fa":"۳ ماه - پریمیوم",   "en":"3 Months – Premium", "price":36.00},
        {"id":"nf6mp", "fa":"۶ ماه - پریمیوم",   "en":"6 Months – Premium", "price":68.00},
        {"id":"nf12mp","fa":"۱۲ ماه - پریمیوم",  "en":"12 Months – Premium","price":130.00},
    ],
    "google": [
        {"id":"gp5",  "fa":"$۵ گیفت کارت",  "en":"$5 Gift Card",  "price":5.50},
        {"id":"gp10", "fa":"$۱۰ گیفت کارت", "en":"$10 Gift Card", "price":10.80},
        {"id":"gp25", "fa":"$۲۵ گیفت کارت", "en":"$25 Gift Card", "price":26.50},
        {"id":"gp50", "fa":"$۵۰ گیفت کارت", "en":"$50 Gift Card", "price":52.00},
    ],
    "apple": [
        {"id":"ap5",  "fa":"$۵ گیفت کارت",  "en":"$5 Gift Card",  "price":5.80},
        {"id":"ap10", "fa":"$۱۰ گیفت کارت", "en":"$10 Gift Card", "price":11.20},
        {"id":"ap25", "fa":"$۲۵ گیفت کارت", "en":"$25 Gift Card", "price":27.00},
        {"id":"ap50", "fa":"$۵۰ گیفت کارت", "en":"$50 Gift Card", "price":53.00},
    ],
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def lang(ctx): return ctx.user_data.get("lang", "fa")

def find_pkg(pkg_id):
    for catalog in [
        *[p for n in MOBILE_PACKAGES.values() for p in n.values()],
        *GAME_PACKAGES.values(),
        *APP_PACKAGES.values(),
    ]:
        for p in catalog:
            if p["id"] == pkg_id:
                return p
    return None

async def edit_or_send(update, text, keyboard, parse_mode="Markdown"):
    markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=markup, parse_mode=parse_mode)
    else:
        await update.message.reply_text(text, reply_markup=markup, parse_mode=parse_mode)

# ── Start ─────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[
        InlineKeyboardButton("🇦🇫 دری / فارسی", callback_data="lang_fa"),
        InlineKeyboardButton("🇬🇧 English",      callback_data="lang_en"),
    ]]
    text = (
        "🇦🇫 *Afghan TopUp Bot*\n\n"
        "به بوت افغان تاپ‌آپ خوش آمدید!\n"
        "Welcome to Afghan TopUp Bot!\n\n"
        "لطفاً زبان خود را انتخاب کنید / Please select your language:"
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    return LANGUAGE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    context.user_data["lang"] = update.callback_query.data.replace("lang_", "")
    return await main_menu(update, context)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lg = lang(context)
    kb = [
        [InlineKeyboardButton(t("btn_mobile", lg), callback_data="mobile")],
        [InlineKeyboardButton(t("btn_games",  lg), callback_data="games")],
        [InlineKeyboardButton(t("btn_apps",   lg), callback_data="apps")],
    ]
    await edit_or_send(update, t("main_menu", lg), kb)
    return MAIN_MENU

# ── Mobile ────────────────────────────────────────────────────────────────────
async def mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lg = lang(context)
    if update.callback_query:
        await update.callback_query.answer()
        data = update.callback_query.data

        if data == "mobile":
            kb = [[InlineKeyboardButton(v[lg], callback_data=f"net_{k}")] for k,v in NETWORKS.items()]
            kb.append([InlineKeyboardButton(t("btn_main", lg), callback_data="main_menu")])
            await update.callback_query.edit_message_text(t("select_network", lg), reply_markup=InlineKeyboardMarkup(kb))
            return MOBILE_NETWORK

        if data.startswith("net_"):
            net = data[4:]
            context.user_data["net"] = net
            kb = [
                [InlineKeyboardButton(t("btn_internet", lg), callback_data="mtype_internet")],
                [InlineKeyboardButton(t("btn_calls",    lg), callback_data="mtype_calls")],
                [InlineKeyboardButton(t("btn_credit",   lg), callback_data="mtype_credit")],
                [InlineKeyboardButton(t("btn_back",     lg), callback_data="mobile")],
            ]
            await update.callback_query.edit_message_text(
                f"📶 {NETWORKS[net][lg]}\n\n{t('select_type', lg)}",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            return MOBILE_TYPE

        if data.startswith("mtype_"):
            svc = data[6:]
            context.user_data["svc"] = svc
            net = context.user_data.get("net","roshan")
            pkgs = MOBILE_PACKAGES.get(net,{}).get(svc,[])
            kb = [[InlineKeyboardButton(f"{p[lg]}  —  {p['price']} USDT", callback_data=f"mpkg_{p['id']}")] for p in pkgs]
            kb.append([InlineKeyboardButton(t("btn_back", lg), callback_data=f"net_{net}")])
            await update.callback_query.edit_message_text(t("select_package", lg), reply_markup=InlineKeyboardMarkup(kb))
            return MOBILE_PACKAGE

        if data.startswith("mpkg_"):
            pid = data[5:]
            net = context.user_data.get("net","roshan")
            svc = context.user_data.get("svc","internet")
            pkg = next((p for p in MOBILE_PACKAGES.get(net,{}).get(svc,[]) if p["id"]==pid), None)
            if pkg:
                context.user_data["pkg"] = pkg
                context.user_data["otype"] = "mobile"
            await update.callback_query.edit_message_text(t("enter_number", lg))
            return MOBILE_NUMBER

    else:
        # phone number input
        num = update.message.text.strip()
        if not re.fullmatch(r"0\d{9}", num):
            await update.message.reply_text(t("invalid_number", lg))
            return MOBILE_NUMBER
        context.user_data["dest"] = num
        pkg = context.user_data.get("pkg", {})
        net = context.user_data.get("net","")
        context.user_data["summary"] = (
            f"{'شبکه' if lg=='fa' else 'Network'}: {NETWORKS.get(net,{}).get(lg,'')}\n"
            f"{'بسته' if lg=='fa' else 'Package'}: {pkg.get(lg,'')}\n"
            f"{'شماره' if lg=='fa' else 'Number'}: {num}\n"
            f"{'مبلغ' if lg=='fa' else 'Amount'}: {pkg.get('price',0)} USDT"
        )
        context.user_data["amount"] = f"{pkg.get('price',0)} USDT"
        return await show_payment(update, context)

    return MOBILE_NETWORK

# ── Games ─────────────────────────────────────────────────────────────────────
async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lg = lang(context)
    if update.callback_query:
        await update.callback_query.answer()
        data = update.callback_query.data

        if data == "games":
            kb = [[InlineKeyboardButton(v[lg], callback_data=f"game_{k}")] for k,v in GAMES.items()]
            kb.append([InlineKeyboardButton(t("btn_main", lg), callback_data="main_menu")])
            await update.callback_query.edit_message_text(t("select_game", lg), reply_markup=InlineKeyboardMarkup(kb))
            return GAME_SELECT

        if data.startswith("game_"):
            gid = data[5:]
            context.user_data["game"] = gid
            pkgs = GAME_PACKAGES.get(gid,[])
            kb = [[InlineKeyboardButton(f"{p[lg]}  —  {p['price']} USDT", callback_data=f"gpkg_{p['id']}")] for p in pkgs]
            kb.append([InlineKeyboardButton(t("btn_back", lg), callback_data="games")])
            await update.callback_query.edit_message_text(
                f"{GAMES.get(gid,{}).get(lg,gid)}\n\n{t('select_gpkg', lg)}",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            return GAME_PACKAGE

        if data.startswith("gpkg_"):
            pid = data[5:]
            gid = context.user_data.get("game","pubg")
            pkg = next((p for p in GAME_PACKAGES.get(gid,[]) if p["id"]==pid), None)
            if pkg:
                context.user_data["pkg"] = pkg
                context.user_data["otype"] = "game"
            await update.callback_query.edit_message_text(t("enter_game_id", lg))
            return GAME_ID

    else:
        gid_input = update.message.text.strip()
        context.user_data["dest"] = gid_input
        gid = context.user_data.get("game","")
        pkg = context.user_data.get("pkg",{})
        context.user_data["summary"] = (
            f"{'بازی' if lg=='fa' else 'Game'}: {GAMES.get(gid,{}).get(lg,'')}\n"
            f"{'بسته' if lg=='fa' else 'Package'}: {pkg.get(lg,'')}\n"
            f"{'شناسه' if lg=='fa' else 'Game ID'}: {gid_input}\n"
            f"{'مبلغ' if lg=='fa' else 'Amount'}: {pkg.get('price',0)} USDT"
        )
        context.user_data["amount"] = f"{pkg.get('price',0)} USDT"
        return await show_payment(update, context)

    return GAME_SELECT

# ── Apps ──────────────────────────────────────────────────────────────────────
async def apps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lg = lang(context)
    if not update.callback_query:
        return APP_SELECT
    await update.callback_query.answer()
    data = update.callback_query.data

    if data == "apps":
        kb = [[InlineKeyboardButton(v[lg], callback_data=f"app_{k}")] for k,v in APPS.items()]
        kb.append([InlineKeyboardButton(t("btn_main", lg), callback_data="main_menu")])
        await update.callback_query.edit_message_text(t("select_app", lg), reply_markup=InlineKeyboardMarkup(kb))
        return APP_SELECT

    if data.startswith("app_") and not data == "app_back":
        aid = data[4:]
        context.user_data["app"] = aid
        pkgs = APP_PACKAGES.get(aid,[])
        kb = [[InlineKeyboardButton(f"{p[lg]}  —  {p['price']} USDT", callback_data=f"apkg_{p['id']}")] for p in pkgs]
        kb.append([InlineKeyboardButton(t("btn_back", lg), callback_data="apps")])
        await update.callback_query.edit_message_text(
            f"{APPS.get(aid,{}).get(lg,aid)}\n\n{t('select_package', lg)}",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        return APP_PACKAGE

    if data == "app_back":
        kb = [[InlineKeyboardButton(v[lg], callback_data=f"app_{k}")] for k,v in APPS.items()]
        kb.append([InlineKeyboardButton(t("btn_main", lg), callback_data="main_menu")])
        await update.callback_query.edit_message_text(t("select_app", lg), reply_markup=InlineKeyboardMarkup(kb))
        return APP_SELECT

    if data.startswith("apkg_"):
        pid = data[5:]
        aid = context.user_data.get("app","netflix")
        pkg = next((p for p in APP_PACKAGES.get(aid,[]) if p["id"]==pid), None)
        if pkg:
            context.user_data["pkg"] = pkg
            context.user_data["otype"] = "app"
        app_name = APPS.get(aid,{}).get(lg,aid)
        context.user_data["summary"] = (
            f"{'برنامه' if lg=='fa' else 'App'}: {app_name}\n"
            f"{'بسته' if lg=='fa' else 'Package'}: {pkg.get(lg,'') if pkg else ''}\n"
            f"{'مبلغ' if lg=='fa' else 'Amount'}: {pkg.get('price',0) if pkg else 0} USDT"
        )
        context.user_data["amount"] = f"{pkg.get('price',0) if pkg else 0} USDT"
        return await show_payment(update, context)

    return APP_SELECT

# ── Payment ───────────────────────────────────────────────────────────────────
async def show_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lg = lang(context)
    summary = context.user_data.get("summary","")
    kb = [[InlineKeyboardButton(f"💳 {m}", callback_data=f"pay_{i}")] for i,m in enumerate(PAYMENT_METHODS)]
    kb.append([InlineKeyboardButton(t("btn_main", lg), callback_data="main_menu")])
    text = f"💳 *{'خلاصه سفارش' if lg=='fa' else 'Order Summary'}:*\n\n{summary}\n\n{'لطفاً روش پرداخت را انتخاب کنید:' if lg=='fa' else 'Please select a payment method:'}"
    await edit_or_send(update, text, kb)
    return PAYMENT_METHOD

async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lg = lang(context)
    await update.callback_query.answer()
    data = update.callback_query.data
    idx = int(data.replace("pay_",""))
    method = PAYMENT_METHODS[idx]
    amount = context.user_data.get("amount","")
    acct = PAYMENT_ACCOUNTS[method][lg]
    context.user_data["method"] = method
    text = (
        f"✅ *{'روش پرداخت' if lg=='fa' else 'Payment Method'}: {method}*\n\n"
        f"💰 {'مبلغ' if lg=='fa' else 'Amount'}: *{amount}*\n\n"
        f"📤 {'لطفاً مبلغ را به حساب زیر پرداخت کنید' if lg=='fa' else 'Please send payment to'}:\n\n"
        f"{acct}\n\n"
        f"⚠️ {'بعد از پرداخت رسید یا شماره تراکنش را ارسال کنید.' if lg=='fa' else 'After payment, send the receipt or transaction ID.'}"
    )
    kb = [[InlineKeyboardButton(t("btn_back", lg), callback_data="pay_back")]]
    await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    await context.bot.send_message(update.callback_query.message.chat.id, t("send_receipt", lg))
    return AWAITING_RECEIPT

async def receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lg = lang(context)
    oid = "".join(random.choices(string.digits, k=8))
    await update.message.reply_text(t("receipt_ok", lg, oid=oid), parse_mode="Markdown")

    admin_id = context.bot_data.get("admin_id", 0)
    if admin_id:
        user = update.effective_user
        msg = (
            f"🔔 *New Order #{oid}*\n\n"
            f"👤 @{user.username or user.first_name} (ID: {user.id})\n"
            f"📋 {context.user_data.get('summary','')}\n"
            f"💳 {context.user_data.get('method','')}\n"
            f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        try:
            if update.message.photo:
                await context.bot.send_photo(admin_id, update.message.photo[-1].file_id, caption=msg, parse_mode="Markdown")
            else:
                await context.bot.send_message(admin_id, msg + f"\n\n📝 {update.message.text}", parse_mode="Markdown")
        except Exception:
            pass

    kb = [[InlineKeyboardButton(t("btn_main", lg), callback_data="main_menu")]]
    await update.message.reply_text(
        "🏠", reply_markup=InlineKeyboardMarkup(kb)
    )
    return MAIN_MENU

# ── Admin ─────────────────────────────────────────────────────────────────────
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != context.bot_data.get("admin_id", 0):
        await update.message.reply_text("⛔ Access denied.")
        return
    await update.message.reply_text("🔐 *Admin Panel*\n\nBot is running normally. ✅", parse_mode="Markdown")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    ADMIN_ID  = int(os.getenv("ADMIN_ID", "0"))

    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not set!")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    app.bot_data["admin_id"] = ADMIN_ID

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE:        [CallbackQueryHandler(set_language, pattern="^lang_")],
            MAIN_MENU: [
                CallbackQueryHandler(mobile, pattern="^mobile$"),
                CallbackQueryHandler(games,  pattern="^games$"),
                CallbackQueryHandler(apps,   pattern="^apps$"),
                CallbackQueryHandler(start,  pattern="^main_menu$"),
            ],
            MOBILE_NETWORK:  [
                CallbackQueryHandler(mobile, pattern="^net_"),
                CallbackQueryHandler(start,  pattern="^main_menu$"),
            ],
            MOBILE_TYPE:     [CallbackQueryHandler(mobile, pattern="^(mtype_|net_)")],
            MOBILE_PACKAGE:  [CallbackQueryHandler(mobile, pattern="^(mpkg_|mtype_|net_)")],
            MOBILE_NUMBER:   [
                MessageHandler(filters.TEXT & ~filters.COMMAND, mobile),
                CallbackQueryHandler(mobile, pattern="^mpkg_"),
            ],
            GAME_SELECT:     [
                CallbackQueryHandler(games, pattern="^game_"),
                CallbackQueryHandler(start, pattern="^main_menu$"),
            ],
            GAME_PACKAGE:    [CallbackQueryHandler(games, pattern="^(gpkg_|game_)")],
            GAME_ID:         [MessageHandler(filters.TEXT & ~filters.COMMAND, games)],
            APP_SELECT:      [
                CallbackQueryHandler(apps,  pattern="^app_"),
                CallbackQueryHandler(start, pattern="^main_menu$"),
            ],
            APP_PACKAGE:     [CallbackQueryHandler(apps,  pattern="^(apkg_|app_)")],
            PAYMENT_METHOD:  [
                CallbackQueryHandler(payment, pattern="^pay_\\d+$"),
                CallbackQueryHandler(start,   pattern="^main_menu$"),
            ],
            AWAITING_RECEIPT:[
                MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), receipt),
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            CallbackQueryHandler(main_menu, pattern="^main_menu$"),
        ],
        allow_reentry=True,
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("admin", admin))

    logger.info("✅ AfghanTopUpBot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
