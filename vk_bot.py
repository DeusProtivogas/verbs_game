import os
import random
from dotenv import load_dotenv

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_utils import create_api_key, detect_intent_texts



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
