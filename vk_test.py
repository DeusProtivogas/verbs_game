import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(
        token="vk1.a.sLJ5PqkFaCtoo75m9ZFzVU1DAHcvkl2RG38dEaMGgdXp4WuTUR5GEXri0atTegwOza7kQYVpBRxRK0I5th27xj8vob_dv9W0YtHYtldfNav_FE5BgVfQapcdcO0SUnW9cmrxghFIQESjrB813MjTwldzZnQdx-fDmCTy0_YcsxPs8pz6AKut18ErqZzTZj54LK6ISGn5jcM5u2gFtekpmQ"
    )

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)

# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#         print('Новое сообщение:')
#         if event.to_me:
#             print('Для меня от: ', event.user_id)
#         else:
#             print('От меня для: ', event.user_id)
#         print('Текст:', event.text)