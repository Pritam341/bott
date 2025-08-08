from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
import os

# ---- Configuration ----
TOKEN = '7769667614:AAGP7ei6UvquxrjiwBJZ0q7TpGn1aC7JaxI'
CHANNEL_ID = -1002180406156

# ---- Flask Setup ----
app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

# ---- States ----
DETAILS, LINK = range(2)

# ---- Bot Handlers ----
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Welcome! Use /post to create a job post.")

def post(update: Update, context: CallbackContext):
    update.message.reply_text("✍️ Send job details (company, role, etc.)")
    return DETAILS

def get_details(update: Update, context: CallbackContext):
    context.user_data["details"] = update.message.text
    update.message.reply_text("🔗 Send the apply link.")
    return LINK

def get_link(update: Update, context: CallbackContext):
    link = update.message.text.strip()
    details = context.user_data.get("details", "")

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📧 Apply Now", url=link)]])

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=details,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

    update.message.reply_text("✅ Job posted successfully!")
    return ConversationHandler.END

# ---- Conversation Handler ----
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("post", post)],
    states={
        DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],
        LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link)],
    },
    fallbacks=[],
)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(conv_handler)

# ---- Flask Routes ----
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "EURMjobs Bot is running!"
