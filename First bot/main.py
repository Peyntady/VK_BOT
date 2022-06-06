import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token="7450d860be2562a49962c50a4616fb6cdb985c0546fc8c5f217a88164b59bc2527d58c7efe7f2e69ade64")
session_api= vk_session.get_api()
longpool = VkLongPoll(vk_session)

def send_some_msg(id, some_text):
    vk_session.method("messages.send", {"user_id":id, "message":some_text,"random_id":0})

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == "привет":
                send_some_msg(id, "привет дружище!")
