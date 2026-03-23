"""Games handler."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.translations import t
from utils.states import MAIN_MENU, GAME_SELECT, GAME_PACKAGE, GAME_ID, PAYMENT_METHOD
from data.products import GAMES, GAME_PACKAGES


def _lang(c): return c.user_data.get("lang", "fa")


async def games_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = _lang(context)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        data = query.data
    else:
        return await _handle_game_id(update, context)

    # ── Step 1: game list ─────────────────────────────────────────────────────
    if data == "games":
        keyboard = [
            [InlineKeyboardButton(info[lang], callback_data=f"game_{key}")]
            for key, info in GAMES.items()
        ]
        keyboard.append([InlineKeyboardButton(t("btn_main", lang), callback_data="main_menu")])
        await query.edit_message_text(
            t("select_game", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return GAME_SELECT

    # ── Step 2: package list ──────────────────────────────────────────────────
    if data.startswith("game_") and not data.startswith("game_back"):
        game = data.replace("game_", "")
        context.user_data["selected_game"] = game
        packages = GAME_PACKAGES.get(game, [])

        keyboard = [
            [InlineKeyboardButton(
                f"{p[lang]}  —  {p['price']} USDT",
                callback_data=f"gpkg_{p['id']}"
            )]
            for p in packages
        ]
        keyboard.append([InlineKeyboardButton(t("btn_back", lang), callback_data="games")])
        game_name = GAMES.get(game, {}).get(lang, game)
        await query.edit_message_text(
            f"{game_name}\n\n{t('select_game_package', lang)}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return GAME_PACKAGE

    if data == "game_back":
        # re-show game list
        keyboard = [
            [InlineKeyboardButton(info[lang], callback_data=f"game_{key}")]
            for key, info in GAMES.items()
        ]
        keyboard.append([InlineKeyboardButton(t("btn_main", lang), callback_data="main_menu")])
        await query.edit_message_text(
            t("select_game", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return GAME_SELECT

    # ── Step 3: ask game ID ───────────────────────────────────────────────────
    if data.startswith("gpkg_"):
        pkg_id = data.replace("gpkg_", "")
        game   = context.user_data.get("selected_game", "pubg")
        pkg    = next((p for p in GAME_PACKAGES.get(game, []) if p["id"] == pkg_id), None)
        if pkg:
            context.user_data["selected_package"] = pkg
            context.user_data["order_type"] = "game"

        await query.edit_message_text(t("enter_game_id", lang))
        return GAME_ID

    return GAME_SELECT


async def _handle_game_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang    = _lang(context)
    game_id = update.message.text.strip()
    game    = context.user_data.get("selected_game", "")
    pkg     = context.user_data.get("selected_package", {})

    context.user_data["game_id"] = game_id
    game_name = GAMES.get(game, {}).get(lang, game)

    summary_lines = [
        f"{'بازی' if lang == 'fa' else 'Game'}: {game_name}",
        f"{'بسته' if lang == 'fa' else 'Package'}: {pkg.get(lang, '')}",
        f"{'شناسه بازی' if lang == 'fa' else 'Game ID'}: {game_id}",
        f"{'مبلغ' if lang == 'fa' else 'Amount'}: {pkg.get('price', 0)} USDT",
    ]
    context.user_data["order_summary"] = "\n".join(summary_lines)
    context.user_data["order_amount"]  = f"{pkg.get('price', 0)} USDT"

    from handlers.payment import show_payment_methods
    return await show_payment_methods(update, context)
