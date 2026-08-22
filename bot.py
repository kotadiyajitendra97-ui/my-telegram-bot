import os
import logging
import threading
import sqlite3
import asyncio
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import (
ApplicationBuilder,
ContextTypes,
CommandHandler,
MessageHandler,
ChatJoinRequestHandler,
filters
)

logging.basicConfig(
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)

web_app = Flask(name)

@web_app.route('/')
def home():
return "⚡ High-Performance Telegram Bot is running live!"

def run_web():
port = int(os.environ.get("PORT", 8080))
web_app.run(host="0.0.0.0", port=port)
DB_FILE = "enterprise_bot.db"

def init_db():
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY,
username TEXT,
first_name TEXT,
joined_date TEXT
)
''')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_id ON users(user_id)')
conn.commit()
conn.close()

def add_user_safe(user_id: int, username: str = "", first_name: str = ""):
try:
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
today_date = datetime.now().strftime("%Y-%m-%d")
cursor.execute(
"INSERT OR IGNORE INTO users (user_id, username, first_name, joined_date) VALUES (?, ?, ?, ?)",
(user_id, username, first_name, today_date)
)
conn.commit()
conn.close()
except Exception as e:
logger.error(f"Database error adding user: {e}")

def get_all_user_ids() -> list:
try:
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("SELECT user_id FROM users")
rows = cursor.fetchall()
conn.close()
return [row[0] for row in rows]
except Exception as e:
logger.error(f"Error fetching all users: {e}")
return []

def get_analytics_stats() -> dict:
try:
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
today_str = datetime.now().strftime("%Y-%m-%d")
    month_str = datetime.now().strftime("%Y-%m")
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE joined_date = ?", (today_str,))
    today_new = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE joined_date LIKE ?", (f"{month_str}%",))
    monthly_new = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total": total_users,
        "today": today_new,
        "monthly": monthly_new
    }
except Exception as e:
    logger.error(f"Error getting analytics: {e}")
    return {"total": 0, "today": 0, "monthly": 0}
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "YOUR_ADMIN_ID_HERE"))

async def handle_join_request(update: ChatJoinRequestHandler, context: ContextTypes.DEFAULT_TYPE):
user = update.chat_join_request.from_user
chat = update.chat
add_user_safe(user.id, user.username or "", user.first_name or "")

try:
    welcome_dm = (
        f"👋 Hello {user.first_name}!\n\n"
        f"Maine dekha ki aapne **{chat.title}** join karne ki request bheji hai.\n"
        "Aapki request par process chal raha hai. Tab tak aap mujhse yahan baat kar sakte hain!"
    )
    await context.bot.send_message(chat_id=user.id, text=welcome_dm)
except Exception as e:
    logger.error(f"Could not send DM to user {user.id}: {e}")
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
user = update.effective_user
add_user_safe(user.id, user.username or "", user.first_name or "")
if user.id == ADMIN_ID:
    await update.message.reply_text(
        "👑 **Admin Dashboard Active!**\n\n"
        "Commands:\n"
        "• `/stats` - Daily/Monthly user analytics dekhne ke liye\n"
        "• `/broadcast` - 30 seconds mein 1 Lakh+ users ko message bhejne ke liye\n"
        "• Admin panel se kisi bhi user ke message ka reply seedha de sakte hain."
    )
else:
    await update.message.reply_text(f"👋 Hello {user.first_name}! Main aapka personal assistance bot hoon.")
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.effective_user.id != ADMIN_ID:
await update.message.reply_text("❌ Yeh command sirf Admin ke liye hai!")
return
stats = get_analytics_stats()

report = (
    f"📊 **Bot Analytics Dashboard:**\n\n"
    f"👥 **Total Lifetime Users:** `{stats['total']}`\n"
    f"📅 **New Users Today:** `{stats['today']}`\n"
    f"📆 **New Users This Month:** `{stats['monthly']}`\n\n"
    f"⚡ Status: High-Performance Database Online"
)
await update.message.reply_text(report, parse_mode="Markdown")
async def send_single_user_message(bot, user_id, message_type, content_data, semaphore):
async with semaphore:
try:
if message_type == "photo":
await bot.send_photo(chat_id=user_id, photo=content_data["file_id"], caption=content_data["caption"])
elif message_type == "video":
await bot.send_video(chat_id=user_id, video=content_data["file_id"], caption=content_data["caption"])
else:
await bot.send_message(chat_id=user_id, text=content_data["text"])
return True
except Exception:
return False

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.effective_user.id != ADMIN_ID:
await update.message.reply_text("❌ Yeh command sirf Admin ke liye hai!")
return
user_ids = get_all_user_ids()
if not user_ids:
    await update.message.reply_text("⚠️ Database mein koi user nahi hai.")
    return

message = update.message
status_msg = await update.message.reply_text(f"🚀 High-Speed Broadcast shuru ho raha hai ({len(user_ids)} users)...")

message_type = "text"
content_data = {}

if message.photo:
    message_type = "photo"
    caption = message.caption or ""
    if caption.startswith("/broadcast"):
        caption = caption.replace("/broadcast", "").strip()
    content_data = {"file_id": message.photo[-1].file_id, "caption": caption}
elif message.video:
message_type = "video"
    caption = message.caption or ""
    if caption.startswith("/broadcast"):
        caption = caption.replace("/broadcast", "").strip()
    content_data = {"file_id": message.video.file_id, "caption": caption}
else:
    text = " ".join(context.args)
    if not text and message.reply_to_message:
        text = message.reply_to_message.text
    if not text:
        await status_msg.edit_text("❌ Kripya text likhein ya media ke sath caption mein /broadcast likhein.")
        return
    content_data = {"text": text}
semaphore = asyncio.Semaphore(100) 

tasks = [
    send_single_user_message(context.bot, uid, message_type, content_data, semaphore)
    for uid in user_ids
]

start_time = asyncio.get_event_loop().time()
results = await asyncio.gather(*tasks)
end_time = asyncio.get_event_loop().time()

success_count = sum(1 for r in results if r)
fail_count = len(user_ids) - success_count
duration = round(end_time - start_time, 2)
await status_msg.edit_text(
    f"⚡ **High-Speed Broadcast Complete!**\n\n"
    f"⏱️ Time Taken: `{duration} seconds`\n"
    f"✅ Successful: `{success_count}`\n"
    f"❌ Failed: `{fail_count}`",
    parse_mode="Markdown"
)
async def handle_user_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
message = update.message
if not message or not update.effective_user:
return
user = update.effective_user
add_user_safe(user.id, user.username or "", user.first_name or "")

if user.id == ADMIN_ID:
    if message.reply_to_message:
        try:
            replied_text = message.reply_to_message.text or message.reply_to_message.caption or ""
            if "User ID:" in replied_text:
                lines = replied_text.split("\n")
                for line in lines:
                    if "User ID:" in line:
                        target_user_id = int(line.split(":")[-1].strip())
                        await context.bot.copy_message(
                            chat_id=target_user_id,
                            from_chat_id=message.chat_id,
                            message_id=message.message_id
                        )
                        await message.reply_text("✅ Reply user tak bhej diya gaya hai!")
                        return
        except Exception as e:
            logger.error(f"Error sending reply to user: {e}")
    return
try:
    forward_text = (
        f"📩 **New Message Received!**\n"
        f"👤 Name: {user.first_name}\n"
        f"🆔 User ID: `{user.id}`\n"
        f"🔗 Username: @{user.username or 'None'}\n\n"
        f"Aap is message par 'Reply' karke user ko seedha jawab de sakte hain."
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text, parse_mode="Markdown")
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=message.chat_id,
        message_id=message.message_id
    )
except Exception as e:
    logger.error(f"Error forwarding user message to admin: {e}")
async def handle_media_broadcast_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message and update.message.caption and update.message.caption.startswith("/broadcast"):
await broadcast_command(update, context)

def main():
init_db()
threading.Thread(target=run_web, daemon=True).start()

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("stats", stats_command))
app.add_handler(CommandHandler("broadcast", broadcast_command))

app.add_handler(ChatJoinRequestHandler(handle_join_request))

app.add_handler(MessageHandler(filters.PHOTO & filters.CaptionRegex(r"^/broadcast"), handle_media_broadcast_real))
app.add_handler(MessageHandler(filters.VIDEO & filters.CaptionRegex(r"^/broadcast"), handle_media_broadcast_real))

app.add_handler(MessageHandler(~filters.COMMAND, handle_user_messages))

print("🔥 Enterprise 100k+ Bot successfully running with High-Speed Concurrency & Analytics!")
app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()



