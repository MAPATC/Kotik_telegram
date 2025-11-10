import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

URL_API = os.getenv("URL")
CAT_URL_API = os.getenv("CATS_API")
BOT_TOKEN = os.getenv("TOKEN")
PARAM = "/getUpdates"
MAX_ITERATION = 60

offset = -2
counter = 0
chat_id: int
kotik: requests.Response

while counter < MAX_ITERATION:

    print("attempt =", counter)

    updates = requests.get(
        f"{URL_API}{BOT_TOKEN}{PARAM}?offset={offset + 1}").json()

    if updates["result"]:
        for result in updates["result"]:
            offset = result["update_id"]
            chat_id = result["message"]["from"]["id"]
            user_text = result["message"]["text"]
            requests.get(
                f'{URL_API}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Что значит "{user_text}"...?\nА пофиг, держи котика!')
            kotik = requests.get(f"{CAT_URL_API}")
            if kotik.status_code == 200:
                cat_photo_link = kotik.json()[0]["url"]
                requests.get(
                    f"{URL_API}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_photo_link}")
            else:
                requests.get(
                    f"{URL_API}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Котика нету :(")
    time.sleep(1)
    counter += 1
