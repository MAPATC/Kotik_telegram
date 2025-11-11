import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

URL_API = os.getenv("URL")
CAT_URL_API = os.getenv("CATS_API")
BOT_TOKEN = os.getenv("TOKEN")
PARAM = "/getUpdates"


offset = -2
chat_id: int
kotik: requests.Response


def answer(update_id: int, chat__id: int, user__text: str, cat: requests.Response) -> None:

    print('Был получен апдейт N:', update_id)

    requests.get(
        f'{URL_API}{BOT_TOKEN}/sendMessage?chat_id={chat__id}&text=Давай без "{user__text}", это плохо, лучше посмотри на котика!')
    if cat.status_code == 200:
        photo_link = cat.json()[0]['url']
        requests.get(
            f"{URL_API}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={photo_link}")
    else:
        requests.get(
            f"{URL_API}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Котика нету :(")


while True:
    start = time.time()

    updates = requests.get(
        f"{URL_API}{BOT_TOKEN}{PARAM}?offset={offset + 1}").json()

    if updates["result"]:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            user_text = result['message']['text']
            kotik = requests.get(f'{CAT_URL_API}')
            answer(update_id=offset, chat__id=chat_id,
                   user__text=user_text, cat=kotik)

    time.sleep(3)
    end = time.time()
    print("Запрос на серве за апдейтом: ", end - start, " sec")
