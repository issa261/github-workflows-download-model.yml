from llama_cpp import Llama
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

BOT_TOKEN = os.getenv("7537714477:AAGbdxU0pvQEpBK2Ee5qDguOGcTQPsdIp8o")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "6837315281"))
MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q8_0.gguf"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ الملف {MODEL_PATH} غير موجود في مستودعك.")

llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

def start(update: Update, context):
    if update.effective_user.id != ALLOWED_USER_ID:
        update.message.reply_text("⛔️ غير مصرح لك.")
        return
    update.message.reply_text("🤖 أهلاً! أرسل سؤالك.")

def handle(update: Update, context):
    if update.effective_user.id != ALLOWED_USER_ID:
        update.message.reply_text("⛔️ غير مصرح لك.")
        return
    prompt = update.message.text
    response = llm(prompt, max_tokens=200)["choices"][0]["text"].strip()
    update.message.reply_text(response)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
