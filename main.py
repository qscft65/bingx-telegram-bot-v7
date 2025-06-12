import os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 下單", callback_data="order"),
         InlineKeyboardButton("❌ 不下單", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    expected_profit = 1.0
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"建議幣種：BTC-USDT\n倉位金額：20 USDT\n預估獲利：±{expected_profit * 0.03:.2f} USDT\n\n是否執行下單？",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "order":
        await query.edit_message_text("✅ 已下單")
    elif query.data == "cancel":
        await query.edit_message_text("❌ 已取消")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
