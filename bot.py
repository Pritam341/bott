import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# -------- Configuration --------
TOKEN = "7769667614:AAGP7ei6UvquxrjiwBJZ0q7TpGn1aC7JaxI"
CHANNEL_ID = -1002180406156

# -------- States --------
DETAILS, LINK = range(2)

# -------- Logging --------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# -------- Handlers --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to EURMjobs Bot! Use /post to send a job.")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Send the job post details (company, role, etc.)")
    return DETAILS

async def get_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["details"] = update.message.text
    await update.message.reply_text("🔗 Now send the apply link.")
    return LINK

async def get_link_and_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()
    details = context.user_data.get("details", "")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📧 Apply Now", url=link)]
    ])

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=details,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ Job posted successfully!")
    except Exception as e:
        logger.error("Failed to post job: %s", e)
        await update.message.reply_text("❌ Failed to post the job.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 Job posting cancelled.")
    return ConversationHandler.END

# -------- Main --------

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("post", post)],
        states={
            DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],
            LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link_and_post)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
