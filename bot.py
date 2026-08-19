import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, CommandHandler, MessageHandler, filters, ContextTypes

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running fine!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

BOT_TOKEN = "8845506695:AAFwfO_rgtGovrPYFPIWb0GgXDjb1h9mjbg"
VIDEO_FILE_ID = "YOUR_VIDEO_FILE_ID_HERE"

WELCOME_MESSAGE = """***Link 1
https://t.me/+561zT9_l49k3NjE1
https://t.me/+561zT9_l49k3NjE1
Link 2
https://t.me/+K5XjyxDE9Ts0MGVl
https://t.me/+K5XjyxDE9Ts0MGVl***"""

# User ID ko file mein save karne ka function
def save_user(chat_id):
    try:
        if not os.path.exists("users.txt"):
            with open("users.txt", "w") as f:
                f.write("")
        
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
        
        if str(chat_id) not in users:
            with open("users.txt", "a") as f:
                f.write(str(chat_id) + "\n")
    except Exception as e:
        print(f"Error saving user: {e}")

# Join request aane par yeh chalega
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_chat_id = request.user_chat_id
    
    # User ko save kar lo
    save_user(user_chat_id)
    
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

# Agar koi normal message kare toh bhi user save ho jaye
async def track_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        save_user(update.effective_chat.id)

# Sabhi users ko ek sath message bhejne ki command (/broadcast)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Aap yahan apni Telegram User ID daal sakte hain taaki sirf aap hi broadcast kar saken (Optional)
    # Filhaal koi bhi admin command use kar sakta hai
    message_text = " ".join(context.args)
    
    if not message_text:
        await update.message.reply_text("Kripya message bhi likhein. Example: /broadcast Hello everyone!")
        return

    if not os.path.exists("users.txt"):
        await update.message.reply_text("Abhi tak koi user saved nahi hai.")
        return

    with open("users.txt", "r") as f:
        users = f.read().splitlines()

    success_count = 0
    fail_count = 0

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message_text)
            success_count += 1
        except Exception as e:
            fail_count += 1

    await update.message.reply_text(f"Broadcast poora ho gaya!\nSafarish: {success_count}\nFailed: {fail_count}")

def main():
    threading.Thread(target=run_web, daemon=True).start()
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), track_messages))
    
    print("Bot Free Hosting Par Start Ho Gaya!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
