import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application, MessageHandler, filters
from telegram.constants import ParseMode

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = ""
with open("Token.txt", 'r') as file:
    TOKEN = file.read()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_message = f"""Hello <b>{update.effective_user.first_name or update.effective_user.username}</b>
    this is the <a><b><i>echo bot</i></b></a> i will echo
    every thing you say including <i>images</i>, <i>emojis</i>, <i>Audio</i>,<i>Video</i> and <i>sticker</i>
    type what ever you want and i will echo it :)
    use <a>/help</a> for more detail
    """
    with open("users.txt",'a') as users:
        users.write(update.effective_user.username + update.effective_user.first_name)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message, parse_mode=ParseMode.HTML)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_menu = """
/start - let's set you up
/help - what can i help you with
/contact - this is the contact command
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_menu)


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # add logic to accept why the user need to contact with you
    # add logic to save the senders username
    await context.bot.send_message(chat_id=update.effective_chat.id, text="we will contact you soon")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[0].file_id
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file_id)
    elif update.message.audio:  # Check if the message contains an audio
        file_id = update.message.audio.file_id
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=file_id)
    elif update.message.sticker:
        file_id = update.message.sticker.file_id
        await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=file_id)
    elif update.message.video:
        file_id = update.message.video.file_id
        await context.bot.send_video(chat_id=update.effective_chat.id, video=file_id)
    elif update.message.document:
        file_id = update.message.document.file_id
        await context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)
    else:
        await update.message.reply_text(update.message.text)


if __name__ == '__main__':
    application = application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('contact', contact))
    application.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), echo))

    application.run_polling()
