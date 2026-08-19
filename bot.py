import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running fine!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

BOT_TOKEN = "8845506695:AAHTfV1aEFsByx6RzZvgK5pbRlPp_MqpW-g"
VIDEO_FILE_ID = "YOUR_VIDEO_FILE_ID_HERE"

WELCOME_MESSAGE = """***Link 1
https://t.me/+56lZT9_l49k3NjE1
https://t.me/+56lZT9_l49k3NjE1

Link 2
https://t.me/+K5XjyxDE9Ts0MGVl
https://t.me/+K5XjyxDE9Ts0MGVl***"""

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_chat_id = request.user_chat_id
    try:
        if VIDEO_FILE_ID and VIDEO_FILE_ID != "YOUR_VIDEO_FILE_ID_HERE":
            await context.bot.send_video(
                chat_id=user_chat_id,
                video=VIDEO_FILE_ID,
                caption=WELCOME_MESSAGE
            )
        else:
            await context.bot.send_message(
                chat_id=user_chat_id,
                text=WELCOME_MESSAGE
            )
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Flask server ko background thread mein start karna
    threading.Thread(target=run_web, daemon=True).start()
    
    # Telegram Bot application build karna
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    
    print("Bot Free Hosting Par Start Ho Gaya!")
    # Bot polling start karna
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
