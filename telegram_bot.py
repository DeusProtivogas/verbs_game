import os
import logging

from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow_utils import create_api_key, detect_intent_texts

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""

    update.message.reply_text(
        f'Бот запускается, подождите...',
    )
    user = update.effective_user
    context.user_data["user"] = user
    # print(context.user_data["user"]['username'])
    context.user_data['project_id'] = os.getenv('PROJECT_ID')
    context.user_data['key'] = create_api_key(
        context.user_data['project_id'],
        context.user_data["user"]['username'],
    ).name

    update.message.reply_markdown_v2(
        fr'Привет, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    user_id = context.user_data['user']['id']
    text = update.message.text

    answer = detect_intent_texts(context.user_data['project_id'], str(user_id), text)

    update.message.reply_text(answer)


def main() -> None:
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    # print(telegram_token)

    # project_id = os.getenv('PROJECT_ID')
    # key = create_api_key(project_id, 'abc').name
    # key = os.getenv('API_KEY')
    # detect_intent_texts(project_id, '123456789', ['Привет', 'Хай'])
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(telegram_token)

    # print(updater.message.chat_id)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    load_dotenv()
    main()
