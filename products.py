"""
Products catalog for AfghanTopUpBot
All prices in USDT
"""

# ── Payment Accounts ──────────────────────────────────────────────────────────
PAYMENT_ACCOUNTS = {
    "USDT (TRC20)": {
        "fa": "آدرس USDT (TRC20):\n`TYourUSDTAddressHere1234567890`",
        "en": "USDT (TRC20) Address:\n`TYourUSDTAddressHere1234567890`",
    },
    "Binance Pay": {
        "fa": "Binance Pay ID:\n`123456789`\nیا اسکن QR کد زیر",
        "en": "Binance Pay ID:\n`123456789`\nor scan QR code below",
    },
    "Papara": {
        "fa": "شماره Papara:\n`0500-000-0000`\nنام: Your Name",
        "en": "Papara Number:\n`0500-000-0000`\nName: Your Name",
    },
    "M-Paisa / EasyPaisa": {
        "fa": "شماره M-Paisa / EasyPaisa:\n`03XX-XXXXXXX`",
        "en": "M-Paisa / EasyPaisa Number:\n`03XX-XXXXXXX`",
    },
}

# ── Mobile Networks ───────────────────────────────────────────────────────────
NETWORKS = {
    "roshan": {"fa": "🟢 روشن (Roshan)", "en": "🟢 Roshan"},
    "mtn":    {"fa": "🟡 MTN افغانستان",  "en": "🟡 MTN Afghanistan"},
    "etisalat":{"fa":"🔵 اتصالات",        "en": "🔵 Etisalat"},
    "salaam": {"fa": "🟠 سلام",           "en": "🟠 Salaam"},
}

MOBILE_PACKAGES = {
    "roshan": {
        "internet": [
            {"id": "r_net_1",  "fa": "۱ GB - ۱ روز",    "en": "1 GB – 1 Day",    "price": 0.50},
            {"id": "r_net_2",  "fa": "۵ GB - ۷ روز",    "en": "5 GB – 7 Days",   "price": 2.00},
            {"id": "r_net_3",  "fa": "۱۰ GB - ۳۰ روز",  "en": "10 GB – 30 Days", "price": 3.50},
            {"id": "r_net_4",  "fa": "۲۰ GB - ۳۰ روز",  "en": "20 GB – 30 Days", "price": 6.00},
            {"id": "r_net_5",  "fa": "نامحدود - ۷ روز",  "en": "Unlimited – 7 Days","price": 4.00},
        ],
        "calls": [
            {"id": "r_call_1", "fa": "۳۰ دقیقه",   "en": "30 Minutes",  "price": 0.60},
            {"id": "r_call_2", "fa": "۶۰ دقیقه",   "en": "60 Minutes",  "price": 1.00},
            {"id": "r_call_3", "fa": "۱۲۰ دقیقه",  "en": "120 Minutes", "price": 1.80},
            {"id": "r_call_4", "fa": "۳۰۰ دقیقه",  "en": "300 Minutes", "price": 4.00},
        ],
        "credit": [
            {"id": "r_cr_1",  "fa": "۵۰ افغانی",   "en": "50 AFN",  "price": 0.60},
            {"id": "r_cr_2",  "fa": "۱۰۰ افغانی",  "en": "100 AFN", "price": 1.20},
            {"id": "r_cr_3",  "fa": "۲۰۰ افغانی",  "en": "200 AFN", "price": 2.30},
            {"id": "r_cr_4",  "fa": "۵۰۰ افغانی",  "en": "500 AFN", "price": 5.50},
        ],
    },
    "mtn": {
        "internet": [
            {"id": "m_net_1", "fa": "۱ GB - ۱ روز",    "en": "1 GB – 1 Day",    "price": 0.50},
            {"id": "m_net_2", "fa": "۵ GB - ۷ روز",    "en": "5 GB – 7 Days",   "price": 1.90},
            {"id": "m_net_3", "fa": "۱۰ GB - ۳۰ روز",  "en": "10 GB – 30 Days", "price": 3.40},
            {"id": "m_net_4", "fa": "۲۵ GB - ۳۰ روز",  "en": "25 GB – 30 Days", "price": 7.00},
        ],
        "calls": [
            {"id": "m_call_1","fa": "۳۰ دقیقه",  "en": "30 Minutes",  "price": 0.55},
            {"id": "m_call_2","fa": "۶۰ دقیقه",  "en": "60 Minutes",  "price": 1.00},
            {"id": "m_call_3","fa": "۲۰۰ دقیقه", "en": "200 Minutes", "price": 3.00},
        ],
        "credit": [
            {"id": "m_cr_1", "fa": "۵۰ افغانی",  "en": "50 AFN",  "price": 0.60},
            {"id": "m_cr_2", "fa": "۱۰۰ افغانی", "en": "100 AFN", "price": 1.20},
            {"id": "m_cr_3", "fa": "۲۵۰ افغانی", "en": "250 AFN", "price": 2.80},
            {"id": "m_cr_4", "fa": "۵۰۰ افغانی", "en": "500 AFN", "price": 5.50},
        ],
    },
    "etisalat": {
        "internet": [
            {"id": "e_net_1", "fa": "۲ GB - ۳ روز",    "en": "2 GB – 3 Days",   "price": 0.80},
            {"id": "e_net_2", "fa": "۸ GB - ۱۵ روز",   "en": "8 GB – 15 Days",  "price": 2.50},
            {"id": "e_net_3", "fa": "۱۵ GB - ۳۰ روز",  "en": "15 GB – 30 Days", "price": 4.50},
        ],
        "calls": [
            {"id": "e_call_1","fa": "۵۰ دقیقه",  "en": "50 Minutes",  "price": 0.80},
            {"id": "e_call_2","fa": "۱۰۰ دقیقه", "en": "100 Minutes", "price": 1.50},
        ],
        "credit": [
            {"id": "e_cr_1", "fa": "۱۰۰ افغانی", "en": "100 AFN", "price": 1.20},
            {"id": "e_cr_2", "fa": "۲۰۰ افغانی", "en": "200 AFN", "price": 2.30},
            {"id": "e_cr_3", "fa": "۵۰۰ افغانی", "en": "500 AFN", "price": 5.50},
        ],
    },
    "salaam": {
        "internet": [
            {"id": "s_net_1", "fa": "۱ GB - ۱ روز",    "en": "1 GB – 1 Day",    "price": 0.50},
            {"id": "s_net_2", "fa": "۵ GB - ۷ روز",    "en": "5 GB – 7 Days",   "price": 2.00},
            {"id": "s_net_3", "fa": "۱۰ GB - ۳۰ روز",  "en": "10 GB – 30 Days", "price": 3.50},
        ],
        "calls": [
            {"id": "s_call_1","fa": "۳۰ دقیقه",  "en": "30 Minutes",  "price": 0.60},
            {"id": "s_call_2","fa": "۱۲۰ دقیقه", "en": "120 Minutes", "price": 1.80},
        ],
        "credit": [
            {"id": "s_cr_1", "fa": "۵۰ افغانی",  "en": "50 AFN",  "price": 0.60},
            {"id": "s_cr_2", "fa": "۲۰۰ افغانی", "en": "200 AFN", "price": 2.30},
        ],
    },
}

# ── Games ─────────────────────────────────────────────────────────────────────
GAMES = {
    "pubg": {"fa": "🎯 PUBG Mobile (UC)", "en": "🎯 PUBG Mobile (UC)"},
    "freefire": {"fa": "🔥 Free Fire (الماس)", "en": "🔥 Free Fire (Diamonds)"},
    "mlbb": {"fa": "⚔️ Mobile Legends (الماس)", "en": "⚔️ Mobile Legends (Diamonds)"},
    "cod": {"fa": "🔫 Call of Duty Mobile (CP)", "en": "🔫 Call of Duty Mobile (CP)"},
}

GAME_PACKAGES = {
    "pubg": [
        {"id": "pu_60",   "fa": "۶۰ UC",    "en": "60 UC",    "price": 0.90},
        {"id": "pu_180",  "fa": "۱۸۰ UC",   "en": "180 UC",   "price": 2.50},
        {"id": "pu_325",  "fa": "۳۲۵ UC",   "en": "325 UC",   "price": 4.50},
        {"id": "pu_660",  "fa": "۶۶۰ UC",   "en": "660 UC",   "price": 8.50},
        {"id": "pu_1800", "fa": "۱۸۰۰ UC",  "en": "1800 UC",  "price": 22.00},
        {"id": "pu_3850", "fa": "۳۸۵۰ UC",  "en": "3850 UC",  "price": 44.00},
        {"id": "pu_8100", "fa": "۸۱۰۰ UC",  "en": "8100 UC",  "price": 88.00},
    ],
    "freefire": [
        {"id": "ff_100",  "fa": "۱۰۰ الماس",  "en": "100 Diamonds",  "price": 1.00},
        {"id": "ff_310",  "fa": "۳۱۰ الماس",  "en": "310 Diamonds",  "price": 3.00},
        {"id": "ff_520",  "fa": "۵۲۰ الماس",  "en": "520 Diamonds",  "price": 5.00},
        {"id": "ff_1060", "fa": "۱۰۶۰ الماس", "en": "1060 Diamonds", "price": 9.50},
        {"id": "ff_2180", "fa": "۲۱۸۰ الماس", "en": "2180 Diamonds", "price": 19.00},
        {"id": "ff_5600", "fa": "۵۶۰۰ الماس", "en": "5600 Diamonds", "price": 47.00},
    ],
    "mlbb": [
        {"id": "ml_86",   "fa": "۸۶ الماس",   "en": "86 Diamonds",   "price": 1.20},
        {"id": "ml_172",  "fa": "۱۷۲ الماس",  "en": "172 Diamonds",  "price": 2.30},
        {"id": "ml_257",  "fa": "۲۵۷ الماس",  "en": "257 Diamonds",  "price": 3.40},
        {"id": "ml_514",  "fa": "۵۱۴ الماس",  "en": "514 Diamonds",  "price": 6.50},
        {"id": "ml_1029", "fa": "۱۰۲۹ الماس", "en": "1029 Diamonds", "price": 12.50},
        {"id": "ml_2195", "fa": "۲۱۹۵ الماس", "en": "2195 Diamonds", "price": 25.00},
    ],
    "cod": [
        {"id": "cod_80",   "fa": "۸۰ CP",    "en": "80 CP",    "price": 1.00},
        {"id": "cod_400",  "fa": "۴۰۰ CP",   "en": "400 CP",   "price": 4.80},
        {"id": "cod_800",  "fa": "۸۰۰ CP",   "en": "800 CP",   "price": 9.30},
        {"id": "cod_2000", "fa": "۲۰۰۰ CP",  "en": "2000 CP",  "price": 22.00},
        {"id": "cod_5000", "fa": "۵۰۰۰ CP",  "en": "5000 CP",  "price": 52.00},
    ],
}

# ── Apps & Subscriptions ──────────────────────────────────────────────────────
APPS = {
    "netflix": {"fa": "🎬 Netflix اشتراک", "en": "🎬 Netflix Subscription"},
    "google":  {"fa": "🎁 Google Play Gift Card", "en": "🎁 Google Play Gift Card"},
    "apple":   {"fa": "🍎 Apple Gift Card",        "en": "🍎 Apple Gift Card"},
}

APP_PACKAGES = {
    "netflix": [
        {"id": "nf_1m_s",  "fa": "۱ ماه - استاندارد",  "en": "1 Month – Standard",  "price": 8.00},
        {"id": "nf_1m_p",  "fa": "۱ ماه - پریمیوم",    "en": "1 Month – Premium",   "price": 13.00},
        {"id": "nf_3m_s",  "fa": "۳ ماه - استاندارد",  "en": "3 Months – Standard", "price": 22.00},
        {"id": "nf_3m_p",  "fa": "۳ ماه - پریمیوم",    "en": "3 Months – Premium",  "price": 36.00},
        {"id": "nf_6m_p",  "fa": "۶ ماه - پریمیوم",    "en": "6 Months – Premium",  "price": 68.00},
        {"id": "nf_12m_p", "fa": "۱۲ ماه - پریمیوم",   "en": "12 Months – Premium", "price": 130.00},
    ],
    "google": [
        {"id": "gp_5",  "fa": "$۵ گیفت کارت",   "en": "$5 Gift Card",   "price": 5.50},
        {"id": "gp_10", "fa": "$۱۰ گیفت کارت",  "en": "$10 Gift Card",  "price": 10.80},
        {"id": "gp_25", "fa": "$۲۵ گیفت کارت",  "en": "$25 Gift Card",  "price": 26.50},
        {"id": "gp_50", "fa": "$۵۰ گیفت کارت",  "en": "$50 Gift Card",  "price": 52.00},
    ],
    "apple": [
        {"id": "ap_5",  "fa": "$۵ گیفت کارت",   "en": "$5 Gift Card",   "price": 5.80},
        {"id": "ap_10", "fa": "$۱۰ گیفت کارت",  "en": "$10 Gift Card",  "price": 11.20},
        {"id": "ap_25", "fa": "$۲۵ گیفت کارت",  "en": "$25 Gift Card",  "price": 27.00},
        {"id": "ap_50", "fa": "$۵۰ گیفت کارت",  "en": "$50 Gift Card",  "price": 53.00},
    ],
}


def get_package_by_id(pkg_id: str) -> dict | None:
    """Find any package by its ID across all catalogs."""
    all_catalogs = [
        *[pkgs for net in MOBILE_PACKAGES.values() for pkgs in net.values()],
        *GAME_PACKAGES.values(),
        *APP_PACKAGES.values(),
    ]
    for catalog in all_catalogs:
        for pkg in catalog:
            if pkg["id"] == pkg_id:
                return pkg
    return None
