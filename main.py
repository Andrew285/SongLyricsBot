import telebot
from bs4 import BeautifulSoup
import lxml
import requests

song_bot = telebot.TeleBot("2128007635:AAHuDH8KQlA_RwNDSHE_v2ME2I4tHizdWV8")

replaced_singer = ""

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
    song_bot.send_message(message.chat.id, f"{replaced_singer}+{replaced_song}")

#-----------------------------------GOOGLE------------------------------------------------------------------------
    page_google = requests.get(f"https://www.amazon.com/search?q={replaced_singer}+{replaced_song}+lyrics")
    soup = BeautifulSoup(page_google.text, "lxml")
    str_text = soup.text
    if "/" in str_text and "Джерело:" in str_text:
        start_index = str_text.index("/")
        last_index = str_text.index("Джерело:")

        result_text = str_text[start_index: last_index]
        song_bot.send_message(message.chat.id, result_text)

#--------------------------------------PISNI.UA------------------------------------------------------------------
    else:
        page_pisni = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics+pisni.org.ua")
        soup = BeautifulSoup(page_pisni.text, "lxml")

        # str_text = soup.text
        first_link = soup.find_all("a")[17]['href']
        new_page = requests.get(f"https://www.google.com/{first_link}")
        new_soup = BeautifulSoup(new_page.text, "lxml")

        str_text = new_soup.text
        if "Друк" in str_text and "ІНФОРМАЦІЯ" in str_text:
            # print(str_text)
            start_index = str_text.index(f"Друк") + 4
            last_index = str_text.index(f"ІНФОРМАЦІЯ")
            result_text = str_text[start_index:last_index].strip()
            song_bot.send_message(message.chat.id, result_text)

#-------------------------------------------AZLYRICS---------------------------------------------------------------
        else:
            page_az = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics+azlyrics")
            soup = BeautifulSoup(page_az.text, "lxml")

            # str_text = soup.text
            first_link = soup.find_all("a")[17]['href']
            new_page = requests.get(f"https://www.google.com/{first_link}")
            new_soup = BeautifulSoup(new_page.text, "lxml")

            str_text = new_soup.text
            if "Текст пісні" in str_text and "Writers" in str_text:
                # print(str_text)
                start_index = str_text.index(f"Текст пісні") + 4
                last_index = str_text.index(f"Writers")
                result_text = str_text[start_index:last_index].strip()
                song_bot.send_message(message.chat.id, result_text)

#------------------------------------------ON-HIT---------------------------------------------------------------
            else:
                page_hit = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics")
                soup = BeautifulSoup(page_hit.text, "lxml")

                # str_text = soup.text
                first_link = soup.find_all("a")[17]['href']
                new_page = requests.get(f"https://www.google.com/{first_link}")
                new_soup = BeautifulSoup(new_page.text, "lxml")

                str_text = new_soup.text
                # print(str_text)
                if "Поиск" in str_text and "Тексты песен" in str_text:
                    start_index = str_text.index(f"Поиск") + 7
                    last_index = str_text.index(f"Тексты песен")
                    result_text = str_text[start_index:last_index].strip()
                    song_bot.send_message(message.chat.id, result_text)

#----------------------------------------------------GENIUS-------------------------------------------------------------
                else:
                    page_genius = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics+genius")
                    soup = BeautifulSoup(page_genius.text, "lxml")

                    first_link = soup.find_all("a")[17]['href']
                    new_page = requests.get(f"https://www.google.com/{first_link}")
                    new_soup = BeautifulSoup(new_page.text, "lxml")

                    str_text = new_soup.text
                    # print(str_text)
                    if "LYRICS" in str_text and "MORE ON GENIUS" in str_text:
                        start_index = str_text.index(f"LYRICS") + 7
                        last_index = str_text.index(f"MORE ON GENIUS")
                        result_text = str_text[start_index:last_index].strip()
                        song_bot.send_message(message.chat.id, result_text)
                    else:
                        song_bot.send_message(message.chat.id, "Bot can't find the song lyrics")
song_bot.infinity_polling()