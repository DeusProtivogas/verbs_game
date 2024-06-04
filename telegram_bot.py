import os
import logging

from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow_utils import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f'Бот запускается, подождите...',
    )
    user = update.effective_user
    context.user_data["user"] = user

    update.message.reply_markdown_v2(
        fr'Привет, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def answer_user(update: Update, context: CallbackContext) -> None:
    user_id = context.user_data['user']['id']
    text = update.message.text

    answer = detect_intent_texts(os.getenv('PROJECT_ID'), str(user_id), text)

    update.message.reply_text(answer)


def main() -> None:
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer_user))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
