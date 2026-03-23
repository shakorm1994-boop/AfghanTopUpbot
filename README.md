# 🇦🇫 AfghanTopUpBot

بوت تلگرام برای فروش خدمات دیجیتال افغانستان
Telegram bot for Afghan digital top-up services

---

## 📋 خدمات / Services

| دسته / Category | توضیح / Description |
|---|---|
| 📱 شارژ موبایل | Roshan, MTN, Etisalat, Salaam |
| 🎮 گیم‌ها | PUBG UC, Free Fire Diamonds, Mobile Legends, COD CP |
| 📲 برنامه‌ها | Netflix, Google Play, Apple Gift Card |

---

## ⚙️ نصب و راه‌اندازی / Setup

### پیش‌نیازها / Requirements
- Python 3.10+
- pip

### مراحل / Steps

**1. نصب کتابخانه‌ها / Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. تنظیم متغیرها / Configure environment:**
```bash
cp .env.example .env
```
فایل `.env` را باز کنید و مقادیر زیر را وارد کنید:
- `BOT_TOKEN` → توکن بوت از @BotFather
- `ADMIN_ID` → شناسه تلگرام شما (از @userinfobot بگیرید)

**3. تنظیم حساب‌های پرداخت / Set up payment accounts:**

فایل `data/products.py` را باز کنید و بخش `PAYMENT_ACCOUNTS` را ویرایش کنید:
```python
PAYMENT_ACCOUNTS = {
    "USDT (TRC20)": {
        "fa": "آدرس USDT (TRC20):\n`YOUR_USDT_ADDRESS`",
        "en": "USDT (TRC20) Address:\n`YOUR_USDT_ADDRESS`",
    },
    "Binance Pay": {
        "fa": "Binance Pay ID:\n`YOUR_BINANCE_ID`",
        "en": "Binance Pay ID:\n`YOUR_BINANCE_ID`",
    },
    # ...
}
```

**4. اجرای بوت / Run the bot:**
```bash
python bot.py
```

---

## 🗂️ ساختار پروژه / Project Structure

```
AfghanTopUpBot/
├── bot.py                  # Main entry point
├── requirements.txt
├── .env.example
├── handlers/
│   ├── start.py            # Start + main menu
│   ├── mobile.py           # Mobile top-up flow
│   ├── games.py            # Games flow
│   ├── apps.py             # Apps & subscriptions flow
│   ├── payment.py          # Payment + receipt handling
│   └── admin.py            # Admin commands
├── data/
│   └── products.py         # All products, prices & payment accounts
└── utils/
    ├── states.py            # Conversation states
    └── translations.py      # Dari/English translations
```

---

## 💳 روش‌های پرداخت / Payment Methods

- USDT (TRC20)
- Binance Pay
- Papara
- M-Paisa / EasyPaisa

---

## 📱 نحوه عملکرد / How It Works

```
/start
  └─ انتخاب زبان (دری / English)
       └─ منوی اصلی
            ├─ 📱 شارژ موبایل
            │    ├─ انتخاب شبکه (Roshan/MTN/Etisalat/Salaam)
            │    ├─ انتخاب نوع (انترنت / دقیقه / شارژ مستقیم)
            │    ├─ انتخاب بسته + قیمت USDT
            │    ├─ وارد کردن شماره موبایل
            │    └─ پرداخت + ارسال رسید
            ├─ 🎮 گیم‌ها
            │    ├─ انتخاب بازی
            │    ├─ انتخاب بسته
            │    ├─ وارد کردن ID بازی
            │    └─ پرداخت + ارسال رسید
            └─ 📲 برنامه‌ها
                 ├─ انتخاب برنامه
                 ├─ انتخاب بسته
                 └─ پرداخت + ارسال رسید
```

---

## 🔔 نوتیفیکیشن ادمین / Admin Notifications

وقتی کاربر رسید پرداخت را ارسال کند، یک پیام کامل با اطلاعات سفارش به ادمین فرستاده می‌شود.

When a user sends a payment receipt, a complete order notification is forwarded to the admin.

---

## 🛠️ شخصی‌سازی / Customization

برای تغییر قیمت‌ها یا اضافه کردن محصول جدید، فایل `data/products.py` را ویرایش کنید.

To change prices or add new products, edit `data/products.py`.
