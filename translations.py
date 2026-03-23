"""
Bilingual translations: Dari (fa) and English (en)
"""

TEXTS = {
    "welcome": {
        "fa": (
            "🇦🇫 به بوت افغان تاپ‌آپ خوش آمدید!\n\n"
            "لطفاً زبان خود را انتخاب کنید:"
        ),
        "en": (
            "🇦🇫 Welcome to Afghan TopUp Bot!\n\n"
            "Please select your language:"
        ),
    },
    "main_menu": {
        "fa": (
            "🏠 *منوی اصلی*\n\n"
            "لطفاً یک گزینه را انتخاب کنید:"
        ),
        "en": (
            "🏠 *Main Menu*\n\n"
            "Please select an option:"
        ),
    },
    "btn_mobile": {"fa": "📱 شارژ موبایل افغانستان", "en": "📱 Afghan Mobile Top-Up"},
    "btn_games":  {"fa": "🎮 گیم‌ها",                "en": "🎮 Games"},
    "btn_apps":   {"fa": "📲 برنامه‌ها",              "en": "📲 Apps & Subscriptions"},
    "btn_back":   {"fa": "🔙 بازگشت",                 "en": "🔙 Back"},
    "btn_main":   {"fa": "🏠 منوی اصلی",              "en": "🏠 Main Menu"},

    # Mobile
    "select_network": {
        "fa": "📶 لطفاً شبکه موبایل را انتخاب کنید:",
        "en": "📶 Please select a mobile network:",
    },
    "select_type": {
        "fa": "لطفاً نوع سرویس را انتخاب کنید:",
        "en": "Please select the service type:",
    },
    "btn_internet": {"fa": "🌐 بسته انترنت",  "en": "🌐 Internet Package"},
    "btn_calls":    {"fa": "📞 دقیقه تماس",   "en": "📞 Call Minutes"},
    "btn_credit":   {"fa": "💳 شارژ مستقیم",  "en": "💳 Direct Credit"},
    "select_package": {
        "fa": "📦 لطفاً بسته مورد نظر را انتخاب کنید:",
        "en": "📦 Please select a package:",
    },
    "enter_number": {
        "fa": "📱 لطفاً شماره موبایل مقصد (داخل افغانستان) را وارد کنید:\n\nمثال: 0700123456",
        "en": "📱 Please enter the destination mobile number (inside Afghanistan):\n\nExample: 0700123456",
    },
    "invalid_number": {
        "fa": "❌ شماره موبایل نامعتبر است. لطفاً دوباره وارد کنید.\nشماره باید ۱۰ رقم باشد.",
        "en": "❌ Invalid mobile number. Please try again.\nNumber must be 10 digits.",
    },

    # Games
    "select_game": {
        "fa": "🎮 لطفاً بازی مورد نظر را انتخاب کنید:",
        "en": "🎮 Please select a game:",
    },
    "select_game_package": {
        "fa": "💎 لطفاً بسته مورد نظر را انتخاب کنید:",
        "en": "💎 Please select a package:",
    },
    "enter_game_id": {
        "fa": (
            "🆔 لطفاً ID بازی خود را وارد کنید:\n\n"
            "📌 PUBG: Player ID را از پروفایل بازی پیدا کنید\n"
            "📌 Free Fire: UID را وارد کنید\n"
            "📌 Mobile Legends: ID + Server را وارد کنید"
        ),
        "en": (
            "🆔 Please enter your Game ID:\n\n"
            "📌 PUBG: Find Player ID from your game profile\n"
            "📌 Free Fire: Enter your UID\n"
            "📌 Mobile Legends: Enter ID + Server"
        ),
    },

    # Apps
    "select_app": {
        "fa": "📲 لطفاً برنامه مورد نظر را انتخاب کنید:",
        "en": "📲 Please select an app/subscription:",
    },

    # Payment
    "select_payment": {
        "fa": (
            "💳 *خلاصه سفارش:*\n"
            "{summary}\n\n"
            "لطفاً روش پرداخت را انتخاب کنید:"
        ),
        "en": (
            "💳 *Order Summary:*\n"
            "{summary}\n\n"
            "Please select a payment method:"
        ),
    },
    "payment_instructions": {
        "fa": (
            "✅ *روش پرداخت: {method}*\n\n"
            "💰 مبلغ: *{amount}*\n\n"
            "📤 لطفاً مبلغ را به حساب زیر پرداخت کنید:\n\n"
            "{account_info}\n\n"
            "⚠️ *بعد از پرداخت:*\n"
            "لطفاً اسکرین‌شات یا عکس رسید پرداخت را همراه با شماره تراکنش ارسال کنید."
        ),
        "en": (
            "✅ *Payment Method: {method}*\n\n"
            "💰 Amount: *{amount}*\n\n"
            "📤 Please send the payment to:\n\n"
            "{account_info}\n\n"
            "⚠️ *After payment:*\n"
            "Please send a screenshot or photo of the receipt along with the transaction ID."
        ),
    },
    "receipt_received": {
        "fa": (
            "✅ *رسید دریافت شد!*\n\n"
            "سفارش شما در حال بررسی است.\n"
            "پس از تأیید پرداخت، سرویس برای شما فعال می‌شود.\n\n"
            "🕐 زمان بررسی: ۵ تا ۳۰ دقیقه\n"
            "🆔 شماره سفارش: #{order_id}"
        ),
        "en": (
            "✅ *Receipt received!*\n\n"
            "Your order is being reviewed.\n"
            "Once payment is confirmed, your service will be activated.\n\n"
            "🕐 Review time: 5–30 minutes\n"
            "🆔 Order ID: #{order_id}"
        ),
    },
    "send_receipt_prompt": {
        "fa": "📸 لطفاً اسکرین‌شات رسید پرداخت یا شماره تراکنش را ارسال کنید:",
        "en": "📸 Please send a screenshot of the payment receipt or the transaction ID:",
    },
}


def t(key: str, lang: str, **kwargs) -> str:
    """Get translated text."""
    text = TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get("en", key))
    if kwargs:
        text = text.format(**kwargs)
    return text
