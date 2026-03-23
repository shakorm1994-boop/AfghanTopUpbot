"""Apps & Subscriptions handler."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.translations import t
from utils.states import MAIN_MENU, APP_SELECT, APP_PACKAGE, PAYMENT_METHOD
from data.products import APPS, APP_PACKAGES


def _lang(c): return c.user_data.get("lang", "fa")


async def apps_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = _lang(context)

    if not update.callback_query:
        return APP_SELECT

    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "apps":
        keyboard = [
            [InlineKeyboardButton(info[lang], callback_data=f"app_{key}")]
            for key, info in APPS.items()
        ]
        keyboard.append([InlineKeyboardButton(t("btn_main", lang), callback_data="main_menu")])
        await query.edit_message_text(
            t("select_app", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return APP_SELECT

    if data.startswith("app_") and not data.startswith("app_back"):
        app = data.replace("app_", "")
        context.user_data["selected_app"] = app
        packages = APP_PACKAGES.get(app, [])
        keyboard = [
            [InlineKeyboardButton(
                f"{p[lang]}  —  {p['price']} USDT",
                callback_data=f"apkg_{p['id']}"
            )]
            for p in packages
        ]
        keyboard.append([InlineKeyboardButton(t("btn_back", lang), callback_data="apps")])
        app_name = APPS.get(app, {}).get(lang, app)
        await query.edit_message_text(
            f"{app_name}\n\n{t('select_package', lang)}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return APP_PACKAGE

    if data == "app_back":
        keyboard = [
            [InlineKeyboardButton(info[lang], callback_data=f"app_{key}")]
            for key, info in APPS.items()
        ]
        keyboard.append([InlineKeyboardButton(t("btn_main", lang), callback_data="main_menu")])
        await query.edit_message_text(
            t("select_app", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return APP_SELECT

    if data.startswith("apkg_"):
        pkg_id = data.replace("apkg_", "")
        app    = context.user_data.get("selected_app", "netflix")
        pkg    = next((p for p in APP_PACKAGES.get(app, []) if p["id"] == pkg_id), None)
        if pkg:
            context.user_data["selected_package"] = pkg
            context.user_data["order_type"] = "app"

        app_name = APPS.get(app, {}).get(lang, app)
        summary_lines = [
            f"{'برنامه' if lang == 'fa' else 'App'}: {app_name}",
            f"{'بسته' if lang == 'fa' else 'Package'}: {pkg.get(lang, '') if pkg else ''}",
            f"{'مبلغ' if lang == 'fa' else 'Amount'}: {pkg.get('price', 0) if pkg else 0} USDT",
        ]
        context.user_data["order_summary"] = "\n".join(summary_lines)
        context.user_data["order_amount"]  = f"{pkg.get('price', 0) if pkg else 0} USDT"

        from handlers.payment import show_payment_methods
        return await show_payment_methods(update, context)

    return APP_SELECT
