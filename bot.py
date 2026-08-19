    # Agar admin khud message bhej raha hai, toh forward mat karo
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

BOT_TOKEN = "8845506695:AAHCLbvbgkgLxsHYHuDidF2xk0HP3qI-n7I"
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

# Normal message par user save karna
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

BOT_TOKEN = "8845506695:AAHCLbvbgkgLxsHYHuDidF2xk0HP3qI-n7I"
VIDEO_FILE_ID = "YOUR_VIDEO_FILE_ID_HERE"

# Aapki Admin ID yahan set kar di gayi hai
ADMIN_ID = 6802793034

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
    save_user(user_chat_id)
    
    try:
        if VIDEO_FILE_ID and VIDEO_FILE_ID != "YOUR_VIDEO_FILE_ID_HERE":
            await context.bot.send_video(
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

BOT_TOKEN = "8845506695:AAHCLbvbgkgLxsHYHuDidF2xk0HP3qI-n7I"
VIDEO_FILE_ID = "YOUR_VIDEO_FILE_ID_HERE"

ADMIN_ID = 6802793034

WELCOME_MESSAGE = """***Link 1
https://t.me/+561zT9_l49k3NjE1
https://t.me/+561zT9_l49k3NjE1
Link 2
https://t.me/+K5XjyxDE9Ts0MGVl
https://t.me/+K5XjyxDE9Ts0MGVl***"""

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

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_chat_id = request.user_chat_id
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

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.from_user:
        return

    user = message.from_user
    user_chat_id = user.id
    
    save_user(user_chat_id)

    if user_chat_id == ADMIN_ID:
        return

    try:
        header_text = f"📩 Naya Message Aaya Hai!\n👤 Naam: {user.first_name}\n🆔 User ID: `{user_chat_id}`"
        await context.bot.send_message(chat_id=ADMIN_ID, text=header_text, parse_mode="Markdown")
        
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=user_chat_id,
            message_id=message.message_id
        )
    except Exception as e:
        print(f"Error forwarding message: {e}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Aapke paas is command ko use karne ki permission nahi hai.")
        return

    if not os.path.exists("users.txt"):
        await update.message.reply_text("Abhi tak koi user saved nahi hai.")
        return

    with open("users.txt", "r") as f:
        users = f.read().splitlines()

    if not users:
        await update.message.reply_text("Users list khali hai.")
        return

    success_count = 0
    fail_count = 0
    message = update.message

    if message.photo:
        photo_file_id = message.photo[-1].file_id
        caption = message.caption or ""
        if caption.startswith("/broadcast"):
            caption = caption.replace("/broadcast", "").strip()

        for user_id in users:
            try:
                await context.bot.send_photo(chat_id=int(user_id), photo=photo_file_id, caption=caption)
                success_count += 1
            except Exception:
                fail_count += 1

    elif message.video:
        video_file_id = message.video.file_id
        caption = message.caption or ""
        if caption.startswith("/broadcast"):
            caption = caption.replace("/broadcast", "").strip()

        for user_id in users:
            try:
                await context.bot.send_video(chat_id=int(user_id), video=video_file_id, caption=caption)
                success_count += 1
            except Exception:
                fail_count += 1

    else:
        message_text = " ".join(context.args)
        if not message_text:
            await update.message.reply_text("Kripya message likhein ya Photo/Video ke sath caption mein /broadcast likhein.")
            return

        for user_id in users:
            try:
                await context.bot.send_message(chat_id=int(user_id), text=message_text)
                success_count += 1
            except Exception:
                fail_count += 1

    await update.message.reply_text(f"Broadcast poora ho gaya!\nSuccessful: {success_count}\nFailed: {fail_count}")

async def handle_media_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.caption and message.caption.startswith("/broadcast"):
        await broadcast(update, context)

def main():
    threading.Thread(target=run_web, daemon=True).start()
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    app.add_handler(CommandHandler("broadcast", broadcast))
    
    app.add_handler(MessageHandler(filters.PHOTO & filters.CaptionRegex(r"^/broadcast"), handle_media_broadcast))
    app.add_handler(MessageHandler(filters.VIDEO & filters.CaptionRegex(r"^/broadcast"), handle_media_broadcast))
    
    app.add_handler(MessageHandler(~filters.COMMAND, forward_to_admin))
    
    print("Bot Free Hosting Par Start Ho Gaya!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
