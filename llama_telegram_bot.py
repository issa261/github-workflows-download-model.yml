from llama_cpp import Llama
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "0"))
MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q8_0.gguf"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ الملف {MODEL_PATH} غير موجود في مستودعك.")

llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("⛔️ غير مصرح لك.")
        return
    await update.message.reply_text("🤖 أهلاً! أرسل سؤالك.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("⛔️ غير مصرح لك.")
        return
    prompt = update.message.text
    response = llm(prompt, max_tokens=200)["choices"][0]["text"].strip()
    await update.message.reply_text(response)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
