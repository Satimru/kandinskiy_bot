import base64
import os
from io import BytesIO
from dotenv import load_dotenv
import telebot
from PIL import Image

from main import Text2ImageAPI

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
KANDINSKIY_URL = os.getenv("KANDINSKIY_URL")
KANDINSKIY_KEY = os.getenv("KANDINSKIY_KEY")
KANDINSKIY_SECRET_KEY = os.getenv("KANDINSKIY_SECRET_KEY")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши запрос, чтобы получить изображение.")


@bot.message_handler(func=lambda message: True)
def send_photo(message):
    prompt = message.text
    api = Text2ImageAPI(KANDINSKIY_URL, KANDINSKIY_KEY,
                        KANDINSKIY_SECRET_KEY)

    print("Work...")

    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)

    s64 = base64.b64decode(images[0])
    image = Image.open(BytesIO(s64))

    bot.send_photo(message.chat.id, image)


bot.polling()
