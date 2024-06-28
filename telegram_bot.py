import os
import logging

from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, CallbackContext

from dialogflow_utils import detect_intent_texts

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Бот запускается, подождите...',
    )
    user = update.effective_user

    update.message.reply_markdown_v2(
        fr'Привет, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def answer_user(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    answer, is_fallback = detect_intent_texts(
        os.getenv('PROJECT_ID'),
        str(update.effective_user.id),
        text
    )

    update.message.reply_text(answer)


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command, answer_user
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
