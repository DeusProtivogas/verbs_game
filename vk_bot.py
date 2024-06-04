import os
import random
from dotenv import load_dotenv

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from google.cloud import dialogflow
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key

def create_api_key(project_id: str, suffix: str) -> Key:
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()

    return response

def detect_intent_texts(project_id, session_id, text, language_code='en-US'):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if response.query_result.intent.is_fallback:
        return ""
    answer = response.query_result.fulfillment_text
    return answer



def send_reply(event, vk_api, dialogflow_key):

    reply = detect_intent_texts(
        dialogflow_key,
        str(event.user_id),
        event.text
    )

    if reply:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply,
            random_id=random.randint(1,1000)
        )


if __name__ == "__main__":
    load_dotenv()

    project_id = os.getenv('PROJECT_ID')
    dialogflow_key = create_api_key(project_id, "abc").name

    vk_session = vk.VkApi(
        token=os.getenv('VK_KEY')
    )

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_reply(event, vk_api, project_id)
