import os
import logging

from dotenv import load_dotenv
from google.cloud import dialogflow
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def create_api_key(project_id: str, suffix: str) -> Key:
    """
    Creates and restrict an API key. Add the suffix for uniqueness.

    1. Before running this sample,
      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    2. Make sure you have the necessary permission to create API keys.

    Args:
        project_id: Google Cloud project id.

    Returns:
        response: Returns the created API Key.
    """
    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    # Initialize request and set arguments.
    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    # Make the request and wait for the operation to complete.
    response = client.create_key(request=request).result()

    # print(f"Successfully created an API key: {response.name}")
    # For authenticating with the API key, use the value in "response.key_string".
    # To restrict the usage of this API key, use the value in "response.name".
    return response

def detect_intent_texts(project_id, session_id, text, language_code='en-US'):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    answer = response.query_result.fulfillment_text
    print("Fulfillment text: {}\n".format(answer))
    return answer


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
