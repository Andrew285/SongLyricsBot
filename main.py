import telebot
from bs4 import BeautifulSoup
import lxml
import requests

song_bot = telebot.TeleBot("2128007635:AAHuDH8KQlA_RwNDSHE_v2ME2I4tHizdWV8")

replaced_singer = ""
replaced_song = ""

@song_bot.message_handler(content_types=["text"])
def get_singer(message):
    global replaced_singer
    mssg = message.text
    replaced_singer = mssg.replace(" ", "+")
    msg = song_bot.send_message(message.chat.id, "Now enter the song name:")
    song_bot.register_next_step_handler(msg, get_song)

def get_song(message):
    global replaced_singer
    mssg = message.text
    replaced_song = mssg.replace(" ", "+")

    page = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics")
    soup = BeautifulSoup(page.text, "lxml")

    str_text = soup.text
    index_find = str_text.index("/")
    last_index = str_text.index("Джерело:")

    result_text = str_text[index_find: last_index]
    song_bot.send_message(message.chat.id, result_text)


song_bot.infinity_polling()
