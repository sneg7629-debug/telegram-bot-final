from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import time

TOKEN = "8787582148:AAE5khlUOu5Jdb0cQ1yi_MKRZxj7aVrIo4U"

pending_targets = {}
last_message_time = {}

keyboard = [["📨 Моє посилання", "ℹ️ Допомога"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if context.args:
        target_id = context.args[0]
        pending_targets[user_id] = target_id
        await update.message.reply_text("Напиши анонімне повідомлення 👇")
        return

    await update.message.reply_text("Вітаю! Обери дію 👇", reply_markup=markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text

    now = time.time()
    if user_id in last_message_time:
        if now - last_message_time[user_id] < 5:
            await update.message.reply_text("⏳ Почекай кілька секунд")
            return

    last_message_time[user_id] = now

    if text == "📨 Моє посилання":
        link = f"https://t.me/Inkognito_message_bot?start={user_id}"
        await update.message.reply_text(f"Твоє посилання:\n{link}")
        return

    if text == "ℹ️ Допомога":
        await update.message.reply_text("Поділись посиланням — і тобі зможуть писати анонімно.")
        return

    if user_id in pending_targets:
        target_id = pending_targets[user_id]

        await context.bot.send_message(
            chat_id=int(target_id),
            text=f"📩 Анонімне повідомлення:\n\n{text}"
        )

        await update.message.reply_text("✔ Повідомлення відправлено")
        del pending_targets[user_id]
        return

    await update.message.reply_text("Спочатку відкрий чиєсь посилання 👆")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено...")
    app.run_polling()


if __name__ == "__main__":
    main()